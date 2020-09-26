'''
Setup
Before we get started you'll need a few things.
Download the Chinook Database
Create a file named study_part2.py and complete the exercise below.
The only library you should need to import is sqlite3.
Don't forget to be PEP8 compliant!
'''
import os
import sqlite3

# Add a connection to the chinook database to answer the queries below.
conn_path = os.path.join(os.path.dirname(__file__), "Chinook_Sqlite.sqlite")
conn = sqlite3.connect(conn_path)
cursor = conn.cursor()

# Queries:
# Single Table Queries
# 1. Find the average invoice total for each customer,
#    return the details for the first 5 ID's
avg_inv_query = '''
SELECT CustomerId, AVG(Total)
FROM Invoice
GROUP BY CustomerId
LIMIT 5;
'''
avg_inv = cursor.execute(avg_inv_query).fetchall()
print('\nAverage Invoice Total Per Customer ID\n', avg_inv, '\n')

# 2. Return all columns in Customer for the first 5 customers
#    residing in the United States
usa_cust_query = '''
SELECT *
FROM Customer
WHERE Country == 'USA'
LIMIT 5;
'''
usa_cust = cursor.execute(usa_cust_query).fetchall()
print('First 5 Customers in the USA:\n', usa_cust, '\n')

# 3. Which employee does not report to anyone?
doesnt_report_query = '''
SELECT FirstName || ' ' || LastName
FROM Employee
WHERE ReportsTo IS NULL;
'''
doesnt_report = cursor.execute(doesnt_report_query).fetchone()
print('Employee that does not report to anyone =', doesnt_report, '\n')

# 4. Find the number of unique composers
composers_query = '''
SELECT COUNT(DISTINCT Composer) AS num_of_unique_composers
FROM Track
WHERE Composer IS NOT NULL;
'''
composers = cursor.execute(composers_query).fetchone()
print('The number of Unique Composers =', composers, '\n')

# 5. How many rows are in the Track table?
track_rows_query = '''
SELECT COUNT(*) AS num_of_track_rows FROM Track;
'''
track_rows = cursor.execute(track_rows_query).fetchone()
print('Number of Rows in the Track table =', track_rows, '\n')

# Joins:
# 6. Get the name of all Black Sabbath tracks and the albums they came off of
black_sab_query = '''
SELECT t.Name AS track_name, a.Title AS album_title
FROM Track AS t
LEFT JOIN Album AS a ON t.AlbumId = a.AlbumId
WHERE a.ArtistId == 12;
'''
black_sab = cursor.execute(black_sab_query).fetchall()
print('Black Sabbath tracks and the Album Name:\n', black_sab, '\n')

# 7. What is the most popular genre by number of tracks?
pop_genre_query = '''
SELECT g.Name AS genre_name, COUNT(t.GenreId) AS num_of_tracks
FROM Track AS t
LEFT JOIN Genre AS g ON t.GenreId = g.GenreId
GROUP BY t.GenreId
ORDER BY num_of_tracks DESC
LIMIT 1;
'''
pop_genre = cursor.execute(pop_genre_query).fetchone()
print('Most popular Genre based on number of tracks =', pop_genre, '\n')

# 8. Find all customers that have spent over $45
over_45_query = '''
SELECT i.CustomerId, c.LastName, c.FirstName, SUM(i.Total) AS total_spent
FROM Customer AS c
LEFT JOIN Invoice AS i ON c.CustomerId = i.CustomerId
GROUP BY i.CustomerId
HAVING total_spent >= 45;
'''
over_45 = cursor.execute(over_45_query).fetchall()
print('Customers who spent over $45 total:\n', over_45, '\n')

# 9. Find the first and last name, title, and the number of customers
#    each employee has helped. If the customer count is 0 for an
#    employee, it doesn't need to be displayed. Order the employees
#    from most to least customers.
cust_emps_helped_query = '''
SELECT e.FirstName || ' ' || e.LastName, e.Title,
    COUNT(DISTINCT c.CustomerId) AS total_customers
FROM Employee AS e
JOIN Customer AS c ON c.SupportRepId = e.EmployeeId
GROUP BY c.SupportRepId
ORDER BY total_customers DESC;
'''
cust_emps_helped = cursor.execute(cust_emps_helped_query).fetchall()
print('Number of Customers each Employee helped:\n', cust_emps_helped, '\n')

# 10. Return the first and last name of each employee and who they report to
emp_boss_query = '''
SELECT e1.FirstName AS employee_first_name, e1.LastName AS employee_last_name,
    e2.FirstName || ' ' || e2.LastName AS reports_to
FROM Employee AS e1
LEFT JOIN Employee AS e2 ON e2.EmployeeId = e1.ReportsTo
WHERE e1.ReportsTo == e2.EmployeeId;
'''
emp_boss = cursor.execute(emp_boss_query).fetchall()
print('Employee First and Last Name and who they report to:\n', emp_boss)

conn.commit()
cursor.close()
conn.close()
