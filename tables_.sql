--- three main tables
--- subject
--- sample
--- version

--- subtables
--- (1) "action" use to indicate what was done such as: create, modify, revert, withdraw, split, add, dispose 
--- (2) "protocol"


------- comments
--- version is a three column uuid, action, date, table, with a JSON type to keep records 
--- I don't think we should allow undo/revert function because it will make the version control 
--- problematic, perhaps just allow program to populate and revert as one the actions


DROP TABLE  IF EXISTS  subject;
CREATE EXTENSION "uuid-ossp";
CREATE TABLE subject(
id uuid NOT NULL DEFAULT uuid_generate_v4(), 
age INT,
sex INT,
protocol INT  ## FK
date_collection DATE NOT NULL
version INT DEFAULT
action INT ## 
);


INSERT INTO subject ("id","age")
	VALUES (
	uuid_generate_v4(), '111'
	
	);


DROP TABLE  IF EXISTS  tissue;
-- table below stores data for tissue biopsy collection

CREATE TABLE sample_type_data(
    id INT NOT NULL, -- unique to each subject: see below for contraints 
    id_sample INT NOT NULL, -- unique to each biopsy 
    tissue_type VARCHAR(50) NOT NULL, -- predefined dictionary table
    date_collection date NOT NULL,
    location_collection VARCHAR(50) NOT NULL, -- predefined dictionary table
    grade INT NOT NULL, -- by percent from 0-100 - this is how Stan grades his samples
    technician VARCHAR(50) NOT NULL, -- login username
    orientation VARCHAR(50) NOT NULL, -- dictionary table
    amount double precision NOT NULL, -- in milligrams
    location_storage VARCHAR(50) NOT NULL, -- predefined dictionary table
    timestamp TIMESTAMP(2) DEFAULT (now() at time zone 'PST'), 
    action VARCHAR(50) NOT NULL,
    version INT DEFAULT 0, -- control by function below
    comments VARCHAR(300),
    UNIQUE (id, id_sample,version) -- the combination of these three fields makes a unique record
);



-- below functions keeps track of version number 

CREATE OR REPLACE FUNCTION version_c() RETURNS TRIGGER AS $version_c$
BEGIN
      SELECT max(version) + 1 INTO NEW.version
      FROM tissue
      WHERE id = NEW.id AND id_sample=NEW.id_sample;
      If NEW.version IS NULL  THEN
          NEW.version = 1;
      END IF;
 RETURN NEW;
END;
$version_c$
language plpgsql;

-- trigger to update version number before insertion

CREATE TRIGGER tr_version_c
  BEFORE INSERT OR UPDATE ON tissue
  FOR EACH ROW EXECUTE PROCEDURE version_c();
  
-- below are some sample inputs, however, because its done all at once
-- timestamp for version control are all the same


INSERT INTO tissue (
id, id_sample, tissue_type, date_collection, location_collection,grade,technician,orientation,amount,
location_storage, timestamp, action,version
) 
VALUES (1,1,'lung','2015-09-24','stanford hospital',80,'alex','RU',50,'-80,A',DEFAULT,'create',DEFAULT);



-- example of what happens when sample is relocated. 

INSERT INTO tissue (
id, id_sample, tissue_type, date_collection, location_collection,grade,technician,orientation,amount,
location_storage, timestamp, action,version
) 
VALUES (1,1,'lung','2015-09-24','stanford hospital',80,'alex','RU',50,'-20,A',DEFAULT,'moved',DEFAULT);



-- example of when samples are withdrawn 
-- UI will automatically deduct what has been removed, in ths case 20 mg was removed 
-- UI will force user to only use most current version 
INSERT INTO tissue (
id, id_sample, tissue_type, date_collection, location_collection,grade,technician,orientation,amount,
location_storage, timestamp, action,version
) 
VALUES (1,1,'lung','2015-09-25','stanford hospital',80,'alex','RU',30,'-20,A',DEFAULT,'removed',DEFAULT);


-- create new biopsy from same id, blood
-- note that change in id_sample
INSERT INTO tissue (
id, id_sample, tissue_type, date_collection, location_collection,grade,technician,orientation,amount,
location_storage, timestamp, action,version
) 
VALUES (1,2,'blood','2015-09-24','stanford hospital',80,'alex','RU',50,'-80,A',DEFAULT,'create',DEFAULT);


INSERT INTO tissue (
id, id_sample, tissue_type, date_collection, location_collection,grade,technician,orientation,amount,
location_storage, timestamp, action,version
) 
VALUES (2,1,'lung','2015-09-26','stanford hospital',80,'alex','LL',50,'-80,A',DEFAULT,'create',DEFAULT);

INSERT INTO tissue (
id, id_sample, tissue_type, date_collection, location_collection,grade,technician,orientation,amount,
location_storage, timestamp, action,version
) 
VALUES (2,1,'lung','2015-09-26','stanford hospital',80,'alex','LL',0,'-80,A',DEFAULT,'removed',DEFAULT);

-- examples below to show different ways to query version numbers. 
-- most likely I will do the heavy lifting via my script since I'm not that familiar with SQL B
-- nonetheless here is an example in SQL 


-- show table with most current versions only 
SELECT * FROM tissue v1 WHERE NOT EXISTS(
SELECT * FROM tissue vn WHERE vn.id_sample=v1.id_sample AND vn.id=v1.id AND vn.version>v1.version);

-- show table but null all the other version 
SELECT
    *,
    CASE 
        WHEN version = max(version) over(partition by id_sample,id) 
        THEN version
        ELSE 
            NULL
        
    END 

FROM tissue

