from bson import ObjectId
from pydantic import BaseModel
import pymongo
from flask import Flask
from fastapi import FastAPI
from requests import request
import uvicorn
from student_schema import Student_se,Student_serial


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
        
        output=Student_serial(mycollection.find({"roll_no":int(roll_no)}))
        return {"status": "ok","data":output}
        
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
def update(roll_no:str,student:Student):
    try:
        mycollection.find_one_and_update({"roll_no":ObjectId(roll_no)},{
            "$set":dict(student)
        })
        output=mycollection.find({"roll_no":ObjectId(roll_no)})
        return {"status": "ok","data":output}
    except Exception as e:
        print("error on viewing data " +str(e))

if __name__=='__main__':
    uvicorn.run("fastapi_school_reg:app",reload=True,access_log=False)