from operator import ne
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
from scipy.stats import pearsonr
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
        user_loc = (user[0].loc)     

        # Location list
        if user[0].position=="org_admin":
            locations = Location.objects.filter(org=org)

        else:
            locations = Location.objects.filter(loc_id=user_loc.loc_id)

        

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

# Function to load sensors
@csrf_exempt
def getVersionsAjax(request):

    if request.method == "POST":
        sns_id = request.POST['sns_id']
        latest_v = 0

        try:
            if sns_id:
                sensor = Sensor.objects.filter(sg_id = sns_id).first()
                # Get the latest saved version in the database
                versions = SensorGenData.objects.filter(sensor = sensor)

                ver = versions.aggregate(Max('version_id'))
    
                if ver['version_id__max']:
                    latest_v = ver['version_id__max']
                
            else:
                sensors = Sensor.objects.none()
        except Exception:
            request.data['error_message'] = 'error'
            return JsonResponse(request.data)
        return JsonResponse(latest_v, safe = False) 


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

@csrf_exempt
def getVersionData(request):

    if request.method == "POST":
        sensors_list = (json.loads(request.POST['sensors']))["data"]
        
        data_list = []
        
        try:
            if sensors_list:
                
                # Get data for every sensor
                for sensor in sensors_list:
                    
                    val = sensor.split(',')
                    sns = Sensor.objects.filter(sensor_id = val[2])
                    version = int(val[3])
                    data = SensorGenData.objects.filter(sensor = sns[0], version_id = version)

                    lst = []

                    value = {
                            'x' : (data[0].from_time).strftime('%Y-%m-%d %H:%M:%S'),
                            'y' : data[0].from_data
                        }
                    
                    lst.append(value)

                    for point in data:
                        value = {
                            'x' : (point.to_time).strftime('%Y-%m-%d %H:%M:%S'),
                            'y' : point.to_data
                        }

                        lst.append(value)

                    obj = {
                        'label' : sns[0].sensor_name + " " + str(version),
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
        user_loc = (user[0].loc)     

        # Location list
        if user[0].position=="org_admin":
            locations = Location.objects.filter(org=org)

        else:
            locations = Location.objects.filter(loc_id=user_loc.loc_id)

        print("Location id of user is :" , user_loc.loc_name)

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

    # Get the latest saved version in the database
    versions = SensorGenData.objects.filter(sensor = sensor)
    latest_v = 0

    ver = versions.aggregate(Max('version_id'))
    
    if ver['version_id__max']:
        latest_v = ver['version_id__max']
    
    current = latest_v + 1

    # Saving each row
    for i in range(len(data) - 1):

        try:
            row = SensorGenData(sensor=sensor, version_id=current, from_data=data[i]['y'], to_data=data[i+1]['y'], from_time=data[i]['x'], to_time=data[i+1]['x'])
            row.save()
        except Exception:
            print(Exception)
            return current



    return current

# Function to redirect to saved data page
def savedData(request):
    if 'user' in request.session:
        #print(request.session['user'])

        user = Users.objects.filter(username=request.session['user']) 
        org = user[0].org 
        user_loc = (user[0].loc)     

        # Location list
        if user[0].position=="org_admin":
            locations = Location.objects.filter(org=org)

        else:
            locations = Location.objects.filter(loc_id=user_loc.loc_id)

        print("Location id of user is :" , user_loc.loc_name)

        mapper={
            'locations':locations,
            'heading':'Data Retrieval Portal',
            'display':'block'
        }
        return render(request,'savedData.html',mapper)
    else:
        return HttpResponseRedirect("/")


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


# Function to create user generated graph for option 3
@csrf_exempt
def option_3_graph(request):

    if request.method=="POST":
        sensors_data = (json.loads(request.POST['values']))["data"]
        timestamps = (json.loads(request.POST['timestamp']))["data"]
        name = request.POST["name"]

        # Initialise the return list
        data_list = []

        try:
            if sensors_data:

                # Create data points with corresponding time
                lst = []

                for i in range(len(sensors_data)):
                    time = datetime.strptime(timestamps[i], '%Y-%m-%d %H:%M:%S')
                    value = {
                        'x' : time.strftime('%Y-%m-%d %H:%M:%S'),
                        'y' : sensors_data[i]
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
def option_3_insert_db(request):
    if request.method=="POST":
        sensors_data = (json.loads(request.POST['values']))["data"]
        timestamps = (json.loads(request.POST['timestamp']))["data"]
        name = request.POST["name"]
        sensor_id = int(request.POST["id"])

        # Initialise the return list
        data_list = []

        try:
            if sensors_data:

                sensor = Sensor.objects.filter(sensor_id = sensor_id)
                # Create data points with corresponding time
                lst = []

                for i in range(len(sensors_data)):
                    time = datetime.strptime(timestamps[i], '%Y-%m-%d %H:%M:%S')
                    value = {
                        'x' : time.strftime('%Y-%m-%d %H:%M:%S'),
                        'y' : sensors_data[i]
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


# Function to create user generated graph for option 3
@csrf_exempt
def option_4_graph(request):
    if request.method=="POST":
        sensors_data = (json.loads(request.POST['values']))["data"]
        timestamps = (json.loads(request.POST['timestamp']))["data"]
        name = request.POST["name"]

        # Initialise the return list
        data_list = []

        try:
            if sensors_data:

                # Create data points with corresponding time
                lst = []

                for i in range(len(sensors_data)):
                    time = timestamps[i] #datetime.strptime(timestamps[i], '%Y-%m-%d %H:%M:%S')
                    value = {
                        'x' : time,
                        'y' : sensors_data[i]
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

# Function to calculate statistics
def num_unique(data):
    return len(set(data))

def mean_val(data):
    return round(numpy.mean(data), 2)

def quartile_val(data, num):
    return round(numpy.percentile(data, num), 2)

def mode_val(data):
    print((stats.mode(data)).mode[0])
    return int((stats.mode(data)).mode[0])

def std_val(data):
    return round(numpy.std(data), 2)

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
            data_points = [ int(float(data['y'])) for data in sensor['data'] ]
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
        
        # Converting the list to a particular format
        result = [list(data_list[0].keys())]
        
        for i in range(len(sensors_data)):
            new_row = []

            new_row.append(data_list[0]['titles'][i])
            new_row.append(data_list[0]['count'][i])
            new_row.append(data_list[0]['unique'][i])
            new_row.append(data_list[0]['mean'][i])
            new_row.append(data_list[0]['std'][i])
            new_row.append(data_list[0]['min'][i])
            new_row.append(data_list[0]['25%'][i])
            new_row.append(data_list[0]['median'][i])
            new_row.append(data_list[0]['75%'][i])
            new_row.append(data_list[0]['max'][i])
            new_row.append(data_list[0]['mode'][i])
            

            result.append(new_row)

        print(result)

        return JsonResponse(list(result) , safe=False)


@csrf_exempt
def movingAvg(array, count):

    # calculate average for subarray  
    def avg(array):
        sum = 0
        for i in array:
            sum += i
        return int(sum/len(array))

    #calculate average for each subarray
    result = []
    i = 0
    while(i<len(array)):
        val = avg(array[i:i+count])
        i+=count
        result.append(val)

    return result
   
def split_array(arr, window):
    split_arr = []

    i = 0
    while((i+window)<=len(arr)):
        split_arr.append(arr[i:i+window])
        i = i + window

    return split_arr

@csrf_exempt
def getMotifs(request):
    if request.method == "POST":
        sensors_data = json.loads(request.POST['sensors_data']) 
        percent = int(json.loads(request.POST['window']))
        cutoff = float(json.loads(request.POST['cutoff']))
        occur = int(json.loads(request.POST['occur']))
        # percent = int(request.POST["percent"])

        print("Percent : ", percent)

        # Initialise the return list
        data_list = []

        for sensor in sensors_data:
            
            label = sensor['label']
            
            data_points = [ int(float(data['y'])) for data in sensor['data'] ]

            time_points = [ (data['x']) for data in sensor['data'] ]

            window = int(len(data_points)*percent//100)

            # threshold = 3

            split_points = split_array(data_points, window)

            split_time = split_array(time_points, window)

            flag = [0] * len(split_points)

            similar_objs = []
            time_intervals = []
            
            count = 0

            for i in range(0, len(split_points)):

                if not flag[i]:

                    new_list = [i]
                    new_interval = [(split_time[i][0], split_time[i][window-1])]

                    for j in range(i+1, len(split_points)):

                        if not flag[j]:
                            # Pearson's Correlation
                            corr, _ = pearsonr(split_points[i], split_points[j])

                            if corr > cutoff:

                                new_list.append(j)
                                new_interval.append((split_time[j][0], split_time[j][window-1]))
                                # no. of repetitions w.r.t i, points of window i 
                                # similar_objs[i] = j

                                flag[j] = 1

                    if len(new_list)>=occur:
                        similar_objs.append(new_list)
                        time_intervals.append(new_interval)

                    flag[i] = 1


            for i in range(len(similar_objs)):

                window_data = split_points[similar_objs[i][0]]

                # Create data points with corresponding time
                lst = []

                for j in range(1, len(window_data)+1):
                    time = j #datetime.strptime(timestamps[i], '%Y-%m-%d %H:%M:%S')
                    value = {
                        'x' : str(time),
                        'y' : str(window_data[j-1])
                    }

                    lst.append(value)

                obj = {
                    'label' : label + '_' + str(i+1),
                    'data' : lst,
                    'repititions' : len(similar_objs[i]),
                    'intervals' : time_intervals[i]
                }

                data_list.append(obj)

            
        return JsonResponse(list(data_list) , safe=False)



@csrf_exempt
def getADFT(request):

    try:
        sensors_data = (json.loads(request.POST['sensor_data']))["data"]

        # print(type(sensors_data[0]))

        data = [val['y'] for val in sensors_data[0]['data']]
        print(data)
        # data = [3, 4, 4, 5, 6, 7, 6, 6, 7, 8, 9, 12, 10]
        # data_2 = [3,4,3,4,2,4,3,4,3,4,3,4,3,4]
        print(adfuller(data))

    except Exception as e:
        print(e)
        response = JsonResponse(str(e), safe=False)
        response.status_code = 400
        return response

    return JsonResponse(adfuller(data) , safe=False)


# Add/Edit Page render
def add_edit(request):
    mapper={
    'heading':'Organization Hierarchy',

    }
    return render(request,"add_edit.html",mapper)