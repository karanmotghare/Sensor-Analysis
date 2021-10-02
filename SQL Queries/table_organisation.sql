-- Define database
use sensor_analysis;

-- Drop table if already exists
drop table if exists organisation;

-- Create table
create table organisation (
	org_id int not null,
	org_name varchar(255) not null,
    address varchar(255) not null,
    constraint organisation_pkey primary key (org_id)
)
