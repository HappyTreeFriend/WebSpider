import sqlite3,os
try:
	os.remove('example.db')
except:
	pass
conn = sqlite3.connect('example.db')
c = conn.cursor()

# Create table
c.executescript('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real);''')

# Insert a row of data
c.executescript("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14);")

# Save (commit) the changes
conn.commit()
print c.fetchall()

# Never do this -- insecure!
symbol = 'RHAT'
c.executescript("SELECT * FROM stocks;")
print c.fetchall()

# Do this instead
t = ('RHAT',)
c.executescript('SELECT * FROM stocks;')
print c.fetchall()

# Larger example that inserts many records at a time
conn.commit()
c.executescript('SELECT * FROM stocks;')
print c.fetchall()
#print c.fetchone()
#print c.fetchall()
