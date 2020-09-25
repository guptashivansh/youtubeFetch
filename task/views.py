from django.shortcuts import render
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.search import SearchQuery, SearchRank
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q,F

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination


from .serializers import VideoSerializer
from .models import Videos
from .filters import CustomSearchFilter




# Create your views here.

class NodeResultsSetPagination(LimitOffsetPagination):
    default_limit = 5
    offset_query_param = 'skip'


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Videos.objects.all()
    search_fields = ['title', 'description']
    filter_backends = (CustomSearchFilter,  DjangoFilterBackend,filters.OrderingFilter)
    filter_fields = ['title', 'description','channel_title']
    ordering_fields = ['title', 'description','publishedDateTime','channel_title']
    serializer_class = VideoSerializer
    pagination_class = NodeResultsSetPagination
    # filter_backends = (filters.SearchFilter,filters.OrderingFilter)

    # return the result after doing a full text search on the queryset
    # def get_queryset(self, *args, **kwargs):
        # qs = Videos.objects.all()
        # search = self.request.GET.get("search", None)
        # if search:
        #     try:
        #         # search_string = self.request.GET['search']
        #         search_string = SearchQuery(self.request.GET['search'])
        #         print(search_string)
                
        #         # trigram search which didn't work
        #         # qs = qs.annotate(similarity=TrigramSimilarity('title', search_string)).filter(similarity__gt=0.01).order_by('-similarity')
                
                
        #         #anmotate adds to the qs the search rank for search string for 
        #         # title and vector and then we filter according to the match
        #         # we can increase the vector field match values to get a closed match of required
        #         # this should be a configurable value defined in DB or env to change it when required
        #         qs = qs.annotate(title_rank=SearchRank(F('title_vector'),search_string,)
        #             ).annotate(description_rank=SearchRank(F('description_vector'),search_string,)
        #             ).annotate(rank=F('title_rank') + F('description_rank')
        #             ).filter(Q(title_rank__gt=0.0) | Q(rank__gt=0.0)
        #             ).order_by('-title_rank','-publishedDateTime')




        #         # print(qs.first())
        #         return qs
        #     except KeyError:
        #         return Videos.objects.none()
        # return qs.order_by('-publishedDateTime')