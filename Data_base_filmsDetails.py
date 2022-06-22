import pymongo
from flask import Flask,request


client=pymongo.MongoClient("mongodb+srv://gayathri:Sairambaba@cluster1.davwpcs.mongodb.net/?retryWrites=true&w=majority")
mydb=client['mydatabase']
mycol=mydb['film_collection']

app=Flask(__name__)

@app.route('/addfilm',methods=['post'])
def add_films():
    try:
        val=request.get_json()
        mycol.insert_many(val)

        return "Added successfully"

    except Exception as e:
        print("error accures :" +str(e))

@app.route('/update',methods=['put'])
def update_films():
    try:
        val=request.get_json("_id")
        curser=mycol.find()
        for doc in curser:
            if doc['_id']==val: 
                j=doc['year']
                myq={"year":j}
                newj={"$set":{"year":"2017"}}
                mycol.update_one(myq,newj)

        return "success"

    except Exception as e:
        print("Error on updating :" +str(e))

@app.route('/delete',methods=['get','delete'])
def delete_films():
    try:
        val=request.get_json('title')
        curser=mycol.find()
        for i in curser:
            if i['title']==val:
                mycol.delete_one(i)
        
        
        return "success"

    except Exception as e:
        print("Error on updating :" +str(e))





if __name__=='__main__':
   app.run(debug=True)