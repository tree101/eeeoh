--- three main tables
--- subject
--- sample
--- version 


------- comments
--- version table stores id and referencing table, with a JSON type to store fields
--- unique to the old record


DROP TABLE  IF EXISTS  subject;
-- CREATE EXTENSION "uuid-ossp";
DROP TABLE  IF EXISTS  version;
DROP TABLE  IF EXISTS  sample;



CREATE TABLE subject(
id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(), 
users VARCHAR NOT NULL, --from current user (store in cookie on login)
age INT,
sex INT, -- male, female, na
consent INT NOT NULL REFERENCES  consent(id),  -- FK from conset table
date_create DATE NOT NULL,
date_modify date, -- this date is the most current version date
version INT, -- inserts latest version but keeps a record in table "version"
action INT REFERENCES action (id), -- FK table action
notes VARCHAR
);


--____________________________________________________________________________________
---- combined sample tables will consist of generic fields but contain a JSON field 
---- specific to any sort of data 
---- versions and log stored in table version


CREATE TABLE sample(
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(), -- PK
    id_subject INT NOT NULL REFERENCES  subject(id), -- FK from subject 
    
	tissue_type INT NOT NULL REFERENCES  type(id), -- FK from type
	sub_type INT NOT NULL REFERENCES  subtype(id), -- FK from subtype
	
    date_create date NOT NULL,
	date_modify date, -- this date is the most current version date
					  -- before insertion script will search through version of the latest, if not found then its version 1		
	
    location_collection INT NOT NULL REFERENCES  location_collection(id), -- FK from table location_collection
    
    users INT NOT NULL, -- from cookie
    amount double precision NOT NULL, 
	unit INT NOT NULL, --- FK from units
	location_storage INT NOT NULL REFERENCES  storage(id), -- FK from storage
    

    date_modify date, -- current entry date
    
	version INT, -- inserts latest version but keeps a record in table "version"
    action INT REFERENCES action (id), -- FK table action

	data JSON, -- stores  data unique to entry
    notes VARCHAR	
	-- for example, for tissue collection could include orientation, quality, 
	);
	
	
--____________________________________________________________________________________

----- create version table now
----- this will log version and a JSON field containing older entries
----- this version table is not dependent on calling table because it will store all the older fields in a JSON type

CREATE TABLE version(
calling_table VARCHAR, -- name of calling table
id uuid NOT NULL, -- primary id of calling table
version_number SERIAL NOT NULL
action INT, -- action from calling table
users INT, -- from current user (store in cookie on login)
timestamp TIMESTAMP(2), -- when triggered
data_log JSON, -- stores all data associated with older entry Not dependent on table
notes VARCHAR
);




