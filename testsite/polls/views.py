from django.shortcuts import render

from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello. You're at polls index")



# Create your views here.
