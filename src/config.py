import os
from dotenv import load_dotenv
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
import motor.motor_asyncio

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
URL = os.getenv("DB_URI")
ENV = os.getenv(f"{prefix}ENV")
DB_COLLECTION = os.getenv(f"{prefix}DB_COLLECTION")

# Connection to MongoDB database
client = motor.motor_asyncio.AsyncIOMotorClient(URL)

# Create simple collection
db = client[DB_COLLECTION]

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# db = client

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)