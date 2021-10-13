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
});

// Generate graph
function generate_graph(){


    var from = document.getElementById('from_time').value;
    var to = document.getElementById('to_time').value;
    var list = document.getElementById('selection').options;

    if(!from || !to || !list.length)
    {
        console.log("Invalid Selection !");
    }
    else
    {
        // String to js Date
        fr = new Date(from);

        // Converting to mysql format
        mys = fr.toISOString().split('T')[0] + ' ' + fr.toTimeString().split(' ')[0];

        console.log(fr);
        console.log(mys);
        console.log(typeof fr);
    }

    
}