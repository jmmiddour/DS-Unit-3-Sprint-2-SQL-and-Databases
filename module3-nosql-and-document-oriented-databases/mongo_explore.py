'''
Getting started with MongoDB Atlas:
- Create a new Project
- Build a Cluster
 - Put in your organization
 - Add your project name
 - Select your programming language (Python)
 - Choose your cluster type (free)
 - Choose your cloud provider and region (AWS, Virginia)
- Once finished creating your cluster:
 - Click Connect
  - Whitelist a connection (Allow Access from Anywhere)
   - Click the link to IP Whitelists tab to verify it was created
  - Create a Database User (Username and Password)
   - Click on show password and copy it to paste in .env file
   - Add your credentials to your .env file (user, password, cluster)
 - Choose a connection method (Connect your application)
  - Select driver and version (Python 3.6 or later)
  - Need to copy the top line (client) in your connection string
 - Click on collections
  - Load sample dataset for now.
'''

# import pandas as pd
import os
from pdb import set_trace as breakpoint
import json
from dotenv import load_dotenv
import pymongo
import pandas as pd

# Load contents of .env file:
load_dotenv()

# Create variables for connecting to MongoDB:
MONGO_USER = os.getenv('MONGO_USER', default='OOPS')
MONGO_PASS = os.getenv('MONGO_PASS', default='OOPS')
MONGO_CLUST = os.getenv('MONGO_CLUST', default='OOPS')

uri = f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_CLUST}?retryWrites=true&w=majority'
client = pymongo.MongoClient(uri)
print('\n', 'URI:', uri, '\n')

# To view your MongoDB Client information
print(client, '\n')

# To view all the methods in the client class:
print(dir(client), '\n')

# View all database within the cluster:
print('Databases in my Cluster', client.list_database_names(), '\n')

# Set the DB to the sample_analytics DB
analytics_db = client.sample_analytics
print('Sample Analytics Collections: ',
      analytics_db.list_collection_names(), '\n')

# Access a specific collection
transactions = analytics_db.transactions

# Get the count of the documents(rows) in the collection(table)
# Filter is required, for an empty filter use {}
# # count_documents is like "SELECT COUNT(*)"
print('Number of Documents (rows) =', transactions.count_documents({}), '\n')

# How many customers have more than 50 transactions
print('Customers with more than 50 transactions =',
      transactions.count_documents({'transaction_count': {'$gt': 50}}), '\n')

# Get all the customers into a DataFrame:
customers = analytics_db.customers
all_customers = customers.find()  # find is like "SELECT * FROM customers"
# ^-- If you wanted to add a condition... find({condition goes here})
# If you use find_one(), it is like using "LIMIT 1"
df = pd.DataFrame(all_customers)
print('New All Customers DataFrame\n', df.head(), '\n')
print('Column list of Customer DataFrame\n', df.columns, '\n')

# Add 1 new column to the DataFrame if it does not exist:
# This can cause a problem because how easy it can be added,
#  when someone might think they are just adding a record.
# In RDBMS it will throw an error if you tried this.
customers.insert_one({'full_name': 'Bruno Janota'})

# ------> Write JSON Data from RPG DB to MongoDB <------ #

# Read the JSON file
with open('./module3-nosql-and-document-oriented-databases/test_data_json.txt') as json_file:
    rpg_data = json.load(json_file)

# Create a new database named rpg_data
my_db = client.rpg_data

# Create a characters collection in the rpg_data DB
character_table = my_db.characters

# Insert the JSON data into characters collection
character_table.insert_many(rpg_data)
print('Number of rows in Character Table =', 
      character_table.count_documents({}))
