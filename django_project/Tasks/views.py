from django.shortcuts import render
from django.http import HttpResponse

def m_page(request):
    return render(request, 'base.html')
