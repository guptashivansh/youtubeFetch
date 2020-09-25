from django.shortcuts import render
from rest_framework import viewsets
from .serializers import VideoSerializer
from .models import Videos
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.search import SearchQuery, SearchRank

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q,F
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

# Create your views here.

class NodeResultsSetPagination(LimitOffsetPagination):
    default_limit = 5
    offset_query_param = 'skip'


class VideoViewSet(viewsets.ModelViewSet):
    # queryset = Videos.objects.all()
    search_fields = ['title', 'description']
    filter_backends = ( DjangoFilterBackend,filters.OrderingFilter)
    # filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    filter_fields = ['title', 'description','channel_title']
    ordering_fields = ['title', 'description','publishedDateTime','channel_title']
    serializer_class = VideoSerializer
    pagination_class = NodeResultsSetPagination

    def get_queryset(self, *args, **kwargs):
        qs = Videos.objects.all()
        search = self.request.GET.get("search", None)
        if search:
            try:
                # search_string = self.request.GET['search']
                search_string = SearchQuery(self.request.GET['search'])
                print(search_string)
                # qs = qs.annotate(similarity=TrigramSimilarity('title', search_string)).filter(similarity__gt=0.01).order_by('-similarity')
                qs = qs.annotate(title_rank=SearchRank(F('title_vector'),search_string,)
                    ).annotate(description_rank=SearchRank(F('description_vector'),search_string,)
                    ).annotate(rank=F('title_rank') + F('description_rank')
                    ).filter(Q(title_rank__gt=0.0) | Q(rank__gt=0.0)
                    ).order_by('-title_rank','-publishedDateTime')
                print(qs.first())
                return qs
            except KeyError:
                return Videos.objects.none()
        return qs.order_by('-publishedDateTime')