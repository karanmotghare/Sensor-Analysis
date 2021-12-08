from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect,render
from django.http import HttpResponse,JsonResponse
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from models_dir.models import *
import json
import random
from datetime import datetime, timedelta
import numpy
from scipy import stats
from statsmodels.tsa.stattools import adfuller

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

        try:
            user = Users(username=username, pwd=password, position=post, org=Organisation.objects.filter(org_id=org_id)[0], created_by="admin")
            user.save()
        except Exception:
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

            try:
                org = Organisation(org_name=name, address=addr)
                org.save()
            except Exception:
                mapper['msg']="Please enter valid details"
                mapper['style']={'color':'red','bg_color':'#F5B3B4'}

            request.isSuperAdmin=True
            return render(request, 'addOrg.html',mapper)
        
        else:
            return HttpResponseRedirect('/home')
    
    else:
        return HttpResponseRedirect('/')

def chart_js(request):

    return render(request,'chartdemo.html')

def data_Gen(request):
    mapper ={ 
    'heading':'Data Generation Portal',
    }
    return render(request,'dataGeneration.html',mapper)

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
        # print(sensors_list, to, frm)
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
                            'x' : (point.record_time).strftime('%Y-%m-%d %H:%M:%S'),
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


# data generation function 
#lb- lower bound
#ub- upper bound
#status- char either 'I' or 'D' for increasing or decreasing slope & 'R' for random
def data_gen_function(lb,ub,status):
    lb=int(lb)
    ub=int(ub)
    data_list = []
    val=0
    count=0
    if status=='I':
        # for increasing slope points
        while count<20:
            val = random.randint(lb,ub)
            data_list.append(val)
            lb=val
            count+=1
        data_list.sort()
    elif status=='D':
        # for decreasing slope points
        while count<20:
            val=random.randint(lb,ub)
            data_list.append(val)
            ub=val
            count+=1
        data_list.sort(reverse=True) #gives the points in decreasing order
    else:
        # for random points
        while count<20:
            val = random.randint(lb,ub)
            data_list.append(val)
            count+=1
        data_list.sort()

    return data_list


############################################################################################################################
#wrapper function where you get points values from user
#function is incomplete and changes need to be made
def wrap_data_gen(points_list,pattern_name):
    points_list=list(points_list)
    length = len(points_list)
    data_points=[]


    if pattern_name=="r_ptn":
        #random pattern
        data_points=data_gen_function(points_list[0],points_list[1],'R')

    elif pattern_name=="n_ptn":
        #N_pattern assuming 4 points
        #[0]-start/lb
        # [1]-end/ub
        # [2]-minima
        # [3]-maxima

        data_points=data_gen_function(points_list[0],points_list[3],'I')
        data_points.extend(data_gen_function(points_list[3],points_list[2],'D'))
        data_points.extend(data_gen_function(points_list[2],points_list[1],'I'))

#################################################################################################################

# Function to redirect to data generation page
def dataGen(request):
    if 'user' in request.session:
        #print(request.session['user'])

        user = Users.objects.filter(username=request.session['user']) 
        org = user[0].org       

        # Location list
        locations = Location.objects.filter(org=org)

        mapper={
            'locations':locations,
            'heading':'Data Generation Portal',
            'display':'block'
        }
        return render(request,'dataGeneration.html',mapper)
    else:
        return HttpResponseRedirect("/")

# Function to save the generated data
def saveGenData(data, sensor):

    versions = SensorGenData.objects.filter(sensor = sensor)
    latest_v = 0

    ver = versions.aggregate(Max('version_id'))
    
    if ver['version_id__max']:
        latest_v = ver['version_id__max']
    
    current = latest_v + 1

    return current

# Function to create user generated graph for option 1
@csrf_exempt
def option_1_graph(request):
    if request.method == "POST":
        sensors_data = (json.loads(request.POST['sensors']))["data"]
        to = datetime.strptime(request.POST["to_time"], '%Y-%m-%d %H:%M:%S')
        frm = datetime.strptime(request.POST["from_time"], '%Y-%m-%d %H:%M:%S')

        # Initialise the return list
        data_list = []

        try:
            if sensors_data:

                # Get the name of sensor
                values = sensors_data[0].split(',')
                sensor = Sensor.objects.filter(sensor_id = values[2])
                name = sensor[0].sensor_name

                # Divide the data equally for the given time interval
                length = len(sensors_data)
                
                time_delta = ((to - frm).total_seconds()) / (length - 1)

                time_list = [frm]
                curr = frm
                for x in range(length-1):
                    curr = curr + timedelta(seconds = time_delta)
                    time_list.append(curr.strftime('%Y-%m-%d %H:%M:%S'))

                # Create data points with corresponding time
                lst = []
                i = 0
                for point in sensors_data:
                    val = (point.split(','))[3]
                    value = {
                        'x' : time_list[i],
                        'y' : val
                    }

                    lst.append(value)
                    i = i+1

                obj = {
                    'label' : name,
                    'data' : lst 
                }

                data_list.append(obj)

        except Exception:
            request.data['error_message'] = Exception
            return JsonResponse(request.data)
        
        return JsonResponse(list(data_list) , safe=False)

@csrf_exempt
def option_1_insert_db(request):
    if request.method == "POST":
        sensors_data = (json.loads(request.POST['sensors']))["data"]
        to = datetime.strptime(request.POST["to_time"], '%Y-%m-%d %H:%M:%S')
        frm = datetime.strptime(request.POST["from_time"], '%Y-%m-%d %H:%M:%S')

        # Initialise the return list
        data_list = []

        try:
            if sensors_data:

                # Get the name of sensor
                values = sensors_data[0].split(',')
                sensor = Sensor.objects.filter(sensor_id = values[2])
                name = sensor[0].sensor_name

                # Divide the data equally for the given time interval
                length = len(sensors_data)
                
                time_delta = ((to - frm).total_seconds()) / (length - 1)

                time_list = [frm]
                curr = frm
                for x in range(length-1):
                    curr = curr + timedelta(seconds = time_delta)
                    time_list.append(curr.strftime('%Y-%m-%d %H:%M:%S'))

                # Create data points with corresponding time
                lst = []
                i = 0
                for point in sensors_data:
                    val = (point.split(','))[3]
                    value = {
                        'x' : time_list[i],
                        'y' : int(val)
                    }

                    lst.append(value)
                    i = i+1

                version_id = saveGenData(lst, sensor[0])

                # obj = {
                #     'label' : name,
                #     'data' : lst 
                # }

                # data_list.append(obj)

        except Exception:
            request.data['error_message'] = Exception
            return JsonResponse(request.data)
        
        return JsonResponse(version_id , safe=False)


# Function to create user generated graph for option 2
@csrf_exempt
def option_2_graph(request):
    if request.method == "POST":
        sensors_data = (json.loads(request.POST['sensors']))["data"]
        
        # Initialise the return list
        data_list = []

        try:
            if sensors_data:

                # Get the name of sensor
                values = sensors_data[0].split(',')
                sensor = Sensor.objects.filter(sensor_id = values[2])
                name = sensor[0].sensor_name

                # Create data points with corresponding time
                lst = []
                for point in sensors_data:
                    arr = point.split(',')
                    val = arr[3]
                    time = datetime.strptime(arr[4], '%Y-%m-%d %H:%M:%S')
                    value = {
                        'x' : time.strftime('%Y-%m-%d %H:%M:%S'),
                        'y' : val
                    }

                    lst.append(value)

                obj = {
                    'label' : name,
                    'data' : lst 
                }

                data_list.append(obj)

        except Exception:
            request.data['error_message'] = Exception
            return JsonResponse(request.data)
        
        return JsonResponse(list(data_list) , safe=False)

@csrf_exempt
def option_2_insert_db(request):
    if request.method == "POST":
        sensors_data = (json.loads(request.POST['sensors']))["data"]
        
        # Initialise the return list
        data_list = []

        try:
            if sensors_data:

                # Get the name of sensor
                values = sensors_data[0].split(',')
                sensor = Sensor.objects.filter(sensor_id = values[2])
                name = sensor[0].sensor_name

                # Create data points with corresponding time
                lst = []
                for point in sensors_data:
                    arr = point.split(',')
                    val = arr[3]
                    time = datetime.strptime(arr[4], '%Y-%m-%d %H:%M:%S')
                    value = {
                        'x' : time.strftime('%Y-%m-%d %H:%M:%S'),
                        'y' : val
                    }

                    lst.append(value)

                version_id = saveGenData(lst, sensor[0])

                # obj = {
                #     'label' : name,
                #     'data' : lst 
                # }

                # data_list.append(obj)

        except Exception:
            request.data['error_message'] = Exception
            return JsonResponse(request.data)
        
        return JsonResponse(version_id , safe=False)

# Function to calculate statistics
def num_unique(data):
    return len(set(data))

def mean_val(data):
    return numpy.mean(data)

def quartile_val(data, num):
    return numpy.percentile(data, num)

def mode_val(data):
    print((stats.mode(data)).mode[0])
    return int((stats.mode(data)).mode[0])

def std_val(data):
    return numpy.std(data)

@csrf_exempt
def getStatistics(request):
    if request.method == "POST":
        sensors_data = json.loads(request.POST['sensors_data']) 
        # print(sensors_data)
        
        # Initialise the return list
        data_list = [{
            'titles' : [],
            'count' : [],
            'unique' : [],
            'mean' : [],
            'std' : [],
            'min' : [],
            '25%' : [],
            'median' : [],
            '75%' : [],
            'max' : [],
            'mode' : []
        }]

        # For each sensor in the list of data
        for sensor in sensors_data:

            # Add sensor name
            data_list[0]['titles'].append(sensor['label'])

            # Add count of data
            data_list[0]['count'].append(len(sensor['data']))
            # print(len(sensor['data']))

            # Calculate unique values
            data_points = [ int(data['y']) for data in sensor['data'] ]
            # print(data_points)
            data_list[0]['unique'].append(num_unique(data_points))

            # Calculate mean
            data_list[0]['mean'].append(mean_val(data_points))
            
            # Calculate 25 percentile
            data_list[0]['25%'].append(quartile_val(data_points, 25))

            # Calculate median
            data_list[0]['median'].append(quartile_val(data_points, 50))

            # Calculate 75 percentile
            data_list[0]['75%'].append(quartile_val(data_points, 75))

            # Calculate max value
            data_list[0]['max'].append(max(data_points))

            # Calculate min value
            data_list[0]['min'].append(min(data_points))

            # Calculate mode value
            data_list[0]['mode'].append(mode_val(data_points))

            # Calculate standard deviation
            data_list[0]['std'].append(std_val(data_points))

        print(data_list)
        
        return JsonResponse(list(data_list) , safe=False)

def getADFT(data):

    data = [3, 4, 4, 5, 6, 7, 6, 6, 7, 8, 9, 12, 10]

    print(adfuller(data))