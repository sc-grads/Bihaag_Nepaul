import pyodbc
import pandas as pd
import pwinput


"""
    Creates a table in a SQL database and inserts data from a pandas DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data to be inserted into the table.
        table_name (str): The name of the table to be created.

    Returns:
        None

    Raises:
        pyodbc.InterfaceError: If there is an error with the database connection.
        pyodbc.OperationalError: If there is an error with the database operation.
        pyodbc.ProgrammingError: If there is an error with the SQL syntax or database structure.
        pyodbc.Error: If there is any other error during the execution.

    Prints:
        - Welcome to the data exporter for SQL!
        - Please enter your SQL Server details
        - Enter the SQL Server name:
        - Enter the database name:
        - Enter the user name:
        - Enter the password:
        - Please confirm the following details:
        - Server: {server}
        - Database: {database}
        - User Name: {uid}
        - Are these details correct? (yes/no):
        - Generated CREATE TABLE query: {create_table_query}
        - Table created successfully!
        - Data inserted successfully!
        - An interface error occurred. Please check your connection details and try again.
        - An operational error occurred. This may be due to incorrect server details or network issues.
        - A programming error occurred. Please check your SQL syntax and database structure.
        - Login failed for user. Please check your username and password.
        - Database does not exist or insufficient permissions. Please check the database name and user permissions.
        - An error occurred: {e}
"""
def create_table_and_insert_data(df, table_name):
    print("Welcome to the data exporter for SQL!")
    while True:
        # Prompt user for database details
        print("Please enter your SQL Server details")
        server = input("Enter the SQL Server name: ")
        database = input("Enter the database name: ")
        uid = input("Enter the user name: ")
        pwd = pwinput.pwinput("Enter the password: ")

        # Display the entered details for confirmation
        print("\nPlease confirm the following details:")
        print(f"Server: {server}")
        print(f"Database: {database}")
        print(f"User Name: {uid}")
        confirmation = input("Are these details correct? (yes/no): ").strip().lower()

        if confirmation == 'yes':
            break
        else:
            print("Let's try again.\n")

    driver = '{ODBC Driver 18 for SQL Server}'

    try:
        conn = pyodbc.connect(
            Driver=driver,
            Server=server,
            Database=database,
            Encrypt="no",  
            TrustServerCertificate="yes",  
            UID=uid, 
            PWD=pwd
        )
        cursor = conn.cursor()

        # Generate the CREATE TABLE statement dynamically
        create_table_query = f"CREATE TABLE {table_name} ("
        for column in df.columns:
            # Escape column names and assume all columns are of type VARCHAR(255) for simplicity
            create_table_query += f"[{column}] VARCHAR(255), "
        
        # Remove the last comma and space
        create_table_query = create_table_query[:-2] + ")"
        
        print("Generated CREATE TABLE query:", create_table_query)

        try:
            cursor.execute(create_table_query)
            print("Table created successfully!")
        except Exception as e:
            print("Error creating table:", e)

        # Generate the INSERT INTO statement dynamically
        insert_query = f"INSERT INTO {table_name} ({', '.join([f'[{col}]' for col in df.columns])}) VALUES ({', '.join(['?' for _ in df.columns])})"
        
        for index, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))

        conn.commit()
        print("Data inserted successfully!")
    except pyodbc.InterfaceError as ie:
        print("An interface error occurred. Please check your connection details and try again.")
    except pyodbc.OperationalError as oe:
        print("An operational error occurred. This may be due to incorrect server details or network issues.")
    except pyodbc.ProgrammingError as pe:
        print("A programming error occurred. Please check your SQL syntax and database structure.")
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == '28000':
            print("Login failed for user. Please check your username and password.")
        elif sqlstate == '42000':
            print("Database does not exist or insufficient permissions. Please check the database name and user permissions.")
        else:
            print(f"An error occurred: {e}")

# Example usage
data = pd.read_csv('muffins_cupcakes.csv')





