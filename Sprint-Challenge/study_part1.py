import os
import sqlite3
'''
Create a file named study_part1.py and complete the exercise below.
The only library you should need to import is sqlite3.
Don't forget to be PEP8 compliant!
Create a new database file call study_part1.sqlite3
'''
conn_path = os.path.join(os.path.dirname(__file__), "study_part1.sqlite3")
conn = sqlite3.connect(conn_path)
cursor = conn.cursor()
'''
Create a table with the following columns
 student - string
 studied - string
 grade - int
 age - int
 sex - string
'''
create_table_query = '''
CREATE TABLE students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student VARCHAR(80),
    studied TEXT,
    grade INT,
    age INT,
    sex VARCHAR(20));
'''
cursor.execute('DROP TABLE IF EXISTS students;')
cursor.execute(create_table_query)

# Fill the table with the following data​
#  'Lion-O', 'True', 85, 24, 'Male'
#  'Cheetara', 'True', 95, 22, 'Female'
#  'Mumm-Ra', 'False', 65, 153, 'Male'
#  'Snarf', 'False', 70, 15, 'Male'
#  'Panthro', 'True', 80, 30, 'Male'

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
'''
Save your data. You can check that everything is working so far if you can
view the table and data in DBBrowser.

Write the following queries to check your work. Query outputs should be
formatted for readability, don't simply print a number to the screen with
no explanation, add context.
'''
# What is the average age? Expected Result - 48.8
avg_age_query = '''
SELECT AVG(age) AS average_student_age
FROM students
'''
avg_age = cursor.execute(avg_age_query).fetchone()
print('\nAverage Age of Students =', avg_age, '\n')

# What is the name of the female students? Expected Result - 'Cheetara'
female_query = '''
SELECT student AS Female_Student
FROM students
WHERE sex == 'Female'
'''
female = cursor.execute(female_query).fetchone()
print('Name of the Female Student =', female, '\n')

# How many students studied? Expected Results - 3
studied_query = '''
SELECT COUNT(student) AS Count_of_Students_Who_Studied
FROM students
WHERE studied == 'True'
'''
studied = cursor.execute(studied_query).fetchone()
print('Number of Students who Studied =', studied, '\n')

# Return all students and all columns, sorted by student names
#   in alphabetical order.
sorted_students = '''
SELECT *
FROM students
ORDER BY student
'''
sorted_stud = cursor.execute(sorted_students).fetchall()
print('All Students sorted Alphabetically:\n', sorted_stud)

conn.commit()
cursor.close()
conn.close()
