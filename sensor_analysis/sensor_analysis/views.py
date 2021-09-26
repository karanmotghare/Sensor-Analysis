from django.shortcuts import redirect,render
from django.http import HttpResponse,JsonResponse

def indexPage(request):    

    return render(request,'index.html',)