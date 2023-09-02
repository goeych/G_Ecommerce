
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',include('core.urls',namespace='core')),
    path('admin/', admin.site.urls),
    path('product/',include('product.urls',namespace='product')),
    path('cart/',include('cart.urls',namespace='cart')),
    path('order/',include('order.urls',namespace='order')),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
