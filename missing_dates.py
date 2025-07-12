import mysql.connector 
from datetime import date, timedelta
import json

try:

  

#connection creds
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
    print('Error when connecting to database: {}'.format(err))
    
if connection:
    #makes cursor
    cursor = connection.cursor()
    
try:
    
    #makes the table missing_dates
    query_create_table =  " CREATE TABLE IF NOT EXISTS missing_dates (date DATE) "
    cursor.execute(query_create_table)
    
    #makes cursor and runs and fetches min and max date and puts them in a table (0 and 1 represent index marks in the table**)
    query_select_min_max = "SELECT MIN(date) as min_date, MAX(date) as max_date FROM stocks"
    cursor.execute(query_select_min_max)
    min_max_date = cursor.fetchone()
    min_date = min_max_date [0]
    max_date = min_max_date [1]
    
    #generates missing dates (missing date list empty because we generate the list and when the while loop is done and we exit it, it wont append additonal dates!)
    
    missing_dates = [(date,) for date in [min_date + timedelta(days=i) for i in range ((max_date - min_date).days+1)]]
    
    #inserts all dates between min and max into the database
    for current_date in missing_dates:
        query_insert_missing_dates = "INSERT INTO missing_dates (date) VALUES (%s)"
        cursor.execute(query_insert_missing_dates, (current_date[0],))
        print(f"Inserted {current_date[0]} into missing table.")
        
except mysql.connector.Error as err:
    print('Error executing SQL queries:', err)
    
finally:
    #close cursor here
    if 'cursor' in locals():
        try:
            cursor.close()
        except NameError as e:
            pass
    
    #commit changes (dont forget to add this in future ones idiot(IT WONT SHOW THE DATA IF YOU DONT COMMIT IT MORON))
    try:
        connection.commit()
    except mysql.connector.Error as err:
        print("Error commiting changes:", err)
        
    #CLOSE CONNECTION
    try:
        if 'connection' in locals() and connection is not None:
            connection.close()
    except NameError as e:
        pass
    

    



    
    
    
    
