from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.contrib.auth.models import User
from .models import *
from .forms import *


# Create your views here.
def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:6]
    return render(request, 'core/inicio.html',{
        'featured_products': featured_products
        })
    
def catalogo(request):
    products = Product.objects.all()
    return render(request, 'core/catalogo.html', {
        'products': products,
        'user': request.user
    })

@login_required
def solicitudreciclaje(request):
    if request.method == 'POST':
        form = SolicitudReciclajeForm(request.POST)
        if form.is_valid():
            soli_reciclaje = form.save(commit=False)
            soli_reciclaje.user = request.user  
            # Asigna el usuario actual
            soli_reciclaje.save()
            messages.success(request, 'Solicitud enviada exitosamente')
            return redirect('')
    else:
        form = SolicitudReciclajeForm()
    
    return render(request, 'core/solicitud_reciclaje.html', {
        'form': form
    })

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'core/carrito.html', {
        'cart': cart
    })

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Verificar si el producto ya está en el carrito
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        # Si ya existe, actualizamos la cantidad (máximo 1 según requerimientos)
        cart_item.quantity = 1
        cart_item.save()
    
    messages.success(request, 'Producto agregado al carrito')
    return redirect('catalog')

@login_required
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, 'Producto eliminado del carrito')
    except CartItem.DoesNotExist:
        messages.error(request, 'El producto no se encuentra en el carrito')
    return redirect('cart')


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.cartitem_set.exists():
            messages.error(request, 'Tu carrito está vacío')
            return redirect('cart')
            
        if request.method == 'POST':
            # Crear la orden
            order = Order.objects.create(
                user=request.user,
                total=cart.get_total(),
                status='PENDING'
            )
            
            # Transferir items del carrito a la orden
            for item in cart.cartitem_set.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Limpiar el carrito
            cart.cartitem_set.all().delete()
            
            messages.success(request, 'Pedido realizado exitosamente')
            return redirect('')
            
        return render(request, 'core/checkout.html', {
            'cart': cart
        })
        
    except Cart.DoesNotExist:
        messages.error(request, 'No se encontró el carrito')
        return redirect('home')
    
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')
    
def registrar(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Autenticar y loguear al usuario después del registro
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('in')
    else:
        form = SignUpForm()
    return render(request, 'core/registrar.html', {'form': form})