import pymongo
import json
client=pymongo.MongoClient("mongodb+srv://gayathri:Sairambaba@cluster1.davwpcs.mongodb.net/?retryWrites=true&w=majority")

mydb=client['mydatabase']
mycol=mydb['film_collection']
print(mydb.list_collection_names())