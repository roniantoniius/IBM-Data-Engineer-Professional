# Import libraries required for connecting to mysql
import mysql.connector
import psycopg2


# Connect to MySQL
connection = mysql.connector.connect(user='root', password='vo7s1YPGmY3c16zWx8L25rLk',host='172.21.247.123',database='sales')
if (connection):
	print("Connected to MySQL")
# create cursor
cursor = connection.cursor()

dsn_hostname = '172.21.247.1'
dsn_user='postgres'        # e.g. "abc12345"
dsn_pwd ='9rByRHD9xA0znXBPjIuS1frP'      # e.g. "7dBZ3wWt9XN6$o0J"
dsn_port ="5432"                # e.g. "50000" 
dsn_database ="postgres"           # i.e. "BLUDB"
conn = psycopg2.connect(
   database=dsn_database, 
   user=dsn_user,
   password=dsn_pwd,
   host=dsn_hostname, 
   port= dsn_port
)
cursor_psql=conn.cursor()

# Find out the last rowid from DB2 data warehouse or PostgreSql data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database or PostgreSql.

def get_last_rowid():
    query="SELECT rowid FROM sales_data ORDER BY rowid DESC LIMIT 1"
    cursor_psql.execute(query)
    last_row=cursor_psql.fetchone()[0]
    return last_row


last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
    query=f"SELECT * FROM sales.sales_data WHERE rowid>{rowid}"
    cursor_msql.execute(query)
    row_list=[]
    output=cursor_msql.fetchall()
    for row in output:
        row_list.append(row)   

    return row_list

		

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from MySQL into DB2 or PostgreSql data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in IBM DB2 database or PostgreSql.

def insert_records(records):
    for row in records:
        p_query=f"INSERT INTO sales_data Values{row}"
        cursor_psql.execute(p_query)

    

insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse
connection.close()
# disconnect from DB2 or PostgreSql data warehouse 
conn.close()
# End of program