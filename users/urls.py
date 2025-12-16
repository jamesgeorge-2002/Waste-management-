from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report/', views.report_waste, name='report_waste'),
    path('pickup/<int:pickup_id>/reschedule/', views.request_reschedule, name='request_reschedule'),
]
