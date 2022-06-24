from bson import ObjectId
from pydantic import BaseModel
import pymongo
from flask import Flask
from fastapi import FastAPI
from requests import request
import uvicorn
from student_schema import Student_se,Student_serial,films_serial,films_schema


client=pymongo.MongoClient("mongodb+srv://mongouser:mongopwd@cluster1.davwpcs.mongodb.net/?retryWrites=true&w=majority")
mydata=client['mydatabase']
mycollection=mydata['school_registry']
mycol=mydata['film_collection']

app=FastAPI()

class Student(BaseModel):
    roll_no:int
    name:str
    age:int
    location:str

@app.get('/api/viewAll',tags=['student'])
def view_all():
    try:
        print(Student_serial(mycollection.find()))
        return  Student_serial(mycollection.find())
        
    except Exception as e:
        print("error on viewing data " +str(e))

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
def update(roll_no,student:Student):
    try:
        
        userip=dict(student)
        
        mycollection.update_many({"roll_no":int(roll_no)},{"$set":userip})

        return Student_serial(mycollection.find({"roll_no":roll_no}))

    except Exception as e:
        print("error on viewing data " +str(e))


class Films(BaseModel):
    roll_num:int
    title:str
    year:int
    Director:str
    jurner:str

@app.get('/api/viewall',tags=['Films'])
def viewall():
    try:
        films_serial(mycollection.find())
        return films_serial(mycollection.find())

    except Exception as e:
        print("error " +str(e))
        return "failed"


@app.post('/api/add',tags=['Films'])
def add(film:Films):
    try:
        mycol.insert_one(film.dict())
        return "successfully added"
    except Exception as e:
        print("error " +str(e))
        return "failed"



@app.delete('/api/drop',tags=['Films'])
def delete():
    try:
        mycol.drop()
        return "successfully droped all data"
    except Exception as e:
        print("error " +str(e))
        return "failed"

@app.put('/api/update/{roll_num}',tags=['Films'])
def update(roll_num,film:Films):
    try:
        userip=dict(film)
        
        mycol.update_many({"roll_num":int(roll_num)},{"$set":userip})

        return films_serial(mycollection.find({"roll_num":roll_num}))
        
    except Exception as e:
        print("error " +str(e))
        return "failed"


if __name__=='__main__':
    uvicorn.run("stu_&_film:app",reload=True,access_log=False)