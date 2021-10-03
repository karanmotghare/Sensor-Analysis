-- Define database
use sensor_analysis;

-- Drop table if already exists
drop table if exists sensor_actual_data;

-- Create table
create table sensor_actual_data (
	record_id int not null auto_increment,
	sensor_id int not null,
    data_value float not null,
    record_time timestamp, 
    constraint actual_data_pkey primary key (record_id),
    constraint actual_data_sensor_fkey foreign key (sensor_id) references sensor(sensor_id)
)