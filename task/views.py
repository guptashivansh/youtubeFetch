from django.shortcuts import render
from rest_framework import viewsets
from .serializers import VideoSerializer
from .models import Videos

from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

# Create your views here.
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5

class NodeResultsSetPagination(LimitOffsetPagination):
    default_limit = 5
    offset_query_param = 'skip'


class VideoViewSet(viewsets.ModelViewSet):
    # queryset = Videos.objects.all()
    queryset = Videos.objects.all().order_by('publishedDateTime')
    # queryset = Videos.objects.all().order_by('url')
    serializer_class = VideoSerializer
    pagination_class = NodeResultsSetPagination