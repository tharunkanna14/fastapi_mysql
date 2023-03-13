import pymysql

# Establish a connection to the database
connection = pymysql.connect(
    host="database-1.crxxhbqbmrqj.us-east-2.rds.amazonaws.com",
    user="admin",
    password="changeme",
    database="student_db"
)

# Check if the connection is successful
if connection:
    print("Connection successful!")
else:
    print("Connection unsuccessful.")

# Close the connection
connection.close()
