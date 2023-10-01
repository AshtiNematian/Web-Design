# urls.py

from django.urls import path
from .views import ServicesDetailsView,ServicesListView

urlpatterns = [
    path('Servics/', ServicesListView.as_view(), name='services-list'),
    path('Servics/<int:pk>/', ServicesDetailsView.as_view(), name='Services-detail'),
]
