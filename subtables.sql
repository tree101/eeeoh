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
DROP TABLE  IF EXISTS  storage;
DROP TABLE  IF EXISTS  box_name;

-- drop tables 
DROP TABLE  IF EXISTS  subject;
-- CREATE EXTENSION "uuid-ossp";
DROP TABLE  IF EXISTS  version;
DROP TABLE  IF EXISTS  sample;


-----------------------------------------------------------------------
--- consent table 
--- so far there are only two 
--- Universal and Personalized


CREATE TABLE consent(
id SERIAL PRIMARY KEY, 
form VARCHAR NOT NULL, 
notes VARCHAR
);

-----------------------------------------------------------------------
--- any type of unit you want here 

CREATE TABLE unit(
id SERIAL PRIMARY KEY, 
unit VARCHAR NOT NULL, 
notes VARCHAR
);


CREATE TABLE subtype(
id SERIAL PRIMARY KEY, 
subtype VARCHAR NOT NULL, --
notes VARCHAR
);

CREATE TABLE type(
id SERIAL PRIMARY KEY, 
tissue VARCHAR NOT NULL, -- tissue, molecular, etc
subtype INT NOT NULL REFERENCES  subtype(id), -- FK subtype tissue: Lung, Kidney, Blood, etc  molecular: RNA, DNA, Protein
notes VARCHAR
);


-----------------------------------------------------------------------
--- action table defines what the user did 


CREATE TABLE action(
id SERIAL PRIMARY KEY, 
action VARCHAR NOT NULL, -- so far we have modify, create, withdraw, add, transfer, end
notes VARCHAR 
);

--- users, there will be a script that generates new users with permission level 
--- login will store as cookie and entries will automatically use that username by default
CREATE TABLE users(
id uuid NOT NULL DEFAULT uuid_generate_v4(), 
dateadded  TIMESTAMP(2) DEFAULT (now() at time zone 'PST'), -- date added to database
permission INT NOT NULL DEFAULT (0), -- default read only, 1, 2, 3 will have different permission levels
notes VARCHAR
);

--- create a location of collection 
--- location where sample was processed 



CREATE TABLE location_collection(
id SERIAL PRIMARY KEY, 
location_collection VARCHAR NOT NULL, --  eg SIM1, Stanford Hospital, etc
room VARCHAR,
notes VARCHAR
);


--- predefined strorage location 
-- subtable for storage 

CREATE TABLE box_name(
id SERIAL PRIMARY KEY, 
name VARCHAR NOT NULL,
notes VARCHAR 
);

CREATE TABLE storage(
id SERIAL PRIMARY KEY, 
building VARCHAR NOT NULL, 
room VARCHAR NOT NULL,
storage_name VARCHAR NOT NULL, -- eg -80b, -20a, 4a
shelf VARCHAR, -- 
box INT REFERENCES box_name(id), -- FK box_name  
notes VARCHAR
);

