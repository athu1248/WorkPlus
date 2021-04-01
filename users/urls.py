from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:groupid>/', views.profile, name='profile'),
    path('register/', views.register, name="register")
]
