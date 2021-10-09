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
                html_data += `<option value="${sg.sg_id}">${sg.sg_name}</option>`
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
                html_data += `<option value="${sensor.sensor_id}">${sensor.sensor_name}</option>`
            });

            var sen = document.getElementById('sns_list');
            sen.innerHTML = html_data;
        }
    });
}