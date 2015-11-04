
-- uers 
CREATE TYPE usertype AS ENUM ('admin', 'power', 'view', 'other');

DROP TABLE  IF EXISTS  projects CASCADE;
CREATE TABLE projects(
id SERIAL PRIMARY KEY, 
name VARCHAR NOT NULL,
groupName VARCHAR, 
notes TEXT 

);




DROP TABLE  IF EXISTS  userlogin CASCADE;
CREATE TABLE userLogin(
id SERIAL PRIMARY KEY, 
firstname VARCHAR NOT NULL,
lastname VARCHAR NOT NULL, 
email VARCHAR NOT NULL,
password VARCHAR, 
is_admin INT DEFAULT 0,
notes TEXT

);

-- junction table here 
DROP TABLE  IF EXISTS  userlogin_projects CASCADE;
CREATE TABLE userlogin_projects(
project_id INT REFERENCES projects(id),
userLogin_id INT REFERENCES userLogin(id), 
usertype usertype,
PRIMARY KEY (project_id, userLogin_id),
notes TEXT 
);





-- cosents 

DROP TABLE  IF EXISTS  consent CASCADE;
CREATE TABLE consent(
id SERIAL PRIMARY KEY, 
form VARCHAR NOT NULL, 
link VARCHAR, -- this could be a hyperlink of some sort to the actual document
notes TEXT
);

DROP TABLE  IF EXISTS  subject_consent CASCADE;
CREATE TABLE subject_consent(
subject_id uuid NOT NULL REFERENCES subject(id), 
consent_id INT NOT NULL REFERENCES consent(id),
timestamp TIMESTAMP(2) DEFAULT (now() at time zone 'PST'), -- , 
PRIMARY KEY (subject_id, consent_id),
notes TEXT
);

-- diagnosis 

DROP TABLE  IF EXISTS  diagnosis CASCADE;
CREATE TABLE diagnosis(
id SERIAL PRIMARY KEY, 
disease VARCHAR NOT NULL, 
notes TEXT
);

-- junction 

DROP TABLE  IF EXISTS  subject_diagnosis CASCADE;
CREATE TABLE subject_diagnosis(
subject_id uuid  NOT NULL REFERENCES subject(id),
diagnosis_id INT NOT NULL REFERENCES diagnosis(id), 
timestamp TIMESTAMP(2) DEFAULT (now() at time zone 'PST'), -- , 
PRIMARY KEY (diagnosis_id, subject_id),
notes TEXT
);

-- subject table 

CREATE TYPE sex AS ENUM ('M', 'F', 'UNK', 'OTHER');
DROP TABLE  IF EXISTS  subject CASCADE;
CREATE TABLE subject(
id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(), 
users VARCHAR NOT NULL, --from current user (store in session cookie on login)
age INT,
sex sex NOT NULL,
date_collection date NOT NULL,
timestamp TIMESTAMP(2) DEFAULT (now() at time zone 'PST'), -- ,
version INT, 
notes TEXT
);


DROP TABLE  IF EXISTS  subject_project CASCADE;
CREATE TABLE subject_project(
subject_id uuid NOT NULL REFERENCES subject(id), 
project_id INT NOT NULL REFERENCES projects(id),
timestamp TIMESTAMP(2) DEFAULT (now() at time zone 'PST'), -- , 
PRIMARY KEY (subject_id, project_id),
notes TEXT
);


-- sample 

-- ** keeps track of where each samples orignates from 


-- ** sample  

DROP TABLE  IF EXISTS  subtype CASCADE;
DROP TABLE  IF EXISTS  sampletype CASCADE;

CREATE TABLE subtype(
id SERIAL PRIMARY KEY, 
subtype VARCHAR NOT NULL, -- subtype tissue: Lung, Kidney, Blood, etc  molecular: RNA, DNA, Protein
notes TEXT
);

CREATE TABLE sampletype(
id SERIAL PRIMARY KEY, 
tissue VARCHAR NOT NULL, -- tissue, molecular, etc

notes TEXT
);	

-- units can be anything you want 
DROP TABLE  IF EXISTS  unit CASCADE;
CREATE TABLE unit(
id SERIAL PRIMARY KEY, 
unit VARCHAR NOT NULL, 
notes TEXT
);

-- storage locations 

DROP TABLE  IF EXISTS  location CASCADE;

CREATE TABLE location (
id SERIAL PRIMARY KEY,
parent_id INT REFERENCES location(id),
name VARCHAR NOT NULL,
parent_row INT,
parent_col INT,
rows INT,     -- rows available at this level
cols INT,      -- cols available at this level
notes TEXT)

DROP TABLE  IF EXISTS  location_project CASCADE;
CREATE TABLE location_project(
location_id INT REFERENCES location(id), 
project_id INT REFERENCES project(id), 
PRIMARY KEY(location_id, project_id)
)



DROP TABLE  IF EXISTS  sample CASCADE;
CREATE TABLE sample(
    id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(), 
    subject_id uuid NOT NULL REFERENCES  subject(id),  
	sampletype_id INT NOT NULL REFERENCES  sampletype(id), -- FK from type
	timestamp TIMESTAMP(2) DEFAULT (now() at time zone 'PST'), -- ,	
	
    users INT NOT NULL, -- from cookie
    amount double precision NOT NULL, 
	
	unit_id INT REFERENCES  unit(id), 
	
	location_id INT NOT NULL REFERENCES  location(id), 
    

	label VARCHAR NOT NULL, -- this is still to be decided contingent on what labeling machine we need


	parent uuid REFERENCES sample(id),
	
    notes TEXT	

	);

DROP TABLE  IF EXISTS  parentID CASCADE;

CREATE TABLE sample_parent_child(	
	child  uuid NOT NULL REFERENCES sample(id),
	parent uuid NOT NULL REFERENCES sample(parent) ,
	PRIMARY KEY (child, parent)
	);
		
	
-- end sample table creations 

-- logging tables here 
DROP TABLE  IF EXISTS  version;
CREATE TABLE version(
calling_table VARCHAR, -- name of calling table
id uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(), -- primary id of calling table
version_number INT NOT NULL, -- script will figure this out
users INT, -- from current user (store in cookie on login)
timestamp TIMESTAMP(2) DEFAULT (now() at time zone 'PST'), -- when  was this triggered
data_log JSON, -- stores only what was changed 
notes TEXT
);
DROP TABLE  IF EXISTS  logger;
CREATE TABLE logger(
id SERIAL PRIMARY KEY,
tablename VARCHAR,
username VARCHAR,
timestamp TIMESTAMP(2) DEFAULT (now() at time zone 'PST'), -- when  was this triggered
lognotes TEXT
);

	



