from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payments_dashboard, name='dashboard'),
    path('pay/<int:pk>/', views.pay_payment, name='pay'),
    path('invoice/<int:pk>/', views.invoice_view, name='invoice'),
]
