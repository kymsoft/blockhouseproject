#from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    #return HttpResponse('Hello World!')
    return render(request, 'home.html')