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
                status='pending',
                color=item.color,
                profile=item.profile,
                gauge=item.gauge,
                length=item.length,
                width=item.width,
                height=item.height,
                price_at_addition=item.unit_price  # important!

            )

        # Clear cart after creating orders
        cart_items.delete()

        return redirect('order_success')  # Redirect to order success page

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

from django.shortcuts import render, get_object_or_404
from .models import Order

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'user/order_detail.html', {
        'order': order
    })


from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from django.contrib.auth.decorators import login_required
from cart.models import Cart  # Your Cart model

@login_required
def download_order_pdf(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_cart_price = sum([item.total_cost for item in cart_items])

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []

    styles = getSampleStyleSheet()
    heading_style = styles['Heading1']
    heading_style.alignment = 1  # Center
    elements.append(Paragraph(f"Order Summary for {request.user.first_name} {request.user.last_name}", heading_style))
    elements.append(Spacer(1, 12))

    # Table header
    data = [["Product", "Attributes", "Quantity", "Total (TZS)"]]

    cell_style = ParagraphStyle(name='cell', fontSize=10, leading=12)

    for item in cart_items:
        product_name_para = Paragraph(item.product.name, cell_style)
        attributes = []

        # Roofing / Tile / Steel / Other products
        if item.color: attributes.append(f"Color: {item.color.title()}")
        if item.profile: attributes.append(f"Profile: {item.profile.title()}")
        if item.gauge: attributes.append(f"Gauge: {item.gauge.gauge}")
        if item.length: attributes.append(f"Length: {item.length}")
        if item.width: attributes.append(f"Width: {item.width}")
        if item.height: attributes.append(f"Height: {item.height}")

        attr_text = Paragraph("<br/>".join(attributes) if attributes else "—", cell_style)

        data.append([
            product_name_para,
            attr_text,
            str(item.quantity),
            f"{item.total_cost:,.2f}"
        ])

    # Table column widths
    table = Table(data, colWidths=[200, 180, 50, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#174376")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))

    # Alternate row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.HexColor("#f2f2f2"))]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Total price at bottom
    total_style = ParagraphStyle(name='total', fontSize=12, leading=14, alignment=2, spaceBefore=10)
    elements.append(Paragraph(f"Total Product Cost: {total_cart_price:,.2f} TZS", total_style))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="order_summary.pdf"'
    return response
