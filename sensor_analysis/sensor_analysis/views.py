from django.shortcuts import redirect,render
from django.http import HttpResponse,JsonResponse

def indexPage(request):    

    return render(request,'index.html',)

def get_admin_rank(admin):
    admin_map={
        's_admin':1,
        'n_admin':2,
    }

    return admin_map[admin]

def verify_log_details(u_name,u_pass,u_admin):
    return True

def login_access(request):
    
    username = request.POST['username']
    password = request.POST['password']
    admin_stat = request.POST['admin_opt']



    print(admin_stat)

    return render(request,'index.html')


def homepage(request):

    return render(request,'homepage.html')