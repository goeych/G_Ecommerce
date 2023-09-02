from django.urls import path
from django.contrib.auth import views
from .views import home,shop,signup,myaccount,edit_myaccount

app_name='core'
urlpatterns =[
    path('',home,name='home'),
    path('shop/',shop,name='shop'),
    path('signup/',signup,name='signup'),
    path('login/',views.LoginView.as_view(template_name= 'core/login.html'),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('myaccount/',myaccount,name='myaccount'),
    path('myaccount/edit/',edit_myaccount,name='edit_myaccount'),

] 
