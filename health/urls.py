from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.HealthStatus.as_view(), name='health-check'),
]