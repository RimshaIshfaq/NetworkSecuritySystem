
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://rimshaishfaq86_db_user:<db_password>@cluster0.o4srikh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)