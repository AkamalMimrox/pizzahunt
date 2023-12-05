from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import CategoriesMaster, ProductMaster, about, AddressMaster, Order, OrderItem
from carton.cart import Cart
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import AddressForm
from PizzaStore.custom.order_id_genrate import genrate_orderId
from PizzaStore.custom.tracking_number import generate_tracking_number

from django.conf import settings
from django.core.mail import send_mail


login_uri = 'login'


def index(request):
    categories = CategoriesMaster.objects.all()[:4]
    # cart_icon_clicked = request.GET.get('cart_icon_clicked')

    # if cart_icon_clicked:
    #     messages.success(request, 'Item added to cart!')

    context = {
        "categories": categories,
        "products": render_products(),
    }

    return render(request, 'index.html', context)


def detail(request, slug):
    product = get_object_or_404(ProductMaster, slug=slug)
    try:

        context = {
            'product': product
        }
        return render(request, 'food/food_detail.html', context)
    except product.DoesNotExist:
        return HttpResponse('The product you are looking for not exist or removed!')


def menu(request):
    categories = CategoriesMaster.objects.all()

    context = {
        "categories": categories,
        "products": render_products(),

    }

    return render(request, 'menu.html', context)


def about_view(request):
    return render(request, 'about.html',)


def book(request):
    return render(request, 'book.html')


def cart(request):
    cart = Cart(request.session)
    context = {
        "cart": cart
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, slug):
    cart = Cart(request.session)
    slug = slug

    product = ProductMaster.objects.filter(slug=slug).first()
    if product:
        cart.add(product=product, price=product.price, quantity=1)
        messages.success(request, message=f'{product.name} is add to cart')
        return redirect('cart')


def increment(request, slug):
    cart = Cart(request.session)
    product = ProductMaster.objects.filter(slug=slug).first()
    if product:
        cart.add(product=product, price=product.price, quantity=1)
        return redirect('cart')


def decrement(request, slug):
    cart = Cart(request.session)
    product = ProductMaster.objects.filter(slug=slug).first()
    if product:
        cart.remove_single(product=product)
        return redirect('cart')


def removeitem(request, slug):
    cart = Cart(request.session)
    product = ProductMaster.objects.filter(slug=slug).first()
    if product:
        cart.remove(product=product)
        return redirect('cart')


@login_required(login_url=login_uri)
def checkout(request):
    cart = Cart(request.session)
    form = AddressForm()
    existing_address = AddressMaster.objects.filter(user=request.user)
    selected_address = request.POST.get('selected-address')

    if request.method == "POST":
        selected_address = request.POST.get('selected-address')

        if selected_address is None:
            messages.error(
                request, message="Please select address or add new address!")
            pass
        if selected_address:
            address = AddressMaster.objects.filter(id=selected_address).first()

            if address:
                order = Order()
                order.user = request.user
                order.id = genrate_orderId()
                order.order_total = cart.total
                order.tracking_number = generate_tracking_number()
                order.shiping_address = address

                order = procced_order(request, cart, address)
                order.save()
                subject = 'welcome pizzahunt'
                message = f'Hi {request.user.username}, thank you for order your order will reach you soon. you can track your order by {order.tracking_number}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email, ]
                send_mail(subject, message, email_from, recipient_list )

                cart.clear()
                return redirect('index')
            else:
                return HttpResponse("Error")

        else:
            addnewaddress(request)
    context = {
        "cart": cart,
        "form": form,
        "existing_address": existing_address
    }
    return render(request, 'checkout/checkout.html', context)




def orders(request):
    order = Order.objects.filter(user=request.user)
    context={
        'order' : order
    }
    return render(request,'orders/orders_section.html',context)


def procced_order(request, cart, address):
    order = Order.objects.create(
        id=genrate_orderId(),
        user=request.user,
        order_total=cart.total,
        shiping_address=address,
        tracking_number=generate_tracking_number()
    )

    for item in cart.items:
        order_items = OrderItem.objects.create(
            user=request.user,
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )
        order_items.save()
    return order


def addnewaddress(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            pass
        else:
            return HttpResponse("Form is not valid!")


def render_products():
    return ProductMaster.objects.all()
