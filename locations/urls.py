from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    path('api/wards/', views.wards_for_localbody, name='api_wards'),
]
