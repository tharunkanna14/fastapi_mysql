import pymysql

# create a connection object
conn = pymysql.connect(host='database-1.crxxhbqbmrqj.us-east-2.rds.amazonaws.com',
                       user='admin',
                       password='changeme',
                       database='student_db')

# create a cursor object
cursor = conn.cursor()

# execute the SHOW TABLES command to display all tables in the database
cursor.execute("SHOW TABLES")

# fetch all the results
tables = cursor.fetchall()

# display the tables
print("Tables in the student_db database:")
for table in tables:
    print(table[0])

# close the cursor and connection objects
cursor.close()
conn.close()
