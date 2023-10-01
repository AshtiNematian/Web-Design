from django.shortcuts import render

# Create your views here.
# views.py

from rest_framework import generics
from .models import ServicesList
from .serializer import ServicesSerializer


class ServicesListView(generics.ListAPIView):
    queryset = ServicesList.objects.all()
    serializer_class = ServicesSerializer


class ServicesDetailsView(generics.RetrieveAPIView):
    queryset = ServicesList.objects.all()
    serializer_class = ServicesSerializer
