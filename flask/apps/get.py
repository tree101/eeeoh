import psycopg2
from psycopg2.extensions import AsIs
# takes a table name and returns a table in html with column names dude
def getTableHTML(conn,table):
		
		
		cur = conn.cursor()
		# go get column name man
		out = getColName(conn,table)
		out = '<tr>'+out+'</tr>'; 
		
		data = (table,)
		mydb = "SELECT * from %(table)s;"; 
		cur.execute(mydb,{"table": AsIs(table)})
		rows = cur.fetchall()
		
		for row in rows:
			#out = row[1]
			out = out+ '<tr>'+' '.join('<td>{0}</td>'.format(w) for w in row)+'</tr>'
	     
		out = '<table>' + out + '</table>'
		
		return (out)
		

def getColName(conn,table):
	cur = conn.cursor()
	data = (table,)
	mydb = 'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s';

	out='' 
	cur.execute(mydb,data)
	rows = cur.fetchall()
	if rows:
		for col in rows:
			out = out+'<td>'+col[0]+'</td>'
	return out
	

	
def sendSql(conn,commands,head):

		cur = conn.cursor()
		
		out='<tr>'
		cur.execute(commands)
		rows = cur.fetchall()
		
		r= []
		for row in rows:
			r.append(row)
		
		return (r)
		
