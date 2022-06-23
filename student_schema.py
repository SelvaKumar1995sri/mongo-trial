def Student_se(Student):
    return {
        "roll_no":int(Student["roll_no"]),
        "name":str(Student["name"]),
        "age":int(Student["age"]),
        "location":str(Student["location"])
    }

def Student_serial(Students):
    return [Student_se(Student) for Student in Students]