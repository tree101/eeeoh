import psycopg2
from psycopg2.extensions import AsIs
# returns a generic table 
def getTableHTML(conn,table):
		
		
		cur = conn.cursor()
		# go get column name man
		out = getColName(conn,table)
		
		
		data = (table,)
		mydb = "SELECT * from %(table)s;"; 
		cur.execute(mydb,{"table": AsIs(table)})
		rows = cur.fetchall()
		
		
		return (rows)
		

def getColName(conn,table):
	cur = conn.cursor()
	data = (table,)
	mydb = 'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s';

	out='' 
	cur.execute(mydb,data)
	rows = cur.fetchall()

	return rows
	

	
def sendSql(conn,commands,head):

		cur = conn.cursor()
		
		
		cur.execute(commands)
		rows = cur.fetchall()
		
		
		
		return (rows)



def checkuser(cur, user):

		c = 'SELECT is_admin FROM userlogin WHERE email = %s;'
		cur.execute(c,(user,))
		rows = cur.fetchall()
		
		return (rows[0][0])
		

def getChild_location(cur,pre,name,location):
	
	c = 'SELECT id, name FROM location WHERE parent_id = %s;'
	cur.execute(c,(pre,))
	rows = cur.fetchall()
	if rows: 
		for r in rows: 
			location.append([r[0],name,r[1]])
			location = getChild_location(cur,r[0],name+"_"+r[1],location)
		

	return(location)
		
