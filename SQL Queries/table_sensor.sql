-- Define database
use sensor_analysis;

-- Drop table if already exists
drop table if exists sensor;

-- Create table
create table sensor (
	sensor_id int not null,
	sensor_name varchar(255) not null,
	sg_id int not null,
    constraint sensor_pkey primary key (sensor_id),
    constraint sensor_sg_fkey foreign key (sg_id) references sensor_group(sg_id)
)