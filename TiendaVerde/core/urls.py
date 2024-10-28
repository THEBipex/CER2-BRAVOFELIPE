from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalogo, name='catalog'),
    path('recycling/', views.solicitudreciclaje, name='recycling'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    # Incluir las URLs de autenticación
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.registrar, name='signup'),
]
     
    