from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from .models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import UserRegistration
from django.contrib import messages
from django.core.mail import send_mail
from .models import Cart
from .models import Order
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Wishlist
from .models import Support
from django.db.models import Sum, Count


from django.utils import timezone
from datetime import timedelta
# Create your views here.

def home(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(product_name__icontains=query)
    else:

        products=Product.objects.all()
    return render(request,"index.html",{'products':products,'query':query})

def admin_login(request):
    return render(request,"admin_login.html")

def alog(request):
    if request.method == "POST":
        admin_username=request.POST.get("admin_username")
        admin_password=request.POST.get("admin_password")
        user=auth.authenticate(username=admin_username,password=admin_password)
        if user is not None:
            auth.login(request,user)
            return redirect("admin_dashboard")
        else:
             return redirect("admin_login")
    else:
    
    
    
       return render(request,"admin_login.html")
    
def admin_dashboard(request):
    if request.user.is_authenticated:
         user_count = UserRegistration.objects.count()
         order_count=Order.objects.count()

         return render(request,"admin_dashboard.html",{"admin_name":request.user.username,'user_count':user_count,'order_count':order_count})
    else:
        return redirect("admin_login")

def add(request):
    return render(request,"add_product.html")

def add_product(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name", "").strip()
        product_description = request.POST.get("product_description", "").strip()
        product_price = request.POST.get("product_price", "").strip()
        product_image = request.FILES.get("product_image")

        # -------- Validation Starts --------
        if not product_name:
            messages.error(request, "Product name is required.")
            return render(request, "add_product.html", {"product_added": False})

        if len(product_name) < 3:
            messages.error(request, "Product name must be at least 3 characters long.")
            return render(request, "add_product.html", {"product_added": False})

        if not product_description:
            messages.error(request, "Product description is required.")
            return render(request, "add_product.html", {"product_added": False})

        if len(product_description) < 10:
            messages.error(request, "Description must be at least 10 characters long.")
            return render(request, "add_product.html", {"product_added": False})

        # Validate price
        try:
            price = float(product_price)
            if price <= 0:
                messages.error(request, "Price must be greater than 0.")
                return render(request, "add_product.html", {"product_added": False})
        except ValueError:
            messages.error(request, "Please enter a valid price.")
            return render(request, "add_product.html", {"product_added": False})

        # Validate image
        if not product_image:
            messages.error(request, "Please upload a product image.")
            return render(request, "add_product.html", {"product_added": False})
        # -------- Validation Ends --------

        
        Product.objects.create(
            product_name=product_name,
            product_description=product_description,
            product_price=price,
            product_image=product_image
        )

        messages.success(request, "Product added successfully!")
        return render(request, "add_product.html", {"product_added": True})

    return render(request, "add_product.html", {"product_added": False})


def product_list(request):
    products=Product.objects.all()
    return render(request,'product_list.html',{'products':products})

def update_product(request,id):
    product=Product.objects.get(id=id)

    if request.method == "POST":
        product.product_name=request.POST.get("product_name")
        product.product_description=request.POST.get("product_description")
        product.product_price=request.POST.get("product_price")

        if request.FILES.get("product_image"):
            product.product_image=request.FILES.get("product_image")

        product.save()
        return redirect('product_list')
    return render(request,"update_product.html",{"product":product})

def delete_product(request,id):
    product=Product.objects.get(id=id)
    product.delete()
    return redirect('product_list')
@login_required
def edit_profile(request):
    user=request.user

    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        if username:
            user.username=username
        if password:
            user.set_password(password)
        user.save()
        update_session_auth_hash(request,user)
        return redirect("admin_dashboard")
    return render(request,"edit_profile.html",{"user":user})


def user_register(request):
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        email=request.POST.get('email')
        address=request.POST.get('address')
        gender=request.POST.get('gender')
        pincode=request.POST.get('pincode')
        city=request.POST.get('city')
        state=request.POST.get('state')
        phone_number=request.POST.get('phone_number')

        if password !=confirm_password:
            messages.error(request,"passwords do not match")
            return redirect('home')
        if UserRegistration.objects.filter(username=username).exists():
            messages.error(request,"username already exists")
            return redirect('home')
        if UserRegistration.objects.filter(email=email).exists():
            return redirect('home')
        print(request.POST)

        UserRegistration(first_name=first_name,last_name=last_name,username=username,password=password,email=email,address=address,gender=gender,pincode=pincode,city=city,state=state,phone_number=phone_number).save()

        messages.success(request,"Registration successfull please login")
        return redirect('home')
    return redirect('home')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try to get the user with matching username
        try:
            user = UserRegistration.objects.get(username=username)
        except UserRegistration.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect('home')

        # Check password manually (since you're not using hashing)
        if user.password == password:
            # Send login email
            send_mail(
                subject='Login Successful - Eyeconic',
                message=(
                    f"Hi {user.first_name} {user.last_name},\n\n"
                    "You have successfully logged into Eyeconic.\n"
                    "Thank You For Choosing Eyeconic\n"
                    "The Eyeconic Team"
                ),
                from_email="anjananju19001@gmail.com",
                recipient_list=[user.email],
                fail_silently=True
            )

            # Store session
            request.session['user_id'] = user.id
            request.session['username'] = user.username

            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect('home')

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('home')

    return redirect('home')


def add_to_cart(request,product_id):
    if 'user_id'not in request.session:
        

        return redirect('home')
    
    user_id =request.session['user_id']
    user=UserRegistration.objects.get(id=user_id)

    try:
        product=Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('home')
    
    quantity = int(request.POST.get('quantity', 1))

    
    cart_item,created=Cart.objects.get_or_create(user=user,product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    

    return redirect('cart_page')
          

def cart_page(request):
    if 'user_id' not in request.session:
        return redirect('home')

    user_id = request.session['user_id']
    user = UserRegistration.objects.get(id=user_id)
    cart_items = Cart.objects.filter(user=user)

    # calculate total
    total = sum(item.product.product_price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})



def remove_from_cart(request, item_id):
    try:
        cart_item = Cart.objects.get(id=item_id)
        cart_item.delete()
    except Cart.DoesNotExist:
        pass  # If item not found, just ignore it
    return redirect("cart_page")


def user_logout(request):
    request.session.flush()
    messages.success(request,"you have been logged out successfully")
    return redirect('home')


def increase_quantity(request, item_id):
    item = get_object_or_404(Cart, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart_page')


def decrease_quantity(request, item_id):
    item = get_object_or_404(Cart, id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart_page')

def checkout(request, product_id=None):
    if 'user_id' not in request.session:
        messages.error(request, "Please login to continue.")
        return redirect('user_login')

    user = UserRegistration.objects.get(id=request.session['user_id'])

    if request.method == "POST":
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if not address or not phone:
            messages.error(request, "Please fill in all required fields.")
            return redirect(request.path)
        
        orders = []
        if product_id:  # Buy Now
            product = Product.objects.get(id=product_id)
            order_instance = Order.objects.create(
                user=user,
                product=product,
                quantity=1,
                address=address,
                phone=phone,
                total_price=product.product_price,
                status="Confirmed"
            )
            orders.append(order_instance)
        else:  # Cart checkout
            cart_items = Cart.objects.filter(user=user)
            if not cart_items.exists():
                messages.warning(request, "Your cart is empty.")
                return redirect('cart_page')

            for item in cart_items:
                order_instance = Order.objects.create(
                    user=user,
                    product=item.product,
                    quantity=item.quantity,
                    address=address,
                    phone=phone,
                    total_price=item.total_price(),
                    status="Confirmed"
                )
                orders.append(order_instance)
            cart_items.delete()

        
        return redirect('order_success', order_ids=",".join(str(o.id) for o in orders))

    
    if product_id:
        context = {'single_product': Product.objects.get(id=product_id)}
    else:
        cart_items = Cart.objects.filter(user=user)
        total = sum(item.total_price() for item in cart_items)
        context = {'cart_items': cart_items, 'total': total}

    return render(request, 'checkout.html', context)

def order_success(request, order_ids):
    order_ids = [int(i) for i in order_ids.split(",")]
    orders = Order.objects.filter(id__in=order_ids)

    # If user clicked "Download Invoice"
    if request.GET.get("download") == "invoice":
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        y = 800
        p.setFont("Helvetica-Bold", 16)
        p.drawString(200, y, "INVOICE")
        y -= 40

        p.setFont("Helvetica", 12)
        for order in orders:
            p.drawString(50, y, f"Product: {order.product.product_name}")
            y -= 20
            p.drawString(50, y, f"Quantity: {order.quantity}")
            y -= 20
            p.drawString(50, y, f"Price: {order.total_price}")
            y -= 20
            p.drawString(50, y, f"Address: {order.address}")
            y -= 20
            p.drawString(50, y, f"Phone: {order.phone}")
            y -= 40

            if y < 100:
                p.showPage()
                y = 800

        p.save()
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        return response

    return render(request, "order_success.html", {"orders": orders})


@login_required
def admin_orders(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    orders = Order.objects.all().order_by('-id')  # latest orders first
    return render(request, 'admin_orders.html', {'orders': orders})

def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()
        return redirect('admin_orders')

@login_required
def admin_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    users = UserRegistration.objects.all().order_by('id')
    return render(request, 'admin_users.html', {'users': users})
def user_dashboard(request):
    
    if 'user_id' not in request.session:
        messages.error(request, "Please login to access your dashboard.")
        return redirect('user_login')
    
    user = UserRegistration.objects.get(id=request.session['user_id'])
    orders = Order.objects.filter(user=user).order_by('-id')[:5]  # last 5 orders
    order_count = Order.objects.filter(user=user).count()

    context = {
        'user': user,
        'orders': orders,
        'order_count': order_count,
    }
    return render(request, 'user_dashboard.html', context)

def my_profile(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login first.")
        return redirect('user_login')

    user = get_object_or_404(UserRegistration, id=request.session['user_id'])
    return render(request, 'my_profile.html', {'user': user})


def my_orders(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login first.")
        return redirect('user_login')

    user = get_object_or_404(UserRegistration, id=request.session['user_id'])
    orders = Order.objects.filter(user=user)
    return render(request, 'my_orders.html', {'orders': orders})


def wishlist(request):
    # Check if the user is logged in via session
    if 'user_id' not in request.session:
        messages.error(request, "Please login to view your wishlist.")
        return redirect('user_login')

    # Get the currently logged-in user from session
    user = get_object_or_404(UserRegistration, id=request.session['user_id'])
    items = Wishlist.objects.filter(user=user)

    return render(request, 'wishlist.html', {'items': items})


def add_to_wishlist(request, product_id):
    # Check if user is logged in
    if 'user_id' not in request.session:
        messages.error(request, "Please login to add items to your wishlist.")
        return redirect('user_login')

    user = get_object_or_404(UserRegistration, id=request.session['user_id'])
    product = get_object_or_404(Product, id=product_id)

    # Check if already in wishlist
    if Wishlist.objects.filter(user=user, product=product).exists():
        messages.info(request, "This product is already in your wishlist.")
        return redirect('home')  # or wherever you want to redirect

    # Add to wishlist
    Wishlist.objects.create(user=user, product=product)
    messages.success(request, f"'{product.product_name}' added to your wishlist!")
    return redirect('home')

def remove_from_wishlist(request, product_id):
    if 'user_id' not in request.session:
        messages.error(request, "Please login to manage your wishlist.")
        return redirect('user_login')

    user = get_object_or_404(UserRegistration, id=request.session['user_id'])
    product = get_object_or_404(Product, id=product_id)

    wishlist_item = Wishlist.objects.filter(user=user, product=product)
    if wishlist_item.exists():
        wishlist_item.delete()
        messages.success(request, f"'{product.product_name}' removed from your wishlist!")
    else:
        messages.info(request, "Item not found in your wishlist.")

    return redirect('wishlist')

def support(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login to access support.")
        return redirect('user_login')

    user = UserRegistration.objects.get(id=request.session['user_id'])

    if request.method == "POST":
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        Support.objects.create(user=user, subject=subject, message=message)

        messages.success(request, "Your support request has been submitted successfully.")
        return redirect('support')

    # Show user’s previous support tickets
    tickets = Support.objects.filter(user=user).order_by('-created_at')

    return render(request, 'support.html', {'user': user, 'tickets': tickets})


def admin_reports(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = UserRegistration.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Optional: show orders for the last 7 days
    last_week = timezone.now() - timedelta(days=7)
    recent_orders = Order.objects.filter(ordered_at__gte=last_week).count()

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin_reports.html', context)

def admin_logout(request):
    auth.logout(request)
    messages.success(request,"You have been logged out from the admin portal")
    return redirect('home')