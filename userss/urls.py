from django.contrib import admin
from django.urls import path
from .views import Login,user_logout,my_users,register_users,change_password,password_fill

urlpatterns = [
    path('register/',register_users,name="register" ),
    path('login/',Login.as_view(),name="login" ),
    path('logout/',user_logout,name="logout" ),
    path('myusers/',my_users,name="all_users" ),
    path('changepasswd/',change_password,name="change_passwd" ),
    path("passwd/",password_fill)

]