import pymongo
try:
    myclient=pymongo.MongoClient("mongodb+srv://selvamongouser:Selvamongopassword@cluster0.fvlkt0v.mongodb.net/?retryWrites=true&w=majority")
    dblist=myclient.list_database_names()[0]
    
    print(dblist)

except Exception as e:
    print("error ",str(e))