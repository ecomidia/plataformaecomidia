from .models import User, Status,Hashtag,Url
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, StatusSerializer
from django.db.models import Count
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import requests
import lxml.html
import datetime
from django.db.models import Count, Sum, F

# Create your views here.

def filtering(request):
    query = Status.objects.all()
    date_type = request.GET['datetype']
    if(date_type == 'range'):
        start = request.GET['start']
        end = request.GET['end']
        query = query.filter(created_at__gte=start).filter(created_at__lte=end)
    elif(date_type == 'relative'):
        last = int(request.GET['last'])
        lastDate = datetime.datetime.now() - datetime.timedelta(hours=last)
        query = query.filter(created_at__gte=lastDate)


    return query

def status_view(request):
    #Status.objects.all().values('favorite_count','retweet_count').annotate(total=Sum(F('favorite_count')+F('retweet_count'))).order_by('-favorite_count')
    query = filtering(request)
    type = request.GET['type']
    if (type == 'engagement'):
        query = query.values('id').annotate(total=Sum(F('favorite_count')+F('retweet_count'))).order_by('-total')
    else:
        query = query.values("id").order_by('-created_at')
    query = json.dumps({ 'data': list(query[:20])} )
    return HttpResponse(query, content_type='application/json')

class StatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
    queryset = Status.objects.all().order_by('-created_at')
    serializer_class = StatusSerializer

def hashtags_view(request):
    query = filtering(request)
    query = query.filter(hashtags__isnull=False).values("hashtags").annotate(total=Count('hashtags')).order_by('-total')
    query = json.dumps({ 'data': list(query[:3])} )
    return HttpResponse(query, content_type='application/json')

def images_view(request):
    #Status.objects.all().values('favorite_count','retweet_count').annotate(total=Sum(F('favorite_count')+F('retweet_count'))).order_by('-favorite_count')
    query = filtering(request)
    type = request.GET['type']
    if (type == 'engagement'):
        query = query.filter(photos__isnull=False).values('photos__media_url','favorite_count','retweet_count').annotate(total=Sum(F('favorite_count')+F('retweet_count'))).order_by('-total')
    else:
        query = query.filter(photos__isnull=False).values("photos__media_url").order_by('-created_at')
    query = json.dumps({ 'data': list(query[:8])} )
    return HttpResponse(query, content_type='application/json')

def entities_view(request):
    query = filtering(request)
    query = query.filter(entities__isnull=False).values("entities__name").annotate(total=Count('entities__name')).order_by('-total')[:4]
    query = json.dumps({ 'data': list(query)} )
    return HttpResponse(query, content_type='application/json')

def links_view(request):
    #Status.objects.all().values('favorite_count','retweet_count').annotate(total=Sum(F('favorite_count')+F('retweet_count'))).order_by('-favorite_count')
    #query = Status.objects.filter(urls__isnull=False).values("urls","urls__expanded_url",'urls__meta_title','urls__meta_content','urls__meta_image').annotate(total=Count('urls__expanded_url')).order_by('-total')[:3]
    query = filtering(request)
    type = request.GET['type']
    if (type == 'engagement'):
        query = query.filter(urls__isnull=False).values("urls","urls__expanded_url",'urls__meta_title','urls__meta_content','urls__meta_image').annotate(total=Count('urls__expanded_url')).order_by('-total')[:5]
    else:
        query = query.filter(urls__isnull=False).exclude(urls__meta_title__exact='').values("urls","urls__expanded_url",'urls__meta_title','urls__meta_content','urls__meta_image','user__screen_name').order_by('-created_at')[:5]
    for item in query:   
        u = item['urls__expanded_url']
        url = Url.objects.get(pk=item['urls'])
        if(url.meta_title == None or url.meta_title == ''):
            headers = headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"} 
            try:
                r = requests.get(url=u,headers=headers).text
            except:
                continue
            doc = lxml.html.fromstring(r)

            try:
                title = doc.xpath("//meta[@property='og:title']")
                title = title[0].get('content')
            except:
                Url.objects.filter(pk=item['urls']).update(meta_title='', meta_content='', meta_image = '')
                item['meta_title'] = ''
                item['meta_content'] = ''
                item['meta_image'] = ''
                continue


            content = doc.xpath("//meta[@property='og:description']")
            if(len(content)):
                content = content[0].get('content')
            else:
                content = None

            image = doc.xpath("//meta[@property='og:image']")
            if(len(image)):
                image = image[0].get('content')
            else:
                image = None

            Url.objects.filter(pk=item['urls']).update(meta_title=title, meta_content=content, meta_image = image)
            item['meta_title'] = title
            item['meta_content'] = content
            item['meta_image'] = image


    query = json.dumps({ 'data': list(query)[:3]} )
    return HttpResponse(query, content_type='application/json')