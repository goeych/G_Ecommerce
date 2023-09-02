from django.urls import path
from django.contrib.auth import views
from .views import start_order

app_name='order'
urlpatterns =[
    path('start_order/',start_order,name='start_order'),
   
] 