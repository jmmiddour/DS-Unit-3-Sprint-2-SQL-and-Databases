import os
import pandas as pd
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values
# import csv
# from pdb import set_trace as breakpoint

# Load contents of .env file:
load_dotenv()

# Create variables for connecting to ElephantSQL:
DB_NAME=os.getenv('DB_NAME')
DB_USER=os.getenv('DB_USER')
DB_PASS=os.getenv('DB_PASS')
DB_HOST=os.getenv('DB_HOST')

# print(DB_NAME, DB_USER, DB_PASS, DB_HOST) <-- Already checked out good

# Connect to my database where adding the new table:
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
# print(conn) <-- Already checked out good

# Create cursor object:
cursor = conn.cursor()
# print(type(cursor)) <-- Already checked out good

# Create a variable for the file path to csv file:
csv_path = os.path.join(os.path.dirname(__file__), "titanic.csv")

# Read in the titanic.csv file:
df = pd.read_csv(csv_path)
# print(df.columns.tolist())

df["Survived"] = df["Survived"].values.astype(bool)
df = df.astype("object")
df['Pclass'] = df['Pclass'].replace([1, 2, 3], ['upper', 'middle', 'lower'])

# Convert dataframe to a list of tuples:
titanic = list(df.to_records(index=False))

# Create a table to upload the data from the titanic csv file:
create_titanic_table='''DROP TYPE IF EXISTS PCLASS CASCADE;
DROP TABLE IF EXISTS titanic;
CREATE TYPE PCLASS AS ENUM ('upper', 'middle', 'lower');
CREATE TABLE titanic (
    "record_id" SERIAL PRIMARY KEY,
    "survived" BOOL,
    "passenger_class" PCLASS,
    "full_name" VARCHAR(250),
    "sex" VARCHAR(7),
    "age" DECIMAL(3, 1),
    "num_siblings_spouses_aboard" INT,
    "num_parents_children_aboard" INT,
    "passenger_fare" DECIMAL
    );
    '''

# Execute the above statement:
cursor.execute(create_titanic_table)

# Commit the changes:
conn.commit()

# Insert data into the table:
#   {'survived':'Survived'}, 
#   {'passenger_class':'Pclass}, {'full_name':'Name'},
#   {'sex':'Sex'}, {'age':'Age'}, 
#   {'num_siblings_spouses_aboard':'Siblings/Spouses Aboard'},
#   {'num_parents_children_aboard':'Parents/Children Aboard'},
#   {'passenger_fare':'Fare'}
insert_query = '''
INSERT INTO titanic
(survived, passenger_class, full_name, sex, age,
  num_siblings_spouses_aboard, num_parents_children_aboard, 
  passenger_fare) VALUES %s
  '''

# # Iterate through the rows to get all data
# for row in titanic:
#   insert_query += f' {titanic}, '

# # Replaces the trailing ',' with ';'
# insert_query = insert_query.rstrip(',') + ';'

# Execute the values:
execute_values(cursor, insert_query, titanic)

# Save (commit) the changes:
conn.commit()  

# Close the connection:
cursor.close()
conn.close()
