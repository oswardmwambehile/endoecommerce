from django.shortcuts import render
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login, logout
import re

from django.shortcuts import render
from products.models import Category, Product


def home(request):
    categories = Category.objects.all()
    featured_products = []

    # Pick one product per category
    for category in categories:
        product = category.products.first()  # first product in category
        if product:
            featured_products.append(product)
        if len(featured_products) >= 8:
            break  

    context = {
        'featured_products': featured_products,
    }
    return render(request, 'user/home.html', context)


def register(request):
    # Always available — so template can load dropdowns
    REGION_CHOICES = User.REGION_CHOICES

    if request.method == 'POST':
        # Collect form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        fund_available = request.POST.get('fund_available', 'No')
        pickup_location = request.POST.get('pickup_location', '').strip()
        site_region = request.POST.get('site_region', '').strip()
        site_location = request.POST.get('site_location', '').strip()
        contact = request.POST.get('contact', '').strip()
        password = request.POST.get('password', '')
        password1 = request.POST.get('password1', '')

        # -------------------- VALIDATIONS --------------------
        # First Name
        if len(first_name) < 3:
            messages.error(request, 'First name must be at least 3 characters long.')
            return redirect('register')
        if not re.match(r"^[a-zA-Z\s]*$", first_name):
            messages.error(request, 'First name can only contain letters and spaces.')
            return redirect('register')

        # Last Name
        if len(last_name) < 3:
            messages.error(request, 'Last name must be at least 3 characters long.')
            return redirect('register')
        if not re.match(r"^[a-zA-Z\s]*$", last_name):
            messages.error(request, 'Last name can only contain letters and spaces.')
            return redirect('register')

        # Email
        if not email:
            messages.error(request, 'Email is required.')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('register')

        # Contact
        if contact:
            if not re.match(r'^(?:\+255|0)[67][0-9]\d{7}$', contact):
                messages.error(request, 'Enter a valid Tanzanian phone number (e.g. +255712345678 or 0712345678).')
                return redirect('register')

        # Password
        if len(password) < 5:
            messages.error(request, 'Password must be at least 5 characters long.')
            return redirect('register')
        if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            messages.error(request, 'Password must contain both letters and numbers.')
            return redirect('register')
        if password != password1:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # -------------------- CREATE USER --------------------
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            fund_available=fund_available,
            pickup_location=pickup_location,
            site_region=site_region,
            site_location=site_location,
            contact=contact
        )
        user.save()

        messages.success(request, 'You have successfully registered.')
        return redirect('login')

    # -------------------- GET REQUEST --------------------
    return render(request, 'user/register.html', {'REGION_CHOICES': REGION_CHOICES})




def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # your login form input name
        password = request.POST.get('password')

        # Authenticate with email
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            

            # ✅ Redirect based on user type
            if user.user_type == 'admin':
                return redirect('dashboard')  # admin page
            elif user.user_type == 'customer':
                return redirect('home-index')  # customer page
            else:
                return redirect('profile')  # fallback if user_type missing
        else:
            messages.error(request, 'Wrong email or password combination.')
            return redirect('login')
    else:
        return render(request, 'user/login.html')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home-index')
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')


from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ChangePasswordForm  # assuming you created this form in forms.py


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(user=request.user, data=request.POST)
            
            if form.is_valid():
                # Save the new password
                form.save()
                update_session_auth_hash(request, form.user)  # Important to keep the user logged in
                messages.success(request, 'Your password has been updated successfully!')
                return redirect('change_password')  # Redirect to the profile page or another appropriate page
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = ChangePasswordForm(user=request.user)
        
        return render(request, 'user/change_password.html', {'form': form})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')
    



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    user = request.user  
    context = {
        'user': user,
    }
    return render(request, 'user/profile.html', context)




