--_____________________________________________________________________________________________________________
--- sub-tables

-- drop tables 
DROP TABLE  IF EXISTS  subject CASCADE;
-- CREATE EXTENSION "uuid-ossp";
DROP TABLE  IF EXISTS  version CASCADE;
DROP TABLE  IF EXISTS  sample CASCADE;


DROP TABLE  IF EXISTS  type;
DROP TABLE  IF EXISTS  subtype;
DROP TABLE  IF EXISTS  consent;
DROP TABLE  IF EXISTS  unit;
DROP TABLE  IF EXISTS  action;
DROP TABLE  IF EXISTS  users;
DROP TABLE  IF EXISTS  location_collection;




DROP TABLE  IF EXISTS  storage CASCADE;
DROP TABLE  IF EXISTS  institution;
DROP TABLE  IF EXISTS  building;
DROP TABLE  IF EXISTS  room;
DROP TABLE  IF EXISTS  storageUnit;
DROP TABLE  IF EXISTS shelf;
DROP TABLE  IF EXISTS box;
DROP TABLE  IF EXISTS position;
					   
DROP TABLE  IF EXISTS  parentID CASCADE; 



-----------------------------------------------------------------------
-- project table
CREATE TABLE projects(
id SERIAL PRIMARY KEY, 
name VARCHAR NOT NULL,
groupName VARCHAR, 
notes TEXT 

)

-----------------------------------------------------------------------
--- consent table 
--- so far there are only two 
--- Universal and Personalized


CREATE TABLE consent(
id SERIAL PRIMARY KEY, 
form VARCHAR NOT NULL, 
link VARCHAR, -- this could be a hyperlink of some sort to the actual document
notes TEXT
);

CREATE TABLE consentj(
id SERIAL PRIMARY KEY, 
consent_id INT NOT NULL REFERENCES consent(id), 
sample_id uuid NOT NULL,
notes TEXT
);




-----------------------------------------------------------------------
--- any type of unit you want here 

CREATE TABLE unit(
id SERIAL PRIMARY KEY, 
unit VARCHAR NOT NULL, 
notes TEXT
);


CREATE TABLE subtype(
id SERIAL PRIMARY KEY, 
subtype VARCHAR NOT NULL, --
notes TEXT
);

CREATE TABLE sample_type(
id SERIAL PRIMARY KEY, 
tissue VARCHAR NOT NULL, -- tissue, molecular, etc
subtype INT NOT NULL REFERENCES  subtype(id), -- FK subtype tissue: Lung, Kidney, Blood, etc  molecular: RNA, DNA, Protein
notes TEXT
);


-----------------------------------------------------------------------
--- action table defines what the user did 


CREATE TABLE action(
id SERIAL PRIMARY KEY, 
action VARCHAR NOT NULL, -- so far we have modify, create, withdraw, add, transfer, end
notes TEXT 
);

--- users, there will be a script that generates new users with permission level 
--- login will store as cookie and entries will automatically use that username by default
CREATE TABLE users(
id uuid NOT NULL DEFAULT uuid_generate_v4(), 
dateadded  TIMESTAMP(2) DEFAULT (now() at time zone 'PST'), -- date added to database
permission INT NOT NULL DEFAULT (0), -- default read only, 1, 2, 3 will have different permission levels
notes TEXT
);

--- create a location of collection 
--- location where sample was processed 



CREATE TABLE location_collection(
id SERIAL PRIMARY KEY, 
location_collection VARCHAR NOT NULL, --  eg SIM1, Stanford Hospital, etc
room VARCHAR,
notes TEXT
);


---  
-- subtable for storage 
-
-- each box should have a name or serial number

CREATE TABLE institution(
id SERIAL PRIMARY KEY, 
name VARCHAR NOT NULL,
notes TEXT 
);

CREATE TABLE building(
id SERIAL PRIMARY KEY, 
name VARCHAR NOT NULL,
notes TEXT 
);

CREATE TABLE room(
id SERIAL PRIMARY KEY, 
name VARCHAR NOT NULL,
notes TEXT 
);

-- this table is to name your storage type, eg -80
CREATE TABLE storageUnit(
id SERIAL PRIMARY KEY, 
name VARCHAR NOT NULL,
notes TEXT 
);

-- may or may not have it
CREATE TABLE shelf(
id SERIAL PRIMARY KEY, 
name VARCHAR NOT NULL,
notes TEXT 
);

-- samples may or may not be in a box
CREATE TABLE box(
id SERIAL PRIMARY KEY, 
name VARCHAR NOT NULL,
notes TEXT 
);

-- position really depends on what the intended storage is. 
CREATE TABLE position(
id SERIAL PRIMARY KEY, 
name VARCHAR NOT NULL,
notes TEXT 
);


CREATE TABLE storage(
id SERIAL PRIMARY KEY, 
institution_name INT REFERENCES NOT NULL institution(id),
building_name INT REFERENCES NOT NULL building(id), 
room_name INT REFERENCES room(id),
storageUnit_name INT REFERENCES storageUnit(id),
shelf_name INT REFERENCES shelf(id),  
box_name INT REFERENCES box(id),   
notes TEXT
);

