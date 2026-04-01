from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_map, name='analytics_map'),
]