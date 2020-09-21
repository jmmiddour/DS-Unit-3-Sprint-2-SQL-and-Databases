###### Part 1 of Assignment - Reproduce the live lecture ######
import os
from dotenv import load_dotenv
import psycopg2

# Load contents of .env file:
load_dotenv()

# Create variables for connecting to ElephantSQL:
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')

# Check to make sure the environment variables are coded properly:
# print(DB_NAME, DB_USER, DB_PASS, DB_HOST)
# exit()  ^<-- Check worked so can comment both of these out.

# Create a connection object to connect to ElephantSQL:
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST)

# Create the cursor object:
cursor = conn.cursor()

# Execute a query:
cursor.execute('SELECT * FROM test_table')

# Need to get the data with fetchall seperately with postgreSQL:
results = cursor.fetchall()
# print(results)  <-- Commenting out for now, do not need it anymore.


############ Connect to SQLite DB for RPG Data #############

import sqlite3

# Create SQLite connection:
s1_conn = sqlite3.connect('rpg_db.sqlite3')

# Create the SQLite cursor:
s1_cursor = s1_conn.cursor()

# Execute SQLite characters from RPG DB:
characters = s1_cursor.execute('SELECT * FROM charactercreator_character;').fetchall()
# print(characters)  <-- Commenting out for now, do not need it anymore.

###### Create the Character Table in Postgres and Insert Data ######

create_character_table_query = '''
CREATE TABLE IF NOT EXISTS rpg_characters (
    character_id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    level INT,
    exp INT,
    hp INT,
    strength INT, 
    intelligence INT,
    dexterity INT,
    wisdom INT
)
'''

# Execute the above SQL statement:  
cursor.execute(create_character_table_query)

# Need to commit for the changes to take place:
conn.commit()

# One way to insert the data into the table:
for character in characters:
    insert_query = f'''INSERT INTO rpg_characters
    (character_id, name, level, exp, hp, strength, intelligence,
    dexterity, wisdom)
    VALUES {character}
    '''
    cursor.execute(insert_query)
conn.commit()
