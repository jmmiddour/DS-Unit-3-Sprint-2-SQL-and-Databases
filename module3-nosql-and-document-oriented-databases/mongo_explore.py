# import pandas as pd
import os
from dotenv import load_dotenv
import pymongo
# import psycopg2
# import csv

# Load contents of .env file:
load_dotenv()

# Create variables for connecting to MongoDB:
MONGO_USER = os.getenv('MONGO_USER', default='OOPS')
MONGO_PASS = os.getenv('MONGO_PASS', default='OOPS')
MONGO_CLUST = os.getenv('MONGO_CLUST', default='OOPS')

uri = f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_CLUST}?retryWrites=true&w=majority'
client = pymongo.MongoClient(uri)
print('URI:', uri)
