"""
URL patterns for merchants app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_merchant, name='register_merchant'),
    path('status/', views.check_status, name='check_status'),
    path('status/<str:registration_number>/', views.merchant_status, name='merchant_status'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
