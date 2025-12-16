from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('pickups/', views.pickups_list, name='pickups_list'),
    path('pickups/<int:pickup_id>/assign/', views.assign_pickup, name='assign_pickup'),
]
