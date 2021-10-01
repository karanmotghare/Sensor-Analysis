-- Define database
use sensor_analysis;

-- Drop table if already exists
drop table if exists super_admins;

-- Create table
create table super_admins (
	username varchar(255) not null,
    pwd varchar(255) not null,
    constraint users_pkey primary key (username)
)