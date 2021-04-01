from django.urls import path
from . import views

urlpatterns = [
    path('newGroup/', views.newGroup, name='new-group'),
    path('<str:groupid>/', views.group, name='group'),
]
