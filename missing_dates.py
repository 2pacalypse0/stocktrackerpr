import mysql.connector 
from datetime import date, timedelta

#connection creds
try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port = '3306',
        
        user='root',
        password='2pacAlivefastrap',
        database='ruffridaz'
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
    

    



    
    
    
    