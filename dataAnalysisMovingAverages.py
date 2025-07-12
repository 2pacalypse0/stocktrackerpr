import mysql.connector
from tabulate import tabulate
import json
# Connect to database
try:
  
    with open('config.json', 'r') as f:
         config_data = json.load(f)
  
            
        # pull the database connection deets from the config data
         host = config_data['database']['host']
         port = config_data['database']['port']
         username = config_data['database']['username']
         password = config_data['database']['password']
         database = config_data['database']['name']
        
        #it now connects to the database using extracted deets
         connection = mysql.connector.connect(
            host=host,
            port=int(port),
            username=username,
            password=password,
            database=database
        )
except mysql.connector.Error as err:
 print("Error connecting to database: {}".format(err))

if connection:
    # Create a cursor object
    cursor = connection.cursor()
    
    query_create_table=""" 
    CREATE TABLE IF NOT EXISTS moving_averages( date DATE,MA20 DECIMAL(10, 2))
    """  

    # Query to get data
    query_insert_data= """
        INSERT INTO  moving_averages (date, MA20)
        SELECT  date, AVG(close) OVER (ORDER BY date ROWS 20 PRECEDING) AS "MA_20"
        FROM(
            SELECT  date, close
            FROM stocks WHERE date >= '2023-01-01' AND date <= '2024-06-25'
            ORDER BY date
        ) AS subquery
    """

    # Execute query and get results
    try:
        cursor.execute(query_create_table)
        connection.commit() #commits changes
    except Exception as e:
        print(f"Failed to create table: {e}")
        
    try:
        cursor.execute(query_insert_data)
        connection.commit() #commits changes to database
    except Exception as e:
        print(f'Failed to insert data into table: {e}')
        

# Close the cursor and connection (if it exists)
try:
    if 'cursor' in locals():
        cursor.close()
except NameError as e:
    pass

try:
    if 'connection' in locals() and connection is not None:
        connection.close()
except NameError as e:
    pass
