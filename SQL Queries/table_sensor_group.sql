-- Define database
use sensor_analysis;

-- Drop table if already exists
drop table if exists sensor_group;

-- Create table
create table sensor_group (
	sg_id int not null,
    sg_name varchar(255) not null,
    loc_id int not null,
    constraint sg_pkey primary key (sg_id),
    constraint sg_loc_fkey foreign key (loc_id) references location(loc_id)
)