from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import UpdateCart
from .views import ClearCart
from .views import Checkout
from .views import OrderSuccess
from .views import about


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view(), name='productIndex'),
    path('about', about, name='about'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('cart', views.Cart.as_view(), name='cart'),
    path('update-cart', UpdateCart.as_view(), name='update-cart'),
    path('clear-cart', ClearCart.as_view(), name='clear-cart'),
    path('checkout', Checkout.as_view(), name='checkout'),
    path('order-success', OrderSuccess.as_view(), name='order-success'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
