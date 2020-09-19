# Imports:
import pandas as pd
import sqlite3

# Create a connection to a new sqlite data base:
conn = sqlite3.connect('buddymove_holidayiq.sqlite3')

# Read in the csv file:
buddy = pd.read_csv('buddymove_holidayiq.csv')
print(buddy.head())

# Insert data into a new table in the sqlite3 database:
buddy.to_sql('review', conn, if_exists='replace', index=False)

# Create a function to get data from a SQLite Data Base:
def get_data(query, conn):
    '''
    This function will retrive the data from a SQLite data base and
    turn it into a pandas DataFrame for easier readablility and to
    make it easier to work with.
    '''
    # Instanstiate the cursor object and get the results:
    cursor = conn.cursor()
    results = cursor.execute(query).fetchall()
    
    # Get the columns from the cursor object:
    cols = list(map(lambda x: x[0], cursor.description))
    
    # Assign it to a pandas DataFrame:
    df = pd.DataFrame(data=results, columns=cols)
    return df

# Q1: How many rows:
q1 = get_data('''
SELECT COUNT(*) AS Total_Number_of_Rows
FROM review;''', conn)
print('--> How many rows in the table?\n', q1, '\n')

# Q2: How many users who reviewed at least 100 in Nature 
#   and Shopping category?
q2 = get_data('''SELECT COUNT(*) AS Num_of_Nature_and_Shopping_100_or_More
FROM review 
WHERE Nature >= 100 
	AND Shopping >= 100;''', conn)
print('--> How many users who reviewed at least 100 in Nature\
 and Shopping categories?\n', q2, '\n')


# Q3: What are the average number of reviews for each category?
q3 = get_data('''SELECT
	AVG(Sports) AS Sports_Average,
	AVG(Religious) AS Religious_Average,
	AVG(Nature) AS Nature_Average,
	AVG(Theatre) AS Theatre_Average,
	AVG(Shopping) AS Shopping_Average,
	AVG(Picnic) AS Picnic_Average
FROM review;''', conn)
print('What is the avereage number of reviews for\
 each category?\n', q3)
