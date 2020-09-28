'''
Part 1 - Making and Populating a Database
'''
import sqlite3

# Open a connection to a blank database "demo_data.sqlite3"
conn = sqlite3.connect('demo_data.sqlite3')

# Make a cursor
cursor = conn.cursor()

# Execute a statement to prevent duplicates inserted into table
cursor.execute('DROP TABLE IF EXISTS demo;')

# Create a table "demo"
create_demo_table_query = '''
CREATE TABLE demo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    s VARCHAR(1),
    x INT,
    y INT
);
'''
cursor.execute(create_demo_table_query)
conn.commit()

# Insert values into demo table
insert_demo_values = '''
INSERT INTO demo(s, x, y)
VALUES('g', 3, 9),
      ('v', 5, 7),
      ('f', 8, 7);
'''
cursor.execute(insert_demo_values)
conn.commit()

# How many rows in demo table?
row_count_query = '''
SELECT COUNT(*) FROM demo;
'''
row_count = cursor.execute(row_count_query).fetchall()
print('\nNumber of rows in demo table =', row_count, '\n')

# How many rows are there where both x and y are at least 5?
five_or_more_query = '''
SELECT *
FROM demo
WHERE x >= 5 AND y >= 5;
'''
five_or_more = cursor.execute(five_or_more_query).fetchall()
print('Rows where x and y are at least 5:\n', five_or_more, '\n')

# How many unique values of y are there?
unique_y_query = '''
SELECT COUNT(DISTINCT y) FROM demo;
'''
unique_y = cursor.execute(unique_y_query).fetchall()
print('Number of unique values in y column =', unique_y, '\n')

conn.commit()
cursor.close()
conn.close()
