from .views import *
from django.urls import path
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('register/',register, name="register"),
    path('login/',login_def, name="login"),
    path('logout/',LogoutView.as_view(), name="logout")
]
