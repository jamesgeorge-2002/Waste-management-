from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/user/', views.register_user_view, name='register_user'),
    path('register/worker/', views.register_worker_view, name='register_worker'),
]
