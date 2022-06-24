from bson import ObjectId
from pydantic import BaseModel
import pymongo
from flask import Flask
from fastapi import FastAPI
from requests import request
import uvicorn
from student_schema import Student_se,Student_serial,films_serial,films_schema


client=pymongo.MongoClient("mongodb+srv://mongouser:mongopwd@cluster1.davwpcs.mongodb.net/?retryWrites=true&w=majority")
my_db=client['mydatabase']
Student_collection=my_db['school_registry']
film_collection=my_db['film_collection']

app=FastAPI()

class Student(BaseModel):
    roll_no:int
    name:str
    age:int
    location:str

@app.get('/api/viewAll',tags=['student'])
def view_all():
    try:
        print(Student_serial(Student_collection.find()))
        return  Student_serial(Student_collection.find())
        
    except Exception as e:
        print("error on viewing data " +str(e))

@app.get('/api/viewstudentdetails/{roll_no}',tags=['student'])
def view_student(roll_no):
    try:
        
        output=Student_serial(Student_collection.find({"roll_no":int(roll_no)}))
        return {"status": "ok","data":output}
        
    except Exception as e:
        print("error on viewing data " +str(e))
    

@app.post('/api/adding new student/',tags=['student'])
def add_student(student : Student):
    try:
        Student_collection.insert_one(student.dict())
        return "successfully added"
    except Exception as e:
        print("error on add data " +str(e))


@app.delete('/api/delete student by rollno/{roll_no}',tags=['student'])
def delete_student(roll_no):
    try:
        Student_collection.delete_one({"roll_no":int(roll_no)})
        return "deleted successfully"
    except Exception as e:
        print("error on viewing data " +str(e))


@app.put('/api/update/{roll_no}',tags=["student"])
def update_student(roll_no,student:Student):
    try:
        
        userip=dict(student)
        
        Student_collection.update_many({"roll_no":int(roll_no)},{"$set":userip})

        return Student_serial(Student_collection.find({"roll_no":roll_no}))

    except Exception as e:
        print("error on viewing data " +str(e))


class Films(BaseModel):
    roll_num:int
    title:str
    year:int
    Director:str
    jurner:str

@app.get('/api/view all',tags=['Films'])
def view_all():
    try:
        print(films_serial(film_collection.find()))
        return  films_serial(film_collection.find())

    except Exception as e:
        print("error " +str(e))
        return "failed"


@app.post('/api/adding new film details',tags=['Films'])
def add_new_film(film:Films):
    try:
        film_collection.insert_one(film.dict())
        return "successfully added"
    except Exception as e:
        print("error " +str(e))
        return "failed"

@app.put('/api/updating/{roll_num}',tags=['Films'])
def update_film(roll_num,film:Films):
    try:
        userip=dict(film)
        
        film_collection.update_many({"roll_num":int(roll_num)},{"$set":userip})

        return films_serial(film_collection.find({"roll_num":roll_num}))
        
    except Exception as e:
        print("error " +str(e))
        return "failed"

@app.delete('/api/formating film collection',tags=['Films'])
def format_collection():
    try:
        film_collection.drop()
        return "successfully droped all data"
    except Exception as e:
        print("error " +str(e))
        return "failed"

@app.delete('/api/deleting film{roll_num}',tags=['Films'])
def delete_film(roll_num):
    try:
        film_collection.delete_one({"roll_num":int(roll_num)})
        return "successfully deleted"
    except Exception as e:
        print("error " +str(e))
        return "failed"

if __name__=='__main__':
    uvicorn.run("stu_&_film:app",reload=True,access_log=False)