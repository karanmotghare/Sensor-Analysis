from django.shortcuts import redirect,render
from django.http import HttpResponse,JsonResponse
from models_dir.models import *
#from models import SuperAdmins

def indexPage(request):    
    mapper={
    'heading':'Sensor Analysis',
    'display':'display: none'
    }
    request.isAuthorized = True
    return render(request,'index.html',context=mapper)

def login_access(request):
    #print(request)
    username = request.POST.get('username')
    password = request.POST.get('password')
    admin_stat = request.POST.get('admin_opt')

    request.isAuthorized = False


    # If the user is superAdmin
    if admin_stat == 's_admin':
        user = SuperAdmins.objects.filter(username=username)
        request.isSuperAdmin = True
        if user:
            if user[0].pwd == password:
                request.isAuthorized = True
                return display_orgs(request)
            else:
                return render(request, 'index.html')
        else:
            return render(request, 'index.html') 

    else:
        user = Users.objects.filter(username=username)
        request.isSuperAdmin = False
        if user:
            if user[0].pwd == password:
                request.isAuthorized =True
                return render(request, 'homepage.html')
            else:
                return render(request, 'index.html')
        else:
            return render(request, 'index.html') 


    #print(admin_stat)

    return render(request,'index.html')


def logout(request):
    mapper={
    'heading':'Sensor Analysis',
    'display':'display: none'
    }
    request.isAuthorized = True

    return render(request,'index.html',mapper)

def homepage(request):
    mapper={
    'heading':'Sensor Analysis',
    'display':'display: block'
    }
    return render(request,'homepage.html',mapper)


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
            ],
            'heading':'Super Admin Portal',
            'display':'display: block'
        }

        #print(org["orgs"])
        
        
        
    # Else display the organisation of person/user
    else:
        user = Users.objects.filter(username=request.POST.get('username'))
        orgs = [user[0].org]

        org = {
            "orgs" : orgs,
            "roles" : [
                {'name':'Org Admin', 'value':'org_admin'},
                {'name':'Location Admin', 'value':'loc_admin'},
                {'name':'Other User', 'value':'loc_admin'}
            ],
            'heading':'Admin Portal',
            'display':'display: block'
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

# Function to render adding organisation
def add_org(request):

    return render(request, 'addOrg.html')

# Function to add new organisation
def add_new_org(request):

    name = request.POST.get('org_name')
    addr = request.POST.get('address')

    org = Organisation(org_name=name, address=addr)
    org.save()

    return render(request, 'success.html')


def chart_js(request):

    return render(request,'chartdemo.html')