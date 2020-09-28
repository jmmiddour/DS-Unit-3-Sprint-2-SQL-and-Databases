'''
Part 2 - The Northwind Database
'''
import sqlite3

# Create a connection to the database
conn = sqlite3.connect('northwind_small.sqlite3')
cursor = conn.cursor()

# View all the tables available in northwind_small
view_tables = cursor.execute("SELECT name FROM sqlite_master \
WHERE type='table' ORDER BY name;").fetchall()
print('\nAll tables available in northwind_small:\n',
      view_tables, '\n')

# View the CREATE TABLE statement
create_stmnt = cursor.execute('SELECT sql FROM sqlite_master \
WHERE name="Customer";').fetchall()
print('CREATE TABLE statement:\n', create_stmnt, '\n')

# What are the ten most expensive items (per unit price) in the database?
ten_most_expensive_query = '''
SELECT Id, ProductName, UnitPrice
FROM Product
ORDER BY UnitPrice DESC
LIMIT 10;
'''
ten_most_expensive = cursor.execute(ten_most_expensive_query).fetchall()
print('Top 10 most expensive products by unit price:\n', ten_most_expensive, '\n')

# What is the average age of an employee at the time of their hiring?
avg_age_at_hiring_query = '''
SELECT AVG(HireDate - BirthDate)
FROM Employee;
'''
avg_age_at_hiring = cursor.execute(avg_age_at_hiring_query).fetchall()
print('Average employee age at time of hiring =', avg_age_at_hiring, '\n')

# (Stretch) How does the average age of employee at hire vary by city?
avg_age_by_city_query = '''
SELECT AVG(HireDate - BirthDate), City
FROM Employee
GROUP BY City;
'''
avg_age_by_city = cursor.execute(avg_age_by_city_query).fetchall()
print('Average age of employee on hire date by city:\n',
      avg_age_by_city, '\n')

'''
Part 3 - Sailing the Northwind Seas
'''
# What are the ten most expensive items (per unit price)
#   in the database and their suppliers?
ten_exp_supp_query = '''
SELECT p.ProductName, p.UnitPrice, s.CompanyName
FROM Product p
LEFT JOIN Supplier s ON p.SupplierId = s.Id
ORDER BY UnitPrice DESC
LIMIT 10;
'''
ten_exp_supp = cursor.execute(ten_exp_supp_query).fetchall()
print('Top 10 most expensive products (unit price) and suppliers:\n',
      ten_exp_supp, '\n')

# What is the largest category (by number of unique products in it)?
lrgst_unique_cat_query = '''
SELECT c.CategoryName, COUNT(p.Id) AS ProductCount
FROM Product p
LEFT JOIN Category c ON p.CategoryId = c.Id
GROUP BY c.CategoryName
ORDER BY ProductCount
LIMIT 1;
'''
lrgst_unique_cat = cursor.execute(lrgst_unique_cat_query).fetchall()
print('Largest category by number of unique products =',
      lrgst_unique_cat, '\n')

# (Stretch) Who's the employee with the most territories?
emp_most_terr_query = '''
SELECT e.FirstName || ' ' || e.LastName AS FullName,
    COUNT(et.TerritoryId) AS num_of_territories
FROM Employee e
LEFT JOIN EmployeeTerritory et ON e.Id = et.EmployeeId
ORDER BY num_of_territories DESC
LIMIT 1;
'''
emp_most_terr = cursor.execute(emp_most_terr_query).fetchall()
print('Employee with the most territories =', emp_most_terr)

conn.commit()
cursor.close()
conn.close()
