from django.shortcuts import HttpResponse

def index(request):
    return HttpResponse("<a href='https://ninish.com'>Visit Ninish</a>")