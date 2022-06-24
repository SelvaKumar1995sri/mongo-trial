def Student_se(Student):
    return {
        "roll_no":int(Student["roll_no"]),
        "name":str(Student["name"]),
        "age":int(Student["age"]),
        "location":str(Student["location"])
    }

def Student_serial(Students):
    return [Student_se(Student) for Student in Students]


def films_schema(film):
    return {
        "roll_num":int(film["roll_num"]),
        "title":str(film["title"]),
        "year":int(film["year"]),
        "Director":str(film["Director"]),
        "jurner":str(film["jurner"])
    }

def films_serial(films):
    return [films_schema(film) for film in films]