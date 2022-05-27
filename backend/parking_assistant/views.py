from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import caches
import redis

def get_available_spots(request):    
    r = redis.Redis()
    available_spots = r.get("free_spots").decode('utf-8')
    print(available_spots)
    return HttpResponse(str(available_spots))
