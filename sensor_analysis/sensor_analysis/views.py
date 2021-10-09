from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect,render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
        if user:
            if user[0].pwd == password:
                request.isAuthorized = True
                request.session['user'] = username
                request.session['admin_stat'] = 's_admin'
                request.isSuperAdmin = True

                return HttpResponseRedirect("/sAdmin")
            else:
                return render(request, 'index.html')
        else:
            return render(request, 'index.html') 

    else:
        user = Users.objects.filter(username=username)
        if user:
            if user[0].pwd == password:
                request.isAuthorized =True
                request.session['user'] = username
                request.session['admin_stat'] = user[0].position
                request.isSuperAdmin = False

                return HttpResponseRedirect("/home")
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
    #request.isAuthorized = True

    try:
        del request.session['user']
        del request.session['admin_stat']
        request.isSuperAdmin = False

    except:
        request.isSuperAdmin = False
        return HttpResponseRedirect("/")

    return HttpResponseRedirect("/")

def homepage(request):
    if 'user' in request.session:
        #print(request.session['user'])

        user = Users.objects.filter(username=request.session['user']) 
        org = user[0].org       

        # Location list
        locations = Location.objects.filter(org=org)

        # Sensor Group List
        


        mapper={
            'locations':locations,
            'heading':'Sensor Analysis',
            'display':'display: block'
        }
        return render(request,'homepage.html',mapper)
    else:
        return HttpResponseRedirect("/")

def sAdmin(request):
    #print(request.session['user'])
    #print(request.isSuperAdmin)
    if 'user' in request.session:
        return display_orgs(request)

    return HttpResponseRedirect('/')

# Code for displaying list of orgs in form
def display_orgs(request):
    #print(request)
    #print(orgs)
    #admin_stat = request.POST.get('admin_opt')
    #print(admin_stat)
    # If super admin, display all orgs list
    if request.session['admin_stat'] == 's_admin' :
        orgs = Organisation.objects.all()
        
        org = {
            "orgs" : orgs,
            "roles" : [
                {'name':'Org Admin', 'value':'org_admin'},
                {'name':'Location Admin', 'value':'loc_admin'},
                {'name':'Other User', 'value':'loc_admin'}
            ],
            'heading':'Super Admin Portal',
            'display':'display: block',
        }

        request.isSuperAdmin = True
        #print(org["orgs"])
        
        
        
    # Else display the organisation of person/user
    else:
        user = Users.objects.filter(username=request.session['user'])
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
        
        request.isSuperAdmin = False

    return render(request, 'addUser.html', org)

# Code to add new user
def add_user(request):

    if 'user' in request.session:
        username = request.POST.get('username')
        password = request.POST.get('password')
        org_id = request.POST.get('org_opt')
        post = request.POST.get('post_opt')

        user = Users(username=username, pwd=password, position=post, org=Organisation.objects.filter(org_id=org_id)[0], created_by="admin")
        user.save()

        return render(request, 'success.html')

# Function to render adding organisation
def add_org(request):
    if request.session['admin_stat']=='s_admin':
        return render(request, 'addOrg.html')
    
    return HttpResponseRedirect('/home')

# Function to add new organisation
def add_new_org(request):
    
    if 'user' in request.session:
        if request.isSuperAdmin:
            name = request.POST.get('org_name')
            addr = request.POST.get('address')

            org = Organisation(org_name=name, address=addr)
            org.save()

            return render(request, 'success.html')
        
        else:
            return HttpResponseRedirect('/home')
    
    else:
        return HttpResponseRedirect('/')

def chart_js(request):

    return render(request,'chartdemo.html')

# Function to load sensor groups
@csrf_exempt
def getSgAjax(request):

    if request.method == "POST":
        location_id = request.POST['location_id']
        try:
            if location_id:
                location = Location.objects.filter(loc_id = location_id).first()
                sgs = SensorGroup.objects.filter(loc = location)
            else:
                sgs = SensorGroup.objects.none()
        except Exception:
            request.data['error_message'] = 'error'
            return JsonResponse(request.data)
        return JsonResponse(list(sgs.values('sg_id', 'sg_name')), safe = False) 

# Function to load sensors
@csrf_exempt
def getSensorAjax(request):

    if request.method == "POST":
        sg_id = request.POST['sg_id']
        try:
            if sg_id:
                sg = SensorGroup.objects.filter(sg_id = sg_id).first()
                sensors = Sensor.objects.filter(sg = sg)
            else:
                sensors = Sensor.objects.none()
        except Exception:
            request.data['error_message'] = 'error'
            return JsonResponse(request.data)
        return JsonResponse(list(sensors.values('sensor_id', 'sensor_name')), safe = False) 

