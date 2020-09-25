import sqlite3
'''
Create a file named study_part1.py and complete the exercise below. 
The only library you should need to import is sqlite3. 
Don't forget to be PEP8 compliant!
Create a new database file call study_part1.sqlite3
Create a table with the following columns
 student - string
 studied - string
 grade - int
 age - int
 sex - string
​
Fill the table with the following data​
 'Lion-O', 'True', 85, 24, 'Male'
 'Cheetara', 'True', 95, 22, 'Female'
 'Mumm-Ra', 'False', 65, 153, 'Male'
 'Snarf', 'False', 70, 15, 'Male'
 'Panthro', 'True', 80, 30, 'Male'
​
Save your data. You can check that everything is working so far if you can view the table 
and data in DBBrowser​
Write the following queries to check your work. Querie outputs should be formatted 
for readability, don't simply print a number to the screen with no explanation, add context.​
 What is the average age? Expected Result - 48.8
 What are the name of the female students? Expected Result - 'Cheetara'
 How many students studied? Expected Results - 3
 Return all students and all columns, sorted by student names in alphabetical order.
 '''

conn = sqlite3.connect('study_part1.sqlite3')

cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student VARCHAR(80),
    studied TEXT,
    grade INT,
    age INT,
    sex VARCHAR(20)
)
'''

cursor.execute(create_table_query)

sample_data = [
    ('Lion-O', 'True', 85, 24, 'Male'),
    ('Cheetara', 'True', 95, 22, 'Female'),
    ('Mumm-Ra', 'False', 65, 153, 'Male'),
    ('Snarf', 'False', 70, 15, 'Male'),
    ('Panthro', 'True', 80, 30, 'Male')
 ]

for row in sample_data:
    insert_query = f'''INSERT INTO students (student, studied, grade, age, sex) 
    VALUES {row}'''
    cursor.execute(insert_query)
conn.commit()

# Answer 3 Questions...

cursor.close()
conn.close()