
import psycopg2
conn = psycopg2.connect("dbname='eeeoh' user='alexsql' host='localhost' password='eeeoooh'")

cur = conn.cursor()
mydb = 'SELECT * from '+ 'userlogin'; 
mydb = 'Select * from userlogin where email=\'tree101@stanford.edu\' ';
cur.execute(mydb)
rows = cur.fetchall()
if not rows:
	print "user does not exists"
else:
	name= rows[0][1] + " " + rows[0][2]
	group=rows[0][4]
	user=rows[0][3]
	# check 
	pw_hash = bcrypt.generate_password_hash(rows[0][5])
	passornot = bcrypt.check_password_hash(pw_hash, 'boofdsfdk102') 
	print passornot
