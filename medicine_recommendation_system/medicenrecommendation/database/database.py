# import sqlite3
# import pandas as pd

# # Database connection function
# def get_db_connection():
#     """
#     Establish a connection to the SQLite database. 
#     Creates the database file if it doesn't exist.

#     Returns:
#         connection (sqlite3.Connection): SQLite connection object
#     """
#     connection = sqlite3.connect('medicine_recommendation.db')
#     connection.row_factory = sqlite3.Row  # Enables dictionary-style row access
#     return connection

# # Function to create tables
# def create_tables():
#     """
#     Creates the necessary tables in the database if they don't already exist.
#     """
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     # Table for storing symptoms and their associated diseases
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS symptoms (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             symptom TEXT NOT NULL UNIQUE,
#             disease TEXT NOT NULL
#         )
#     ''')

#     # Table for storing disease descriptions
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS descriptions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             disease TEXT NOT NULL UNIQUE,
#             description TEXT NOT NULL
#         )
#     ''')

#     # Table for storing precautions for diseases
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS precautions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             disease TEXT NOT NULL,
#             precaution_1 TEXT,
#             precaution_2 TEXT,
#             precaution_3 TEXT,
#             precaution_4 TEXT
#         )
#     ''')

#     # Table for storing medications for diseases
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS medications (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             disease TEXT NOT NULL,
#             medication TEXT
#         )
#     ''')

#     # Table for storing recommended diets for diseases
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS diets (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             disease TEXT NOT NULL,
#             diet TEXT
#         )
#     ''')

#     # Table for storing recommended workouts for diseases
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS workouts (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             disease TEXT NOT NULL,
#             workout TEXT
#         )
#     ''')

#     connection.commit()
#     connection.close()

# # Function to insert data into a specific table
# def insert_data(table_name, data):
#     """
#     Insert data into the specified table.

#     Args:
#         table_name (str): Name of the table to insert data into
#         data (list of tuples): List of tuples containing the data to insert
#     """
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     # Validate data to match table structure
#     if table_name == "symptoms":
#         # Ensure only (symptom, disease) pairs are inserted
#         data = [(row[0], row[1]) for row in data]  # Only take the first two columns

#     if table_name == "workouts":
#         # Ensure only (disease, workout) pairs are inserted
#         data = [(row[0], row[1]) for row in data]  # Only take the first two columns (disease, workout)

#     if table_name == "precautions":
#         # Ensure only (disease, precaution_1, precaution_2, precaution_3, precaution_4) are inserted
#         data = [(row[0], row[1], row[2], row[3], row[4]) for row in data]  # Ensure matching columns

#     if table_name == "medications":
#         # Ensure only (disease, medication) pairs are inserted
#         data = [(row[0], row[1]) for row in data]  # Only take the first two columns

#     if table_name == "diets":
#         # Ensure only (disease, diet) pairs are inserted
#         data = [(row[0], row[1]) for row in data]  # Only take the first two columns

#     # Generate a query based on the number of columns in the data
#     placeholders = ', '.join(['?'] * len(data[0]))
#     query = f'INSERT OR IGNORE INTO {table_name} VALUES (NULL, {placeholders})'

#     cursor.executemany(query, data)
#     connection.commit()
#     connection.close()

# # Function to retrieve data from a specific table
# def get_data(table_name, condition=None):
#     """
#     Retrieve data from the specified table.

#     Args:
#         table_name (str): Name of the table to retrieve data from
#         condition (str, optional): WHERE condition for filtering data

#     Returns:
#         rows (list of sqlite3.Row): Retrieved rows from the table
#     """
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     query = f'SELECT * FROM {table_name}'
#     if condition:
#         query += f' WHERE {condition}'

#     cursor.execute(query)
#     rows = cursor.fetchall()
#     connection.close()
#     return rows

# # Function to initialize the database with CSV data
# def initialize_database_from_csv():
#     """
#     Initializes the database by loading data from CSV files
#     and populating the respective tables.
#     """
#     # Define CSV file paths
#     sym_des_path = r"C:\Users\adams\Downloads\symtoms_df.csv"
#     precautions_path = r"C:\Users\adams\Downloads\precautions_df (1).csv"
#     workout_path = r"C:\Users\adams\Downloads\workout_df.csv"
#     description_path = r"C:\Users\adams\Downloads\description.csv"
#     medications_path = r"C:\Users\adams\Downloads\medications.csv"
#     diets_path = r"C:\Users\adams\Downloads\diets.csv"

#     # Load and insert data
#     sym_des_df = pd.read_csv(sym_des_path)
#     precautions_df = pd.read_csv(precautions_path)
#     workout_df = pd.read_csv(workout_path)
#     description_df = pd.read_csv(description_path)
#     medications_df = pd.read_csv(medications_path)
#     diets_df = pd.read_csv(diets_path)

#     # Drop the 'Unnamed: 0' column (index column)
#     precautions_df = precautions_df.drop(columns=['Unnamed: 0'])

#     # Ensure correct columns for symptoms
#     sym_des_df = sym_des_df[['Symptom_1', 'Disease']]

#     # Ensure correct columns for workouts
#     workout_df = workout_df[['Unnamed: 0.1', 'Unnamed: 0', 'disease', 'workout']]  # Adjust column names as needed

#     # Insert data into tables
#     insert_data('symptoms', sym_des_df.values.tolist())
#     insert_data('precautions', precautions_df.values.tolist())
#     insert_data('workouts', workout_df.values.tolist())
#     insert_data('descriptions', description_df.values.tolist())
#     insert_data('medications', medications_df.values.tolist())
#     insert_data('diets', diets_df.values.tolist())

# # Function to clear all data from a table
# def clear_table(table_name):
#     """
#     Clear all data from the specified table.

#     Args:
#         table_name (str): Name of the table to clear
#     """
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     cursor.execute(f'DELETE FROM {table_name}')
#     connection.commit()
#     connection.close()

# # Initialize database tables when this script runs
# if __name__ == '__main__':
#     create_tables()
#     initialize_database_from_csv()
#     print("Database initialized successfully!")


import sqlite3
import pandas as pd


# Database connection function
def get_db_connection():
    """
    Establish a connection to the SQLite database. 
    Creates the database file if it doesn't exist.

    Returns:
        connection (sqlite3.Connection): SQLite connection object
    """
    connection = sqlite3.connect('medicine_recommendation.db')
    connection.row_factory = sqlite3.Row  # Enables dictionary-style row access
    return connection


# Function to create tables
def create_tables():
    """
    Creates the necessary tables in the database if they don't already exist.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    # Table for storing symptoms and their associated diseases
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS symptoms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptom TEXT NOT NULL UNIQUE,
            disease TEXT NOT NULL
        )
    ''')

    # Table for storing disease descriptions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL
        )
    ''')

    # Table for storing precautions for diseases
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS precautions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT NOT NULL,
            precaution_1 TEXT,
            precaution_2 TEXT,
            precaution_3 TEXT,
            precaution_4 TEXT
        )
    ''')

    # Table for storing medications for diseases
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT NOT NULL,
            medication TEXT
        )
    ''')

    # Table for storing recommended diets for diseases
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT NOT NULL,
            diet TEXT
        )
    ''')

    # Table for storing recommended workouts for diseases
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT NOT NULL,
            workout TEXT
        )
    ''')

    # Table for storing feedback
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()


# Function to insert data into a specific table
def insert_data(table_name, data):
    """
    Insert data into the specified table.

    Args:
        table_name (str): Name of the table to insert data into
        data (list of tuples): List of tuples containing the data to insert
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    # Generate a query based on the number of columns in the data
    placeholders = ', '.join(['?'] * len(data[0]))
    query = f'INSERT OR IGNORE INTO {table_name} VALUES (NULL, {placeholders})'

    cursor.executemany(query, data)
    connection.commit()
    connection.close()


# Function to retrieve data from a specific table
def get_data(table_name, condition=None):
    """
    Retrieve data from the specified table.

    Args:
        table_name (str): Name of the table to retrieve data from
        condition (str, optional): WHERE condition for filtering data

    Returns:
        rows (list of sqlite3.Row): Retrieved rows from the table
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    query = f'SELECT * FROM {table_name}'
    if condition:
        query += f' WHERE {condition}'

    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    return rows


# Function to initialize the database with CSV data
def initialize_database_from_csv():
    """
    Initializes the database by loading data from CSV files
    and populating the respective tables.
    """
    # Define CSV file paths
    sym_des_path = r"C:\Users\adams\Downloads\symtoms_df.csv"
    precautions_path = r"C:\Users\adams\Downloads\precautions_df (1).csv"
    workout_path = r"C:\Users\adams\Downloads\workout_df.csv"
    description_path = r"C:\Users\adams\Downloads\description.csv"
    medications_path = r"C:\Users\adams\Downloads\medications.csv"
    diets_path = r"C:\Users\adams\Downloads\diets.csv"

    # Load and insert data
    sym_des_df = pd.read_csv(sym_des_path)
    precautions_df = pd.read_csv(precautions_path)
    workout_df = pd.read_csv(workout_path)
    description_df = pd.read_csv(description_path)
    medications_df = pd.read_csv(medications_path)
    diets_df = pd.read_csv(diets_path)

    # Adjust column selection based on expected table structure
    insert_data('symptoms', sym_des_df[['Symptom_1', 'Disease']].values.tolist())
    insert_data('precautions', precautions_df[['Disease', 'Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']].values.tolist())
    insert_data('workouts', workout_df[['disease', 'workout']].values.tolist())
    insert_data('descriptions', description_df[['Disease', 'Description']].values.tolist())
    insert_data('medications', medications_df[['Disease', 'Medication']].values.tolist())
    insert_data('diets', diets_df[['Disease', 'Diet']].values.tolist())


# Function to add feedback
def add_feedback(feedback):
    """
    Add feedback to the feedback table.

    Args:
        feedback (str): Feedback text to insert
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO feedback (feedback) VALUES (?)', (feedback,))
    connection.commit()
    connection.close()


# Function to retrieve feedback
def get_feedback():
    """
    Retrieve all feedback entries from the database.

    Returns:
        feedback (list of sqlite3.Row): List of feedback entries
    """
    return get_data('feedback')


# Function to clear all data from a table
def clear_table(table_name):
    """
    Clear all data from the specified table.

    Args:
        table_name (str): Name of the table to clear
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM {table_name}')
    connection.commit()
    connection.close()


# Initialize database tables when this script runs
if __name__ == '__main__':
    create_tables()
    initialize_database_from_csv()
    print("Database initialized successfully!")
