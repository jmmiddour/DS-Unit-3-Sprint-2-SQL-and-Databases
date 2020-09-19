# Imports:
import pandas as pd
import sqlite3

# Create a connection to the Database:
conn = sqlite3.connect('rpg_db.sqlite3')

# Look at the connection to verify it is connected:
conn

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

# Q1: How many total Characters are there?
q1 = get_data('''SELECT 
	COUNT(character_id) as Total_Observations,
	COUNT(DISTINCT character_id) as Total_Number_of_Charaters
FROM charactercreator_character''', conn)
print('--> How many total Characters are there?\n', q1, '\n')

# Q2: How many of each specific subclass?
q2 = get_data('''SELECT
	COUNT(DISTINCT charact.character_id) AS Total_Characters,
	COUNT(DISTINCT cleric.character_ptr_id) AS Cleric_Type,
	COUNT(DISTINCT fighter.character_ptr_id) AS Fighter_Type,
	COUNT(DISTINCT mage.character_ptr_id) AS Mage_Type,
	COUNT(DISTINCT thief.character_ptr_id) AS Thief_Type
FROM charactercreator_character AS charact
LEFT JOIN charactercreator_cleric AS cleric 
    ON cleric.character_ptr_id = charact.character_id
LEFT JOIN charactercreator_fighter AS fighter 
    ON fighter.character_ptr_id = charact.character_id
LEFT JOIN charactercreator_mage AS mage 
    ON mage.character_ptr_id = charact.character_id
LEFT JOIN charactercreator_thief AS thief 
    ON thief.character_ptr_id = charact.character_id
''', conn)
print('--> How many of each specific subclass?\n', q2, '\n')

# Q3: How many total Items?
q3 = get_data('''SELECT 
	COUNT(item_id) as Total_Observations,
	COUNT(DISTINCT item_id) as Total_Number_of_Items
FROM armory_item''', conn)
print('--> How many total Items?\n', q3, '\n')

# Q4: How many of the Items are weapons? How many are not?
q4 = get_data('''SELECT 
	COUNT(arm.item_id) AS Total_Number_of_Items,
	COUNT(DISTINCT wep.item_ptr_id) AS Total_Weapons,
	(COUNT(arm.item_id) - COUNT(DISTINCT wep.item_ptr_id)) 
        AS Total_Non_Weapons
FROM armory_item AS arm
LEFT JOIN armory_weapon AS wep 
    ON arm.item_id = wep.item_ptr_id''', conn)
print('--> How many of the Items are weapons? How many are not?\n', q4, '\n')

# Q5: How many Items does each character have? (Return first 20 rows)
q5 = get_data('''SELECT
    ch.character_id AS Character_ID,
	ch.name AS Character_Name,
	COUNT(DISTINCT inv.item_id) AS Total_Items
FROM charactercreator_character AS ch
LEFT JOIN charactercreator_character_inventory AS inv 
    ON inv.character_id = ch.character_id
GROUP BY Character_Name
LIMIT 20''', conn)
print('--> How many Items does each\
 character have? (Return first 20 rows)\n', q5, '\n')

# Q6: How many Weapons does each character have? (Return first 20 rows)
q6 = get_data('''SELECT
    ch.character_id AS Character_ID,
	ch.name AS Character_Name,
	COUNT(DISTINCT inv.item_id) AS Total_Items,
	COUNT(DISTINCT wep.item_ptr_id) AS Total_Weapons
FROM charactercreator_character AS ch
LEFT JOIN charactercreator_character_inventory AS inv 
    ON inv.character_id = ch.character_id
LEFT JOIN armory_item AS arm ON arm.item_id = inv.character_id
LEFT JOIN armory_weapon AS wep ON wep.item_ptr_id = arm.item_id
GROUP BY Character_Name
LIMIT 20''', conn)
print('--> How many Weapons does each\
 character have? (Return first 20 rows)\n', q6, '\n')

# Q7: On average, how many Items does each Character have?
q7 = get_data('''
SELECT AVG(Total_Items) AS Average_Items_Per_Character
FROM (SELECT 
    ch.character_id AS Character_ID,
    ch.name AS Character_Name,
	COUNT(DISTINCT inv.item_id) AS Total_Items
	FROM charactercreator_character AS ch
	LEFT JOIN charactercreator_character_inventory AS inv 
        ON inv.character_id = ch.character_id
	GROUP BY Character_Name);''', conn)
print('--> On average, how many Items does each\
 Character have?\n', q7, '\n')

# Q8: On average, how many Weapons does each character have?
q8 = get_data('''
SELECT AVG(Total_Weapons) AS Avgerage_Weapons_Per_Character
FROM (SELECT
    ch.character_id AS Character_ID,
	ch.name AS Character_Name,
	COUNT(DISTINCT inv.item_id) AS Total_Items,
	COUNT(DISTINCT wep.item_ptr_id) AS Total_Weapons
FROM charactercreator_character AS ch
LEFT JOIN charactercreator_character_inventory AS inv 
    ON inv.character_id = ch.character_id
LEFT JOIN armory_item AS arm ON arm.item_id = inv.character_id
LEFT JOIN armory_weapon AS wep ON wep.item_ptr_id = arm.item_id
GROUP BY Character_Name);''', conn)
print('--> On average, how many Weapons does each\
 character have?\n', q8)
