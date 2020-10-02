from django.shortcuts import render
import requests
from rest_framework.views import APIView
from django.conf import settings
from .models import ytVideo
from django.views.generic import ListView
import threading
import time
import schedule
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .serializer import VidSerializer
from rest_framework.response import Response
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

#to call and update data from yt search api
def ytplay(code=0):
    #search URL
    search_url = settings.SEARCH_URL
    #key
    key = eval(settings.YOUTUBE_DATA_API_DIC)
    #params
    params = {
        'part': 'snippet',
        'q': 'cricket',
        'key': key[code],
        'maxResults': 25,
        'type': 'video',
        'order': 'date',
        'publishedAfter': '2020-09-28T00:00:00Z'
    }

    try:
        rget = requests.get(search_url, params=params)
        # no. of results
        n = int(rget.json()["pageInfo"]["resultsPerPage"])
        #remove items
        ytVideo.objects.filter(iduid=1).delete()
        #add again
        for i in range(1, n):
            ytVideo.objects.create_ytVid(rget.json()['items'][i]["snippet"]["title"], rget.json()['items'][i]["snippet"]["description"], rget.json()[
                'items'][i]["snippet"]["publishedAt"], rget.json()['items'][i]["snippet"]["thumbnails"]["medium"]["url"], 1)
        return
    except:
        codeId = int(rget.json()["error"]["code"])
        code = code+1
        #code 403 is either forbidden or quota exhausted
        if(codeId == 403 and code < int(settings.MAX_KEY)):
            ytplay(code)
        else:
            return

#List for dashboard
class YTListView(ListView):
    model = ytVideo
    template_name = 'ytapi/home.html'
    def get_queryset(self):
        #page no.
        page = self.request.GET.get('page', 0)
        #query filter
        query = self.request.GET.get('name')
        #ordering
        order = self.request.GET.get('ordering','de')
        #no. of pages for pagination
        noperpage = self.request.GET.get('noperpage', 9)
        if noperpage is '':
            noperpage = 9
        object_list = self.model.objects.all()
        if query:
            object_list = object_list.filter(
                    Q(title__icontains=query) | Q(description__icontains=query))
        if order=='as':
            object_list = object_list.order_by('publishingDT')
        try:
            paginator = Paginator(object_list, noperpage)
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(1)
        return object_list
    def get(self, request, *args, **kwargs):
        ytplay()
        return super(YTListView, self).get(request, *args, **kwargs)

#Get api paginated
class VidAPIView(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        #elements per page=3
        paginator.page_size = 3
        vids = ytVideo.objects.all()
        result_page = paginator.paginate_queryset(vids, self.request)
        serializer = VidSerializer(result_page, many=True)
        return Response(serializer.data)
