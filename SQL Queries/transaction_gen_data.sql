-- Define database
use sensor_analysis;

-- Drop table if already exists
drop table if exists sensor_gen_data;

-- Create table
create table sensor_gen_data (
	record_id int not null auto_increment,
	sensor_id int not null,
    version_id int not null,
    from_data float not null,
    to_data float not null,
    from_time timestamp,
    to_time timestamp,
    constraint gen_data_pkey primary key (record_id),
    constraint gen_data_sensor_fkey foreign key (sensor_id) references sensor(sensor_id)
)