import decimal
import string
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect

from SsideApp.models import Category, Product
from .models import Order, UserRegistration,Cart,Address
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import cache_control
import random


def generate_numeric_otp(length=6):
    """Generates a random numeric OTP of given length."""
    return ''.join(random.choices(string.digits, k=length))
# Create your views here.

 
def email(request):
    return render(request,'email.html')
def otp_email(request):
    return render(request,'otp_email.html')
 
def login(request):
    return render(request,'login.html')
 
def register(request):
    return render(request,'register.html')
 
def cart(request):
    user = request.session.get('uid')
    cart_products = Cart.objects.filter(user_id=user)

    # Display Total on Cart Page
    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(10)
    
    # Check if any data exists in the Cart table
    print(Cart.objects.all())  # This should print out all cart objects in your database
    print(user)

    
    cp  = Cart.objects.filter(user=user)

    # Print out user for debugging
    
    print(f"cp:{cp}")
    if cp:
        for p in cp:
            temp_amount = (p.quantity * decimal.Decimal(p.product.itemprice))
            print(f"tempam:{temp_amount}")
            amount += temp_amount
            print(amount)

    # Customer Addresses
    addresses = Address.objects.filter(user_id=user)

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
    }
    return render(request,'cart.html', context)

def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('store')



def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('store')

def checkout(request):
    user = request.session.get('uid')
    address_id = request.GET.get('address')
    
    address = get_object_or_404(Address, id=address_id)
    # Get all the products of User in Cart
    cart = Cart.objects.filter(user=user)
    for c in cart:
        # Saving all the products from Cart to Order
        Order(user_id=user, address=address, product=c.product, quantity=c.quantity).save()
        # And Deleting from Cart
        c.delete()
    return redirect('order')


def order(request):
    all_orders = Order.objects.filter(user=request.session.get('uid')).order_by('-ordered_date')
    return render(request, 'order.html', {'orders': all_orders})


def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories':categories})

def category_products(request, id):
    category = get_object_or_404(Category, id=id)
    print(f"Category{category.title}")
    products = Product.objects.filter(category=category)
    print(f"Products:{products}")
    categories = Category.objects.filter()
    print(f"categories{categories}")
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'category_products.html', context)



from django.shortcuts import render
from .models import UserRegistration, Address, Order

def profile(request):
    user_id = request.session.get('uid')
    email = request.session.get('email')
    print(f"email: {email}")

    try:
        user = UserRegistration.objects.get(id=user_id)  # Use get() for a single user
        print(f"User: {user.email}")  # Access the email attribute directly
    except UserRegistration.DoesNotExist:
        user = None
        print("User not found")

    addresses = Address.objects.filter(user_id=user_id)
    orders = Order.objects.filter(user=user_id)

    return render(request, 'profile.html', {'addresses': addresses, 'orders': orders, 'user': user})
def update_user_info(request):

    
    if request.method == 'POST':
        uid= request.POST.get('user_id')
        print(f"Uid->{uid}")
        users = get_object_or_404(UserRegistration, id=uid)
        print(users)
        fullname = request.POST.get('username')
        print(fullname)
        email = request.POST.get('email')
        print(email)
        if 'item_image' in request.FILES:
            users.profilephoto = request.FILES['item_image']
            print(users.profilephoto)
        users.fullname=fullname
        users.email=email
        users.save()
        return redirect('profile')  # Redirect to the user's profile after saving

    return render(request, 'profile.html')
def add_address(request):
    return render(request,'add_address.html')
def detail(request, id):
    product = get_object_or_404(Product, id=id)
    related_products = Product.objects.exclude(id=product.id).filter(category=product.category_id)
    context = {
        'product': product,
        'related_products': related_products,

    }
    return render(request, 'detail.html', context)

    #return HttpResponse("this is homepage")
def about(request):
    return render(request, 'about.html')
    #return HttpResponse("this is aboutpage")
def services(request):
    return render(request, 'services.html')
def otp_verfiy(request):
    return render(request, 'otp_verfiy.html')
def reset_password(request):
    return render(request, 'reset_password.html')
def email_verfication(request):
    return render(request, 'email_verfication.html')
    #return HttpRespons                 e("this is servicepage")

def viewuser(request):
    users=UserRegistration.objects.all()
    return render(request,'viewuser.html',{'users': users})
    
def edit_user(request, id):
    user = get_object_or_404(UserRegistration, id=id)  # Retrieve the user instance
    if request.method == "POST":
        user.fullname = request.POST['fullname']  # Update the user fields
        user.email = request.POST['email']
        password = request.POST.get('password')
        if password:  # If password is provided, hash it and update
            user.password = make_password(password)
        user.usertype = request.POST['usertype']
        if 'profilephoto' in request.FILES:
            user.profilephoto = request.FILES['profilephoto']
        user.save()  # Save the updated user instance
        return redirect('viewuser')  # Redirect to the user dashboard after saving
    return render(request, 'viewuser.html', {'user': user})
def delete_user(request, id):
    user = get_object_or_404(UserRegistration, id=id)  # Fetch the user with the given ID
    user.isactive = False  # Set isactive to 0 (inactive)
    user.save()  # Save the changes
    return redirect('viewuser')

def delete_my_account(request):
    user_id = request.session.get('uid')  # Retrieve user ID from session

    if user_id:  # Ensure the user is logged in
        user = get_object_or_404(UserRegistration, id=user_id)  # Get the user from the DB
        user.isactive = False  # Set isactive to 0 (inactive)
        user.save()  # Save changes
        logout(request)  # Log the user out
        return redirect('login')  # Redirect to login page
    else:
        return redirect('login')  # Redirect to login page if no session is found

def process_registration(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        password = request.POST['password']
        
        if UserRegistration.objects.filter(email=email).exists():
            messages.error(request,"Email is Alreaday Exists")
            return render(request,'register.html')
        UserRegistration(fullname=fullname,email=email,password=make_password(password)).save()
        subject= 'Welcome to Mendor Store'
        html_message= render_to_string('email.html', {'fullname': fullname})
        plain_message = strip_tags(html_message)
        from_email = 'wwheisenberg2511@gmail.com'
        to = email
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        messages.success(request,'Regsitration Successfully')
        return redirect('login')
    return render(request,'regsiter.html')

    



def process_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        print(f"Login attempt: email={email}, password={password}")
        
        try:
            user = UserRegistration.objects.get(email=email)
            print(f"User found: {user}")
            if check_password(password, user.password):
                request.session['uid'] = user.id
                request.session['fullname'] = user.fullname
                request.session['email'] = user.email
                request.session['usertype'] = user.usertype
                messages.success(request, 'Login successfully')
                print("Login successful")

                if user.usertype == 0:
                    return redirect('index')
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, 'Invalid login credentials')
                print("Invalid password")
        except UserRegistration.DoesNotExist:
            messages.error(request, 'User does not exist')
            print("User does not exist")
    return render(request, 'login.html')

def send_otp(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user=UserRegistration.objects.get(email=email)
            otp = generate_numeric_otp()  # Generate numeric OTP

            request.session['otp'] = otp
            request.session['email'] = email


            # Send the OTP via email
            subject = 'OTP Verification'
            fullname = user.fullname  
            html_message = render_to_string('otp_email.html', {'fullname': fullname, 'otp': otp})
            plain_message = strip_tags(html_message)
            from_email = 'wwheisenberg2511@gmail.com'
            to = email
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            
            messages.success(request, 'OTP sent to your email.')
            return render(request, 'otp_verfiy.html', {'email': email})
           
        except UserRegistration.DoesNotExist:
            messages.error(request, 'Invalid login credentials')
            return render(request,'index.html')
    return render(request,'index.html')


def process_verfication(request):
    if request.method == "POST":
        email = request.POST['email']
        entered_otp = request.POST['otp']
        
        # Retrieve the stored OTP from the session
        stored_otp = request.session.get('otp')
        stored_email = request.session.get('email')

        # print(f"Email from form: {email}")
        #print(f"Entered OTP: {entered_otp}")
        #print(f"Stored OTP: {stored_otp}")
        #print(f"Stored Email: {stored_email}")

        if email == stored_email and entered_otp == stored_otp:
            messages.success(request, 'OTP verified successfully.')
            # Clear the OTP from the session
            del request.session['otp']
            del request.session['email']
            return render(request, 'reset_password.html', {'email': email})
# Redirect to reset password page
        else:
            messages.error(request, 'Invalid OTP.')
            return render(request, 'otp_verfiy.html', {'email': email})

    return render(request, 'otp_verfiy.html')

def process_rpassword(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        user=UserRegistration.objects.get(email=email)

        if password == cpassword and email == user.email:
            messages.success(request, 'reset password successfully.')
            password=make_password(password)
            user.password=password
            user.save()
            return redirect('index')  # Redirect to reset password page
        else:
            messages.error(request, 'Invalid or expired OTP.')
            return render(request, 'otp_verfiy.html', {'email': email})

    return render(request, 'otp_verfiy.html')

def process_address(request):
    if request.method == 'POST':
        user = request.session.get('uid')
        locality=request.POST['locality']
        city=request.POST['city']
        state=request.POST['state']
        Address(user_id=user, locality=locality, city=city, state=state).save()
        return redirect('profile')



def add_to_cart(request):
    user = request.session.get('uid')
    product_id = request.GET.get('prod_id')
    quantity = request.GET.get('quantity')
    print(quantity)
    # Default quantity to 1 if not provided
    if quantity is None:
        quantity = 1
    
    quantity = int(quantity)  # Ensure quantity is an integer
    print(f"quantity: {quantity}")

    # Check whether the Product is already in Cart or not
    item_already_in_cart = Cart.objects.filter(product_id=product_id, user_id=user)
    if item_already_in_cart.exists():
        cp = get_object_or_404(Cart, product_id=product_id, user_id=user)
        if cp.quantity is None:
            cp.quantity = 0  # Initialize quantity if it's None
        cp.quantity += quantity  # Add the quantity
        cp.save()
        messages.success(request, "Product quantity updated in your cart.")
    else:
        # Ensure the quantity is saved as an integer
        Cart(user_id=user, product_id=product_id, quantity=quantity).save()
        messages.success(request, "Product added to your cart.")
    
    return redirect('store')

def remove_address(request, id):
    Address.objects.get(id=id).delete()
    messages.success(request, "Address removed.")
    return redirect('profile')

def remove_cart(request,id):
    Cart.objects.get(id=id).delete()
    messages.success(request, "Product removed from Cart.")
    return redirect('store')



def logout_view(request):
    logout(request)
    request.session.flush()
    messages.success(request, "You have successfully logged out")
    return redirect('index')
