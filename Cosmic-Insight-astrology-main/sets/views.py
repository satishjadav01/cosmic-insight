from django.shortcuts import render,HttpResponse

def temp(request):
    d = {
        'no':1,
        'name':'Thakor',
        'zodiac sign':'Taurus (Vrishabha)',
        'best for jobs like':['fashion designing','Lawyer']
    }

    return HttpResponse(f"<h1>{d}</h1>")

# Create your views here.
