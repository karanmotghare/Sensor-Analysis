from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect,render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from models_dir.models import *
import json

#from models import SuperAdmins

#index page
def indexPage(request):    
    mapper={
    'heading':'Sensor Analysis',
    'display':'none'
    }
    request.isAuthorized = True
    return render(request,'index.html',context=mapper)

#login request check
def login_access(request):
    #print(request)
    username = request.POST.get('username')
    password = request.POST.get('password')
    admin_stat = request.POST.get('admin_opt')

    request.isAuthorized = False
    mapper={
    'heading':'Sensor Analysis',
    'display':'none'
    }

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
                return render(request, 'index.html', context=mapper)
        else:
            return render(request, 'index.html', context=mapper) 

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
                return render(request, 'index.html', context=mapper)
        else:
            return render(request, 'index.html', context=mapper) 


    #print(admin_stat)

    return render(request,'index.html')

#logout function
def logout(request):
    mapper={
    'heading':'Sensor Analysis',
    'display':'none'
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
            'display':'block'
        }
        return render(request,'homepage.html',mapper)
    else:
        return HttpResponseRedirect("/")

def sAdmin(request):
    #print(request.session['user'])
    #print(request.isSuperAdmin)
    if 'user' in request.session:
        if request.session['admin_stat'] == 's_admin' :
            orgs = Organisation.objects.all()

            org = {
                "orgs" : orgs,
                "roles" : [
                    {'name':'Org Admin', 'value':'org_admin'},
                    {'name':'Location Admin', 'value':'loc_admin'},
                    {'name':'Other User', 'value':'user'}
                ],
                'heading':'Super Admin Portal',
                'display':'block',
                'msg_display':False
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
                    {'name':'Other User', 'value':'user'}
                ],
                'heading':'Admin Portal',
                'display':'block',
                'msg_display':False

            }

            request.isSuperAdmin = False

        return render(request, 'addUser.html', org)
    else:
        return HttpResponseRedirect('/')



# Code to add new user
def add_user(request):

    if 'user' in request.session:
        username = request.POST.get('username')
        password = request.POST.get('password')
        org_id = request.POST.get('org_opt')
        post = request.POST.get('post_opt')
        
  
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
                'display':'block',
                'msg_display':True,
                'msg':"Entry added successfully",
                'style': {
                    'color':'green',
                    'bg_color':'#B2EFA8'
                },
       
            }

            request.isSuperAdmin = True

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
                'display':'block',
                'msg_display':True,
                'msg':"Entry added successfully",
                'style': {
                    'color':'green',
                    'bg_color':'#B2EFA8'
                },
                

            }

        if len(username) > 0 and len(password)>0:
            user = Users(username=username, pwd=password, position=post, org=Organisation.objects.filter(org_id=org_id)[0], created_by="admin")
            user.save()
        else:
            org['msg']="Please enter valid details"
            org['style']={'color':'red','bg_color':'#F5B3B4'}

        return render(request, 'addUser.html',org)

# Function to render adding organisation
def add_org(request):
    mapper={
    'heading':'Super Admin Portal',
    'display':'block',
    'msg_display':False
    }

    if request.session['admin_stat']=='s_admin':
        request.isSuperAdmin=True

        return render(request, 'addOrg.html',mapper)
    
    return HttpResponseRedirect('/home')

# Function to add new organisation
def add_new_org(request):
    mapper={
    'heading':'Super Admin Portal',
    'display':'block',
    'msg_display':True,
    'msg':"Entry added successfully",
    'style': {
        'color':'green',
        'bg_color':'#B2EFA8'
        },
    }
    request.isSuperAdmin=True


    if 'user' in request.session:
        if request.isSuperAdmin:
            name = request.POST.get('org_name')
            addr = request.POST.get('address')

            org = Organisation(org_name=name, address=addr)
            org.save()
            request.isSuperAdmin=True
            return render(request, 'addOrg.html',mapper)
        
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

# Function to get sensor data
@csrf_exempt
def getDataValues(request):
    
    if request.method == "POST":
        sensors_list = (json.loads(request.POST['sensors']))["data"]
        to = request.POST["to_time"]
        frm = request.POST["from_time"]
        print(sensors_list, to, frm)
        # Initialise the return list
        data_list = []
        
        try:
            if sensors_list:
                
                # Get data for every sensor
                for sensor in sensors_list:
                    
                    val = sensor.split(',')
                    sns = Sensor.objects.filter(sensor_id = val[2])
                    data = SensorActualData.objects.filter(sensor = sns[0], record_time__lte = to, record_time__gte = frm)

                    lst = []

                    for point in data:
                        value = {
                            'x' : point.record_time,
                            'y' : point.data_value
                        }

                        lst.append(value)

                    obj = {
                        'label' : sns[0].sensor_name,
                        'data' : lst 
                    }

                    data_list.append(obj)

        except Exception:
            request.data['error_message'] = Exception
            return JsonResponse(request.data)
        
        return JsonResponse(list(data_list) , safe=False)
