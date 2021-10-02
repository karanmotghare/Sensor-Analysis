from django.shortcuts import redirect,render
from django.http import HttpResponse,JsonResponse
from models_dir.models import *
#from models import SuperAdmins

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
    #print(request)
    username = request.POST.get('username')
    password = request.POST.get('password')
    admin_stat = request.POST.get('admin_opt')

    # If the user is superAdmin
    if admin_stat == 's_admin':
        user = SuperAdmins.objects.filter(username=username)

        if user:
            if user[0].pwd == password:
                return display_orgs(request)
            else:
                return render(request, 'index.html')
        else:
            return render(request, 'index.html') 

    else:
        user = Users.objects.filter(username=username)

        if user:
            if user[0].pwd == password:
                return render(request, 'homepage.html')
            else:
                return render(request, 'index.html')
        else:
            return render(request, 'index.html') 


    #print(admin_stat)

    return render(request,'index.html')


def homepage(request):

    return render(request,'homepage.html')


# Code for displaying list of orgs in form
def display_orgs(request):
    #print(request)
    #print(orgs)
    admin_stat = request.POST.get('admin_opt')

    # If super admin, display all orgs list
    if admin_stat == 's_admin':
        orgs = Organisation.objects.all()
        
        org = {
            "orgs" : orgs,
            "roles" : [
                {'name':'Org Admin', 'value':'org_admin'},
                {'name':'Location Admin', 'value':'loc_admin'},
                {'name':'Other User', 'value':'loc_admin'}
            ]
        }

        #print(org["orgs"])
        
        
        
    # Else display the organisation of person/user
    else:
        user = Users.objects.filter(username=request.POST.get('username'))
        orgs = Organisation.objects.filter(org_id=user[0].org)

        org = {
            "orgs" : orgs,
            "roles" : [
                {'name':'Org Admin', 'value':'org_admin'},
                {'name':'Location Admin', 'value':'loc_admin'},
                {'name':'Other User', 'value':'loc_admin'}
            ]
        }
        

    return render(request, 'addUser.html', org)

# Code to add new user
def add_user(request):

    username = request.POST.get('username')
    password = request.POST.get('password')
    org_id = request.POST.get('org_opt')
    post = request.POST.get('post_opt')

    user = Users(username=username, pwd=password, position=post, org=Organisation.objects.filter(org_id=org_id)[0], created_by="admin")
    user.save()

    return render(request, 'success.html')
