from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def xyz(request):
    return render(request,"index.html")
def signUp(request):
    print("signup method is working")
    i=5
    i=i+7
    j=i
    j=j+i
    return render(request,"index.html")
