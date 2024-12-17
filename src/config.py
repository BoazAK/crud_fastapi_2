import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from the .env file
load_dotenv()

variable_name = "ENVIRONMENT"  # Replace with the name of the environment variable you want to access
value = os.environ.get(variable_name)

# Determine the prefix based on the value of 'value'
if value.lower() == "prod":
    prefix = "PROD_"
elif value.lower() == "test":
    prefix = "TEST_"
else:
    prefix = ""

# Use the prefix to access the environment variable with the corresponding key
uri = os.getenv(f"{prefix}DB_URI")
ENV = os.getenv(f"{prefix}ENV")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)