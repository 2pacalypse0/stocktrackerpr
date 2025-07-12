import yfinance as yf
import mysql.connector
from mysql.connector import Error
import json



def connect_to_database():
    
    try:

        
        # load config data from json
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

        return connection, None
    #some blocks for errors
    except FileNotFoundError:
        print("Error: config.json not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON in config.json")
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None, f"Error connecting to the database: {e}"

def create_table_if_not_exists(connection):
    try:
        # Create a cursor object
        cursor = connection.cursor()

        # Check if the table exists
        query = "SHOW TABLES LIKE 'stocks'"
        cursor.execute(query)
        
        if not cursor.fetchone():
            # If the table does not exist, create it
            query = "CREATE TABLE stocks (date DATE, open FLOAT, high FLOAT, low FLOAT, close FLOAT, volume INT)"
            cursor.execute(query)

    except Error as e:
        print(f"Error creating table or executing query: {e}")

def main():
    connection, error = connect_to_database()

    if connection is not None:
        try:
            # Connect to database and download stock data
            stock_data = yf.download('AAPL', start='2023-01-01', end='2024-06-25') #you need to change the stock option and dates for sampling here until i get around automating the process and visualzing it!

            # Insert the data into the database
            cursor = connection.cursor()
            for index, row in stock_data.iterrows():
                values = [index, float(row['Open']), float(row['High']), float(row['Low']), float(row['Close']), int(row['Volume'])]
                
                query = "INSERT INTO stocks (date, open, high, low, close, volume) VALUES(%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, values)
            connection.commit()
            
        except Error as e:
            print(f"Error inserting data into database: {e}")
            

    if connection is not None:
        try:
            create_table_if_not_exists(connection)

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
                print('MySQL connection closed')
                


if __name__ == "__main__":
    main()
