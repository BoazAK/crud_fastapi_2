import os
from dotenv import load_dotenv

# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
import motor.motor_asyncio

# Load environment variables from the .env file
load_dotenv()

variable_name = "ENVIRONMENT"  # Replace with the name of the environment variable you want to access
value = str(os.environ.get(variable_name))

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
DOMAIN_NAME = os.getenv(f"{prefix}DOMAIN_NAME")
PORT = os.getenv(f"{prefix}PORT")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")

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
