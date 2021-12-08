let to_drop = false;
function myFunction() {
    console.log("myfunction function called");
    x = document.getElementById('container');

    x.classList.toggle("change");

}

function drop() {


    console.log("drop function called");
    let droplist = document.getElementById('options');

    if (!to_drop) {
        to_drop = true;
        droplist.style.visibility = 'visible';
    }
    else {
        to_drop = false;
        droplist.style.visibility = 'hidden';
    }
}


// Functions to facilitate graph attributes selection on homepage

function change_location(){
    console.log("Location value changed");

    // Get id of selected location
    var x = document.getElementById('location_list');
    var id = x.value;

    $.ajax({
        type: "POST",
        url: 'getSgAjax',
        data: {
            'location_id' : id,
            'csrfmiddlewaretoken': '{{ csrf_token }}',
        },

        success: function(sg){
            let html_data = '<option value="" disabled selected>Select Sensor group</option>';
            sg.forEach(function (sg) {
                html_data += `<option id="sgrp_id" value="${sg.sg_id}">${sg.sg_name}</option>`
            });

            var sengrp = document.getElementById('sngrp_list');
            sengrp.innerHTML = html_data;
            change_sg();
        }
    });

}

function change_sg(){
    console.log("Sensor Group value changed");

    // Get id of selected location
    var x = document.getElementById('sngrp_list');
    var id = x.value;

    $.ajax({
        type: "POST",
        url: 'getSensorAjax',
        data: {
            'sg_id' : id,
            'csrfmiddlewaretoken': '{{ csrf_token }}',
        },

        success: function(sensor){
            let html_data = '<option value="" disabled selected>Select Sensor</option>';
            sensor.forEach(function (sensor) {
                html_data += `<option id="sns_id" value="${sensor.sensor_id}">${sensor.sensor_name}</option>`
            });

            var sen = document.getElementById('sns_list');
            sen.innerHTML = html_data;
        }
    });
}

// Function to add sensor to compare on homepage
function already_exists(val){
    var arr = document.getElementById('selection').options;
    
    val = JSON.stringify(val.join());

    for(var i=0; i<arr.length; i++)
    {
        var op = JSON.stringify(arr[i].value);
        
        if(op == val)
        {
            // Already exists
            return true;
        }
    }

    return false;
}

function add_to_compare(){
    var loc = document.getElementById('location_list');
    var loc_id = loc.value;
    var loc_name = loc.options[loc.selectedIndex].text;

    var sg = document.getElementById('sngrp_list');
    var sg_id = sg.value;
    var sg_name = sg.options[sg.selectedIndex].text;

    var sensor = document.getElementById('sns_list');
    var sensor_id = sensor.value;
    var sensor_name = sensor.options[sensor.selectedIndex].text;

    var val = new Array(loc_id, sg_id, sensor_id);

    var present = already_exists(val);

    console.log(val);

    if(!loc_id || !sg_id || !sensor_id)
    {
        console.log("Invalid sensor selection");
        var err = document.getElementById('err_msg');
        err.innerHTML = '<p>Invalid Selection !</p>';
    }
    else if(present)
    {
        console.log("Already present");
        var err = document.getElementById('err_msg');
        err.innerHTML = '<p>Selection Already Exists !</p>';
    }
    else 
    {
        console.log("Valid Selection");
        var err = document.getElementById('err_msg');
        err.innerHTML = '';

        selected = document.getElementById('selection');
        selected_data = selected.innerHTML;
        selected_data += `<option value="${val}">${loc_name} / ${sg_name} / ${sensor_name}</option>`;
        selected.innerHTML = selected_data;
    }
}

// Function to remove sensor from selected list
function remove_from_list(){

    var opt = document.getElementById('selection');
    var is_selected = [];

    for(var i=0; i<opt.options.length; i++)
    {
        is_selected[i] = opt.options[i].selected;
    }

    // Remove from bottom up
    for(var i=opt.options.length-1; i>=0; i--)
    {
        if(opt.options[i].selected)
        {
            opt.remove(i);
        }
    }
}

// Date time picker
$(function () {
    $('#datetimepicker6').datetimepicker();
    $('#datetimepicker7').datetimepicker({
        useCurrent: false
    });
    $("#datetimepicker6").on("dp.change", function (e) {
        $('#datetimepicker7').data("DateTimePicker").minDate(e.date);
    });
    $("#datetimepicker7").on("dp.change", function (e) {
        $('#datetimepicker6').data("DateTimePicker").maxDate(e.date);
    });
    $('#datetimepicker8').datetimepicker();

});

// Generate graph
function generate_graph(){


    var from_time = document.getElementById('from_time').value;
    var to_time = document.getElementById('to_time').value;
    var list = document.getElementById('selection').options;
    console.log(list);

    if(!from_time || !to_time || !list.length)
    {
        console.log("Invalid Selection !");
    }
    else
    {
        // String to js Date
        console.log("From time ",from_time);
        from = new Date(from_time);
        to = new Date(to_time);
        console.log("From entry ");
        console.log(from[0]);

        // Converting to mysql format
        from_mysql = moment(from).format('YYYY-MM-DD HH:mm:ss');
        to_mysql = moment(to).format('YYYY-MM-DD HH:mm:ss');

        console.log(from, to);
        console.log(from_mysql, to_mysql);
        //console.log(typeof fr);

        // Get data from db using ajax
        data = new Array(list.length);
        for(var i=0; i<list.length; i++)
        {
            data[i] = list[i].value
            //data[i] = (list[i].value).split(",").map(Number);
        }

        data_list = {"data" : data}

        console.log(JSON.stringify(data_list));
        
        $.ajax({
            type: "POST",
            url: 'getDataValues',
            data: {
                'sensors' : JSON.stringify(data_list),
                'from_time' : from_mysql,
                'to_time' : to_mysql,
                'csrfmiddlewaretoken': '{{ csrf_token }}',
            },

            success: function(sensors_data){
                console.log(sensors_data);
                var newWindow = window.open('chartJS');
                
                localStorage.setItem('sensors_data', JSON.stringify(sensors_data));
    
            }

        })
        
    }

    
}

// Generate random colour
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Display Graph
function displayGraph(){
    console.log("New window opened");
    sensors_data = JSON.parse(localStorage.getItem('sensors_data'));
    console.log(sensors_data);

    var dataset = [];

    // For every sensor
    for(var i=0; i<sensors_data.length; i++)
    {
        console.log(sensors_data[i]);
        console.log(sensors_data[i]['label']);

        var data = [];

        // For every date-value pair for that sensor
        for(var j=0; j<sensors_data[i]['data'].length; j++)
        {
            var val = {
                    x : sensors_data[i]['data'][j]['x'],
                    y : sensors_data[i]['data'][j]['y']
                };
            
            data.push(val);
        };

        var obj = {
            label: sensors_data[i]['label'],
            borderColor: getRandomColor(),
            fill: false,
            tension: 0,
            data: data
        };

        dataset.push(obj);

    }
      
    var ctx = document.getElementById('new_chart').getContext('2d');
    console.log(ctx)
    var chart = new Chart(ctx, {
        type: 'line',
        data: { datasets: dataset },
        options: {
            scales: {
            xAxes: [{
                type: 'time'
            }]
            },
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Chart.js Line Chart'
                }
            }
        }
    });

    // Calculate statistics for displayed graph
    $.ajax({
        type: "POST",
        url: 'getStatistics',
        data: {
            'sensors_data' : localStorage.getItem('sensors_data'),
            'csrfmiddlewaretoken': '{{ csrf_token }}',
        },

        success: function(table){
            console.log("Statistics calculated");
            // console.log(typeof table)
            // table = JSON.parse(table_data);
            titles = Object.keys(table[0])
            // console.log(Object.keys(table[0]));

            // Create table in html
            let html_data = '';

            // let i = 0;

            for(row in table[0]){
                html_data += '<tr>'
                console.log(row);
                html_data += `<th>${row}</th>`
                // console.log(table[0][row]);
                for (col in table[0][row]){
                    console.log(table[0][row][col]);
                    html_data += `<td>${table[0][row][col]}</td>`
                }
                html_data += '</tr>'
            }

            // sg.forEach(function (sg) {
                // html_data += `<option id="sgrp_id" value="${sg.sg_id}">${sg.sg_name}</option>`
            // });

            var sengrp = document.getElementById('stats');
            // console.log(sengrp.innerHTML)
            sengrp.innerHTML = html_data;
            
        }
    });


    // console.log(JSON.parse(sensors_data));
}

// DATA GENERATION FUNCTIONS

// Dynamic rendering of divs 
function change_gen_type(){
    
    // Get value of selected type
    var x = document.getElementById('gen_type');
    var type = x.value;

    if(type=='type_1'){
        var option_1 = document.getElementById('option1');
        var option_2 = document.getElementById('option2');

        option_1.style.display = 'block';
        option_2.style.display = 'none';
    }
    else if(type=='type_2'){
        var option_1 = document.getElementById('option1');
        var option_2 = document.getElementById('option2');

        option_1.style.display = 'none';
        option_2.style.display = 'block';
    }
}

// Option 1 : Enter values for a selected time interval
function option_1_add_data(){
    var loc = document.getElementById('location_list');
    var loc_id = loc.value;
    var loc_name = loc.options[loc.selectedIndex].text;

    var sg = document.getElementById('sngrp_list');
    var sg_id = sg.value;
    var sg_name = sg.options[sg.selectedIndex].text;

    var sensor = document.getElementById('sns_list');
    var sensor_id = sensor.value;
    var sensor_name = sensor.options[sensor.selectedIndex].text;

    var data_point = document.getElementById('data_1')
    var data = document.getElementById('data_1').value;

    var val = new Array(loc_id, sg_id, sensor_id, data);

    // var present = already_exists(val);

    console.log(val);

    if(!loc_id || !sg_id || !sensor_id || !data)
    {
        console.log("Invalid sensor selection");
        var err = document.getElementById('err_msg');
        err.innerHTML = '<p>Invalid Selection !</p>';
    }
    // else if(present)
    // {
    //     console.log("Already present");
    //     var err = document.getElementById('err_msg');
    //     err.innerHTML = '<p>Selection Already Exists !</p>';
    // }
    else 
    {
        console.log("Valid Selection");
        var err = document.getElementById('err_msg');
        err.innerHTML = '';

        selected = document.getElementById('selection_1');
        selected_data = selected.innerHTML;
        selected_data += `<option value="${val}">${loc_name} / ${sg_name} / ${sensor_name} / ${data} </option>`;
        selected.innerHTML = selected_data;
    }

    // Clear the text box
    data_point.value = ""
}

function option_1_remove_from_list(){
    var opt = document.getElementById('selection_1');
    var is_selected = [];

    for(var i=0; i<opt.options.length; i++)
    {
        is_selected[i] = opt.options[i].selected;
    }

    // Remove from bottom up
    for(var i=opt.options.length-1; i>=0; i--)
    {
        if(opt.options[i].selected)
        {
            opt.remove(i);
        }
    }
}

function option_1_generate_graph(){
    var from_time = document.getElementById('from_time').value;
    var to_time = document.getElementById('to_time').value;
    var list = document.getElementById('selection_1').options;
    console.log(list);

    if(!from_time || !to_time || (list.length<2))
    {
        console.log("Invalid Selection !");
    }
    else
    {
        // String to js Date
        console.log("From time ",from_time);
        from = new Date(from_time);
        to = new Date(to_time);
        console.log("From entry ");
        console.log(from[0]);

        // Converting to mysql format
        from_mysql = moment(from).format('YYYY-MM-DD HH:mm:ss');
        to_mysql = moment(to).format('YYYY-MM-DD HH:mm:ss');

        console.log(from, to);
        console.log(from_mysql, to_mysql);
        //console.log(typeof fr);

        // Get data from db using ajax
        data = new Array(list.length);
        for(var i=0; i<list.length; i++)
        {
            data[i] = list[i].value
            //data[i] = (list[i].value).split(",").map(Number);
        }

        data_list = {"data" : data}

        console.log(JSON.stringify(data_list));
    
        $.ajax({
            type: "POST",
            url: 'option_1_graph',
            data: {
                'sensors' : JSON.stringify(data_list),
                'from_time' : from_mysql,
                'to_time' : to_mysql,
                'csrfmiddlewaretoken': '{{ csrf_token }}',
            },

            success: function(sensors_data){
                console.log(sensors_data);
                var newWindow = window.open('chartJS');
                
                localStorage.setItem('sensors_data', JSON.stringify(sensors_data));
                
            }

        })
        
    }
}

// Save the graph in database
function option_1_insert_db(){
    var from_time = document.getElementById('from_time').value;
    var to_time = document.getElementById('to_time').value;
    var list = document.getElementById('selection_1').options;
    console.log(list);

    if(!from_time || !to_time || (list.length<2))
    {
        console.log("Invalid Selection !");
        status_box = document.getElementById('status_box');
        // selected_data = status_box.innerHTML;
        selected_data = `Enter all Parameters`;
        status_box.innerHTML = selected_data;
    }
    else
    {
        // String to js Date
        console.log("From time ",from_time);
        from = new Date(from_time);
        to = new Date(to_time);
        console.log("From entry ");
        console.log(from[0]);

        // Converting to mysql format
        from_mysql = moment(from).format('YYYY-MM-DD HH:mm:ss');
        to_mysql = moment(to).format('YYYY-MM-DD HH:mm:ss');

        console.log(from, to);
        console.log(from_mysql, to_mysql);
        //console.log(typeof fr);

        // Get data from db using ajax
        data = new Array(list.length);
        for(var i=0; i<list.length; i++)
        {
            data[i] = list[i].value
            //data[i] = (list[i].value).split(",").map(Number);
        }

        data_list = {"data" : data}

        console.log(JSON.stringify(data_list));
    
        $.ajax({
            type: "POST",
            url: 'option_1_insert_db',
            data: {
                'sensors' : JSON.stringify(data_list),
                'from_time' : from_mysql,
                'to_time' : to_mysql,
                'csrfmiddlewaretoken': '{{ csrf_token }}',
            },

            success: function(version){
                console.log("Saved as : ", version);
                
                status_box = document.getElementById('status_box');
                // selected_data = status_box.innerHTML;
                selected_data = `Data saved as Version Number : <b>${version}</b>`;
                status_box.innerHTML = selected_data;
            }

        })
        
    }
}

// Option 2 : Enter values for a value for given time
function already_exists_2(val){
    var arr = document.getElementById('selection_2').options;
    console.log(val);
    // val = JSON.stringify(val.join());

    for(var i=0; i<arr.length; i++)
    {
        var op = (arr[i].value).split(',');
        console.log(op);
        if(op[4] == val[4])
        {
            // Already exists
            return true;
        }
    }

    return false;
}

function option_2_add_data(){
    var loc = document.getElementById('location_list');
    var loc_id = loc.value;
    var loc_name = loc.options[loc.selectedIndex].text;

    var sg = document.getElementById('sngrp_list');
    var sg_id = sg.value;
    var sg_name = sg.options[sg.selectedIndex].text;

    var sensor = document.getElementById('sns_list');
    var sensor_id = sensor.value;
    var sensor_name = sensor.options[sensor.selectedIndex].text;

    var data_point = document.getElementById('data_2')
    var data = document.getElementById('data_2').value;

    var raw_time = document.getElementById('time').value;
    var time = moment(new Date(raw_time)).format('YYYY-MM-DD HH:mm:ss');

    var val = new Array(loc_id, sg_id, sensor_id, data, time);

    var present = already_exists_2(val);

    console.log(val);

    if(!loc_id || !sg_id || !sensor_id || !data || !time)
    {
        console.log("Invalid sensor selection");
        var err = document.getElementById('err_msg_2');
        err.innerHTML = '<p>Invalid Selection !</p>';
    }
    else if(present)
    {
        console.log("Already present");
        var err = document.getElementById('err_msg_2');
        err.innerHTML = '<p>Selection Already Exists !</p>';
    }
    else 
    {
        console.log("Valid Selection");
        var err = document.getElementById('err_msg_2');
        err.innerHTML = '';

        selected = document.getElementById('selection_2');
        selected_data = selected.innerHTML;
        selected_data += `<option value="${val}">${loc_name} / ${sg_name} / ${sensor_name} / ${data} / ${time} </option>`;
        selected.innerHTML = selected_data;
    }

    // Clear the text box
    data_point.value = ""
}

function option_2_remove_from_list(){
    var opt = document.getElementById('selection_2');
    var is_selected = [];

    for(var i=0; i<opt.options.length; i++)
    {
        is_selected[i] = opt.options[i].selected;
    }

    // Remove from bottom up
    for(var i=opt.options.length-1; i>=0; i--)
    {
        if(opt.options[i].selected)
        {
            opt.remove(i);
        }
    }
}

function option_2_generate_graph(){
    // var from_time = document.getElementById('from_time').value;
    // var to_time = document.getElementById('to_time').value;
    var list = document.getElementById('selection_2').options;
    console.log(list);

    if(list.length<2)
    {
        console.log("Invalid Selection !");
    }
    else
    {
        // Get data from db using ajax
        data = new Array(list.length);
        for(var i=0; i<list.length; i++)
        {
            data[i] = list[i].value
            //data[i] = (list[i].value).split(",").map(Number);
        }

        data_list = {"data" : data}

        console.log(JSON.stringify(data_list));
    
        $.ajax({
            type: "POST",
            url: 'option_2_graph',
            data: {
                'sensors' : JSON.stringify(data_list),
                // 'from_time' : from_mysql,
                // 'to_time' : to_mysql,
                'csrfmiddlewaretoken': '{{ csrf_token }}',
            },

            success: function(sensors_data){
                console.log(sensors_data);
                var newWindow = window.open('chartJS');
                
                localStorage.setItem('sensors_data', JSON.stringify(sensors_data));
                
            }

        })
        
    }
}

function option_2_insert_db(){
    var list = document.getElementById('selection_2').options;
    console.log(list);

    if(list.length<2)
    {
        console.log("Invalid Selection !");
        status_box = document.getElementById('status_box');
        // selected_data = status_box.innerHTML;
        selected_data = `Enter all Parameters`;
        status_box.innerHTML = selected_data;
    }
    else
    {
        // Get data from db using ajax
        data = new Array(list.length);
        for(var i=0; i<list.length; i++)
        {
            data[i] = list[i].value
            //data[i] = (list[i].value).split(",").map(Number);
        }

        data_list = {"data" : data}

        console.log(JSON.stringify(data_list));
    
        $.ajax({
            type: "POST",
            url: 'option_2_insert_db',
            data: {
                'sensors' : JSON.stringify(data_list),
                'csrfmiddlewaretoken': '{{ csrf_token }}',
            },

            success: function(version){

                console.log("Saved as : ", version);

                status_box = document.getElementById('status_box');
                // selected_data = status_box.innerHTML;
                selected_data = `Data saved as Version Number : <b>${version}</b>`;
                status_box.innerHTML = selected_data;
                
            }

        })
        
    }
}

function get_ADFT(){
    console.log("Function called...");

    $.ajax({
        type: "POST",
        url: 'getADFT',
        data: {
            // 'sensors' : JSON.stringify(data_list),
            'csrfmiddlewaretoken': '{{ csrf_token }}',
        },

        success: function(result){

            // console.log("Saved as : ", version);

            console.log(result);
            console.log(typeof result);
            console.log(result[1]);

            verdict = "Non-Stationary Series";
            if(result[1]<=0.05){
                verdict = "Stationary Series";
            }

            status_box = document.getElementById('ADFT_box');
            // // selected_data = status_box.innerHTML;
            selected_data = `p-value : <b>${result[1]}</b><br/>`;
            selected_data += `Verdict : <b>${verdict}</b>`;
            status_box.innerHTML = selected_data;
            
        }

    })
}