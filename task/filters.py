from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import Q,F

from rest_framework import filters

from .models import *

class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return super(CustomSearchFilter, self).get_search_fields(view, request)

    def filter_queryset(self,request, queryset, view):
        qs = Videos.objects.all()
        search = request.GET.get("search", None)
        if search:
            try:
                # search_string = self.request.GET['search']
                search_string = SearchQuery(request.GET['search'])
                print(search_string)
                
                # trigram search which didn't work
                # qs = qs.annotate(similarity=TrigramSimilarity('title', search_string)).filter(similarity__gt=0.01).order_by('-similarity')
                
                
                #anmotate adds to the qs the search rank for search string for 
                # title and vector and then we filter according to the match
                # we can increase the vector field match values to get a closed match of required
                # this should be a configurable value defined in DB or env to change it when required
                qs = qs.annotate(title_rank=SearchRank(F('title_vector'),search_string,)
                    ).annotate(description_rank=SearchRank(F('description_vector'),search_string,)
                    ).annotate(rank=F('title_rank') + F('description_rank')
                    ).filter(Q(title_rank__gt=0.0) | Q(rank__gt=0.0)
                    ).order_by('-title_rank','-publishedDateTime')




                # print(qs.first())
                return qs
            except KeyError:
                return Videos.objects.none()
        return qs.order_by('-publishedDateTime')