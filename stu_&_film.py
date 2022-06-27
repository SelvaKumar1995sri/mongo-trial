from bson import ObjectId
from pydantic import BaseModel
import pymongo
from flask import Flask
from fastapi import FastAPI, File, UploadFile
from requests import request
import uvicorn
from student_schema import Student_se, Student_serial, films_serial, films_schema


client = pymongo.MongoClient(
    "mongodb+srv://mongouser:mongopwd@cluster1.davwpcs.mongodb.net/?retryWrites=true&w=majority")
my_db = client['mydatabase']
Student_collection = my_db['school_registry']
film_collection = my_db['film_collection']

app = FastAPI()


class Student(BaseModel):
    roll_no: int
    name: str
    age: int
    location: str


@app.get('/api/viewAll', tags=['student'])
def view_all():
    try:
        output = Student_serial(Student_collection.find())
        if output == []:
            return "No Data exist to view"
        else:
            return {"data": output}

    except Exception as e:
        print("error on viewing data " + str(e))


@app.get('/api/viewstudentdetails/{roll_no}', tags=['student'])
def view_student(roll_no):
    try:
        output = Student_serial(
            Student_collection.find({"roll_no": int(roll_no)}))
        if output == []:
            return "give a valid value to find"

        else:
            return {"status": "ok", "data": output}

    except Exception as e:
        print("error on viewing data " + str(e))


@app.post('/api/adding new student/', tags=['student'])
def add_student(student: Student):
    try:
        Student_collection.insert_one(student.dict())
        return "successfully added"
    except Exception as e:
        print("error on add data " + str(e))


@app.delete('/api/delete student by rollno/{roll_no}', tags=['student'])
def delete_student(roll_no):
    try:
        output = Student_serial(
            Student_collection.find({"roll_no": int(roll_no)}))
        if output == []:
            return "Give vaid roll_no from existing database"
        else:
            Student_collection.delete_one({"roll_no": int(roll_no)})
            return "deleted successfully"

    except Exception as e:
        print("error on viewing data " + str(e))


@app.put('/api/update/{roll_no}', tags=["student"])
def update_student(roll_no, student: Student):
    try:
        list_id = []
        for i in Student_collection.find():
            list_id.append(i["roll_no"])
        max_id = max(list_id)
        userip = dict(student)

        if max_id >= int(roll_no):
            Student_collection.update_one(
                {"roll_no": int(roll_no)}, {"$set": userip})
            return "Updated Successfully"

        else:
            return "Given value not valid ,choose from existing Data "

    except Exception as e:
        print("error on viewing data " + str(e))


class Films(BaseModel):
    Sno: int
    Title: str
    Year: int
    Rated: str
    Released: str
    Runtime: str
    Genre: str
    Director: str
    Writer: str
    Actors: str
    Language: str


@app.get('/api/view all', tags=['Films'])
def view_all():
    try:
        print(films_serial(film_collection.find()))
        return films_serial(film_collection.find())

    except Exception as e:
        print("error " + str(e))
        return "failed"


@app.get('/api/view student/{Sno}', tags=['Films'])
def view_films(Sno: int):
    try:
        list_id = []
        for i in film_collection.find():
            list_id.append(i["Sno"])
        max_id = max(list_id)
        if max_id >= int(Sno):
            output = films_serial(film_collection.find({"Sno": int(Sno)}))
            print(output)
            return {"data": output}
        else:
            return "give a valid roll no"

    except Exception as e:
        print("error " + str(e))
        return "failed"


@app.post('/api/adding new film details', tags=['Films'])
def add_new_film(film: Films):
    try:
        film_collection.insert_one(film.dict())
        return "successfully added"
    except Exception as e:
        print("error " + str(e))
        return "failed"


@app.put('/api/updating/{Sno}', tags=['Films'])
def update_film(Sno, film: Films):
    try:
        list_id = []
        for i in film_collection.find():
            list_id.append(i["Sno"])
        max_id = max(list_id)
        userip = dict(film)

        if max_id >= int(Sno):
            film_collection.update_many(
                {"roll_num": int(Sno)}, {"$set": userip})
            return "Successfully Updated"

        else:
            return "Given roll no not exist, Choose from existing Data to update"

    except Exception as e:
        print("error " + str(e))
        return "failed"


@app.delete('/api/formating film collection', tags=['Films'])
def format_collection():
    try:
        film_collection.drop()
        return "successfully droped all data"
    except Exception as e:
        print("error " + str(e))
        return "failed"


@app.delete('/api/deleting film{Sno}', tags=['Films'])
def delete_film(Sno):
    try:
        if film_collection.delete_one({"roll_num": int(Sno)}):
            return "successfully deleted"

        else:
            return "Give a existing roll no"
    except Exception as e:
        print("error " + str(e))
        return "failed"


@app.get('/api/Filter by Director/{Director}', tags=['Films'])
def list_by_director(Director):
    try:
        d = []
        for i in film_collection.find():
            d.append(i["Director"])

        if Director not in d:
            return "Kindly give existing Film Director name or give valid name"
        else:
            response = films_serial(
                film_collection.find({"Director": Director}))
            return {"data": response}

    except Exception as e:
        print("Error in filtering Director ", +str(e))
        return "failed to filter"


@app.get('/api/Filter by Year/{Year}', tags=['Films'])
def list_by_Year(Year):
    try:
        response = films_serial(film_collection.find({"Year": int(Year)}))
        print(response)
        return {"data": response}
    except Exception as e:
        print("Error in filtering Director ", +str(e))
        return "failed to filter"


@app.get('/api/Filter from Year/{Year}', tags=['Films'])
def list_from_year(Year):
    try:
        year = []
        for y in film_collection.find():
            year.append(y["Year"])
        if max(year) >= int(Year):
            result = films_serial(film_collection.find(
                {'Year': {'$gte': int(Year)}}))
            return {"data": result}
        else:
            return "Give Year value in existing Range"

    except Exception as e:
        print("Error in filtering Director ", +str(e))
        return "failed to filter"

@app.post('/uploadfile',tags=['Films'])
def upload_file(file : UploadFile=File()):
    films_serial(film_collection.insert_one({"file":file}))
    
    return {"name of the file":file.filename}


if __name__ == '__main__':
    uvicorn.run("stu_&_film:app", reload=True, access_log=False)
