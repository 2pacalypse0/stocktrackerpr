import yfinance as yf
import mysql.connector
from mysql.connector import Error


def connect_to_database():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port='3306',
            
            user='root',
            password='2pacAlivefastrap',
            database='ruffridaz' )
        
          
            
            

        return connection, None

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

    if error is None:
        try:
            # Connect to database and download stock data
            stock_data = yf.download('AAPL', start='2023-01-01', end='2024-06-25')

            # Insert the data into the database
            cursor = connection.cursor()
            for index, row in stock_data.iterrows():
                values = [index, float(row['Open']), float(row['High']), float(row['Low']), float(row['Close']), int(row['Volume'])]
                
                query = "INSERT INTO stocks (date, open, high, low, close, volume) VALUES(%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, values)
            connection.commit()
            
        except Error as e:
            print(f"Error inserting data into database: {e}")
            

    if error is None:
        try:
            create_table_if_not_exists(connection)

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
                print('MySQL connection closed')
                


if __name__ == "__main__":
    main()