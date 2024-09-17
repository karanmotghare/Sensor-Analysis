-- Define database
use sensor_analysis;

-- Drop table if already exists
drop table if exists users;

-- Create table
create table users (
	username varchar(255) not null,
    pwd varchar(255) not null,
    position enum('org_admin', 'loc_admin', 'user') not null,
    org_id int default null,
    created_by varchar(255) not null,
    loc_id int default null,
    constraint users_pkey primary key (username),
    constraint users_loc_fkey foreign key (loc_id) references location(loc_id),
    constraint users_org_fkey foreign key (org_id) references organisation(org_id)
)


