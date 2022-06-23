from pydantic import BaseModel
import pymongo
from flask import Flask
from fastapi import FastAPI
from requests import request
import uvicorn



client=pymongo.MongoClient("mongodb+srv://mongouser:mongopwd@cluster1.davwpcs.mongodb.net/?retryWrites=true&w=majority")
mydata=client['mydatabase']
mycollection=mydata['school_registry']

app=FastAPI()

class Student(BaseModel):
    roll_no:int
    name:str
    age:int
    location:str



@app.post('/api/addstudent/',tags=['Add student details'])
def add_det(student : Student):
    
    mycollection.insert_one(student.dict())
    return "successfully added"

@app.delete('/api/deletestudent/{roll_id}',tags=['Delete student details'])
def delete_det(roll_id):
    print(roll_id)
    print(type(roll_id))
    mycollection.delete_one({"roll_no":int(roll_id)})
    return "deletd added"



if __name__=='__main__':
    uvicorn.run("fastapi_school_reg:app",reload=True,access_log=False)