from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from .models import Category, Products, Customer, Order, OrderItem
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


# ==========================
# Static & Homepage
# ==========================

class Index(View):
    def get(self, request):
        categories = Category.getAllCategory()
        products = Products.getAllProducts()

        return render(request, 'index.html', {
            'products': products,
            'categories': categories,
        })


def about(request):
    return render(request, 'about.html')


# ==========================
# Authentication
# ==========================

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')

    post_data = request.POST
    f_name = post_data.get('first name')
    l_name = post_data.get('last name')
    email = post_data.get('email')
    passwd = post_data.get('password')
    phone = post_data.get('phone')

    values = {
        'First_Name': f_name,
        'Last_Name': l_name,
        'Email_Id': email,
        'Phone_No': phone
    }

    customer = Customer(first_name=f_name, last_name=l_name, email=email, password=passwd, phone=phone)

    error = None
    if not f_name:
        error = 'First name required'
    elif not l_name:
        error = 'Last name required'
    elif not phone or len(phone) < 11:
        error = 'Valid phone number required'
    elif not email:
        error = 'Email required'
    elif customer.isExist():
        error = 'Email already exists'
    elif not passwd or len(passwd) < 8:
        error = 'Password must be at least 8 characters'

    if error:
        return render(request, 'signup.html', {'error': error, 'values': values})

    customer.password = make_password(passwd)
    customer.register()
    return redirect('productIndex')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    email = request.POST.get('email')
    password = request.POST.get('password')
    customer = Customer.loginByEmail(email)

    error = None
    if customer and check_password(password, customer.password):
        request.session['cust_email'] = customer.email
        return redirect('productIndex')
    else:
        error = 'Invalid credentials'

    return render(request, 'login.html', {'error': error})


def logout(request):
    request.session.pop('cust_email', None)
    return redirect('productIndex')


# ==========================
# Cart Handling
# ==========================

class Cart(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = Products.objects.filter(id__in=cart.keys())

        cart_items = []
        total_price = 0

        for product in products:
            quantity = cart[str(product.id)]['quantity']
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

        return render(request, 'cart.html', {
            'cart_items': cart_items,
            'total_price': total_price
        })


class UpdateCart(View):
    def post(self, request):
        product_id = request.POST.get('prodId')
        remove = request.POST.get('remove') == 'True'
        cart = request.session.get('cart', {})

        added, removed = False, False

        if product_id:
            if product_id in cart:
                if remove:
                    cart[product_id]['quantity'] -= 1
                    if cart[product_id]['quantity'] <= 0:
                        del cart[product_id]
                    removed = True
                else:
                    cart[product_id]['quantity'] += 1
                    added = True
            else:
                if not remove:
                    cart[product_id] = {'quantity': 1}
                    added = True

        request.session['cart'] = cart
        redirect_url = request.META.get('HTTP_REFERER', 'productIndex')
        if added:
            return redirect(f"{redirect_url}?added=true")
        elif removed:
            return redirect(f"{redirect_url}?removed=true")
        return redirect(redirect_url)


class ClearCart(View):
    def post(self, request):
        request.session['cart'] = {}
        return redirect('cart')


# ==========================
# Checkout & Orders
# ==========================

@method_decorator(never_cache, name='dispatch')
class Checkout(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = Products.objects.filter(id__in=cart.keys())

        cart_items = []
        total = 0

        for product in products:
            quantity = cart[str(product.id)]['quantity']
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

        return render(request, 'checkout.html', {
            'cart_items': cart_items,
            'total': total
        })

    def post(self, request):
        customer_email = request.session.get('cust_email')
        if not customer_email:
            return redirect('login')

        try:
            customer = Customer.objects.get(email=customer_email)
        except Customer.DoesNotExist:
            return redirect('login')

        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method', '').strip().lower()

        if payment_method != 'cod':
            return HttpResponseForbidden("Unsupported payment method selected.")

        cart = request.session.get('cart', {})
        products = Products.objects.filter(id__in=cart.keys())

        order = Order.objects.create(
            customer=customer,
            address=address,
            phone=phone,
            total=0,
            status='pending'
        )

        total = 0
        for product in products:
            quantity = cart[str(product.id)]['quantity']
            subtotal = product.price * quantity
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=subtotal
            )
            total += subtotal

        order.total = total
        order.save()
        request.session['cart'] = {}

        return redirect('order-success')


class OrderSuccess(View):
    def get(self, request):
        customer_email = request.session.get('cust_email')
        if not customer_email:
            return redirect('login')

        customer = Customer.objects.get(email=customer_email)
        order = Order.objects.filter(customer=customer).order_by('-date').first()

        if not order:
            return redirect('productIndex')

        return render(request, 'order_success.html', {'order': order})
