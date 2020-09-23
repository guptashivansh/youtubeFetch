from django.shortcuts import render
from rest_framework import viewsets
from .serializers import VideoSerializer
from .models import Videos

# Create your views here.

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Videos.objects.all().order_by('title')
    serializer_class = VideoSerializer