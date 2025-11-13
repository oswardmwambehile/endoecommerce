from django.shortcuts import render, redirect
from django.contrib import messages
from .models import  Order
from cart .models import Cart

def checkout(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must login first to access the page')
        return redirect('login')

    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_cart_price = sum(item.total_cost for item in cart_items)

    if request.method == 'POST':
        
        for item in cart_items:
            Order.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity,
                status='pending'
            )

        
        cart_items.delete()

        return redirect('order_success')  # Redirect to an order success page

    return render(request, 'user/checkout.html', {
        'cart_items': cart_items,
        'total_cart_price': total_cart_price,
    })


from django.shortcuts import render, redirect
from django.contrib import messages

def order_success(request):
    if request.user.is_authenticated:
        user = request.user
        # Combine first and last name if they exist, otherwise fallback to email
        full_name = ''
        if hasattr(user, 'first_name') and hasattr(user, 'last_name'):
            full_name = f"{user.first_name} {user.last_name}".strip()
        if not full_name:
            full_name = getattr(user, 'email', 'Valued Customer')  # fallback to email or generic
        return render(request, 'user/order_success.html', {'full_name': full_name})
    else:
        messages.error(request, 'You must login first to access the page')
        return redirect('login')
    

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order

def order_progress(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must login first to access the page')
        return redirect('login')

    orders = Order.objects.filter(user=request.user).order_by('-order_date')  # latest first

    # Calculate total cost safely
    total_cost = sum([float(order.total_cost) for order in orders if order.total_cost is not None])

    return render(request, 'user/order.html', {
        'orders': orders,
        'total_cost': total_cost
    })


from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from django.contrib.auth.decorators import login_required
from cart .models import Cart  # Your Cart model

@login_required
def download_order_pdf(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_cart_price = sum([item.total_cost for item in cart_items])

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []

    styles = getSampleStyleSheet()
    heading_style = styles['Heading1']
    heading_style.alignment = 1  # Center heading
    elements.append(Paragraph("Order Summary", heading_style))
    elements.append(Spacer(1, 12))

    # Table header
    data = [["Product", "Color", "Gauge", "Profile", "Quantity", "Total (TZS)"]]

    # Define a Paragraph style for cells (wrap long text)
    cell_style = ParagraphStyle(name='cell', fontSize=10, leading=12)

    for item in cart_items:
        product = item.product
        color = gauge = profile = "—"

        if hasattr(product, 'roofing_attributes'):
            color = product.roofing_attributes.color.title()
            gauge = product.roofing_attributes.gauge
            profile = product.roofing_attributes.profile.title()
        elif hasattr(product, 'tile_attributes'):
            color = product.tile_attributes.color.title()
            gauge = product.tile_attributes.gauge
            profile = product.tile_attributes.profile.title()

        product_name_para = Paragraph(product.name, cell_style)

        data.append([
            product_name_para,
            color,
            gauge,
            profile,
            str(item.quantity),
            f"{item.total_cost:,.2f}"
        ])

    # Table with column widths
    table = Table(data, colWidths=[200, 60, 50, 80, 50, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#174376")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))

    # Alternate row background colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (-1, i), colors.HexColor("#f2f2f2"))
            ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Total price
    total_style = ParagraphStyle(name='total', fontSize=12, leading=14, alignment=2, spaceBefore=10)
    elements.append(Paragraph(f"Total Product Cost: {total_cart_price:,.2f} TZS", total_style))

    # Build PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="order_summary.pdf"'
    return response
