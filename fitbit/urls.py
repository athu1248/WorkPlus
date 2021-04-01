from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='fitbit-home'),
    path("disconnectfitbit", views.disconnectConfirmation, name='disconnect-fitbit')
]
