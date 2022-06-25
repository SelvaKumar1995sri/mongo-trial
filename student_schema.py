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
        "Sno":int(film["Sno"]),
        "Title": str(film["Title"]),
        "Year": int(film["Year"]),
        "Rated": str(film["Rated"]),
        "Released": str(film["Released"]),
        "Runtime": str(film["Runtime"]),
        "Genre": str(film["Genre"]),
        "Director": str(film["Director"]),
        "Writer": str(film["Writer"]),
        "Actors": str(film["Actors"]),
        "Language": str(film["Language"])
    }

def films_serial(films):
    return [films_schema(film) for film in films]