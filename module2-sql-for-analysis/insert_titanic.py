import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2
import csv

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

# Connect to my database where adding the new table:
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST)

# Create cursor object:
cursor = conn.cursor()

# Read in the titanic.csv file:
df = csv.reader(open('titanic.csv'))

# Create a table to upload the data from the titanic csv file:
create_titanic_table = '''
CREATE TYPE PCLASS AS ENUM ('upper', 'middle', 'lower');
CREATE TABLE IF NOT EXISTS titanic (
    "record_id" SERIAL PRIMARY KEY,
    "survived" BOOL,
    "passenger_class" PCLASS,
    "name" VARCHAR(250),
    "sex" VARCHAR(7),
    "age" DECIMAL(3, 1),
    "num_siblings_spouses_aboard" INT,
    "num_parents_children_aboard" INT,
    "passenger_fare" DECIMAL(3, 2)
);
'''

# Execute the above statement:
cursor.execute('DROP TYPE IF EXISTS PCLASS CASCADE')
cursor.execute('DROP TABLE IF EXISTS titanic')
cursor.execute(create_titanic_table)

# Commit the changes:
# conn.commit()

# Insert data into the table:{'survived':'Survived'}, 
#   {'passenger_class':'Pclass}, {'full_name':'Name'},
#   {'sex':'Sex'}, {'age':'Age'}, 
#   {'num_siblings_spouses_aboard':'Siblings/Spouses Aboard'},
#   {'num_parents_children_aboard':'Parents/Children Aboard'},
#   {'passenger_fare':'Fare'}
insert_query = '''INSERT INTO titanic
(survived, passenger_class, full_name, sex, age,
  num_siblings_spouses_aboard, num_parents_children_aboard, 
  passenger_fare) VALUES'''

for row in df:
    insert_query += f'{df}, '

# Replaces the trailing ',' with ';'
insert_query = insert_query.rstrip(',') + ';'

# insert_query = f'''
#     COPY titanic FROM 'titanic.csv' DELIMITER ',' CSV HEADER;
#     '''

# Execute the insert query:
cursor.execute(insert_query)

# Save (commit) the changes:
conn.commit()

# Close the connection:
cursor.close()
conn.close()