from pydantic import BaseModel
import pymongo
from flask import Flask
from fastapi import FastAPI
from requests import request
import uvicorn
import student_schema


client=pymongo.MongoClient("mongodb+srv://mongouser:mongopwd@cluster1.davwpcs.mongodb.net/?retryWrites=true&w=majority")
mydata=client['mydatabase']
mycollection=mydata['school_registry']

app=FastAPI()

class Student(BaseModel):
    roll_no:int
    name:str
    age:int
    location:str

@app.get('/api/viewstudentdetails/{roll_no}',tags=['student'])
def view_det(roll_no):
    try:
        
        output=mycollection.find({"roll_no":int(roll_no)})
        print(type(roll_no))
        return student_schema(output)
        
    except Exception as e:
        print("error on viewing data " +str(e))
    

@app.post('/api/addstudent/',tags=['student'])
def add_det(student : Student):
    try:
        mycollection.insert_one(student.dict())
        return "successfully added"
    except Exception as e:
        print("error on add data " +str(e))


@app.delete('/api/deletestudent/{roll_no}',tags=['student'])
def delete_det(roll_no):
    try:
        mycollection.delete_one({"roll_no":int(roll_no)})
        return "deleted successfully"
    except Exception as e:
        print("error on viewing data " +str(e))


@app.put('/api/update/{roll_no}',tags=["student"])
def update(roll_no,student:Student):
    try:
        myquery=dict(mycollection.find({"roll_no":roll_no}))
        print(myquery)
        newval=student
        output=mycollection.update_one(myquery,newval)
        return "successfull"
    except Exception as e:
        print("error on viewing data " +str(e))

if __name__=='__main__':
    uvicorn.run("fastapi_school_reg:app",reload=True,access_log=False)