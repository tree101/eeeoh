# takes a table name and returns a table in html with column names dude
def getTableHTML(conn,table):
    
	
		cur = conn.cursor()
		# go get column name man
		out = getColName(conn,table)
		out = '<tr>'+out+'</tr>'; 
		mydb = 'SELECT * from '+ table ; 
		cur.execute(mydb)
		rows = cur.fetchall()
		
		for row in rows:
			#out = row[1]
			out = out+ '<tr>'+' '.join('<td>{0}</td>'.format(w) for w in row)+'</tr>'
	     
		out = '<table>' + out + '</table>'
		
		return (out)
		

def getColName(conn,table):
	cur = conn.cursor()
	mydb = 'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \''+ table + '\'';

	out='' 
	cur.execute(mydb)
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
		for h in head:
			out = out+ '<td>' + h + '</td>'
		
		out = out + '</tr>';
		for row in rows:
			#out = row[1]
			out = out+ '<tr>'+' '.join('<td>{0}</td>'.format(w) for w in row)+'</tr>'
	     
		out = '<table>' + out + '</table>'
		
		return (out)
		
