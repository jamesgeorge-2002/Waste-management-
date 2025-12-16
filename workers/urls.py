from django.urls import path
from . import views

app_name = 'workers'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pickup/<int:pickup_id>/update/', views.update_pickup_status, name='update_pickup'),
]
