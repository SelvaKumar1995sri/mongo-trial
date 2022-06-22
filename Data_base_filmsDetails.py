import pymongo
import json
#client=pymongo.MongoClient("mongodb+srv://selvamongouser:Selvamongopassword@cluster0.fvlkt0v.mongodb.net/?retryWrites=true&w=majority")

db=open("film_database.json",'r')
data_list=json.load(db)['database']

for i in data_list:
    print()