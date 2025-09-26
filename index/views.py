from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    host = request.get_host()
    return HttpResponseRedirect('/api')