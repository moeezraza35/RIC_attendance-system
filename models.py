from mysql.connector import connect
import json

dataFile = open("settings.json","rt")
jsonData = dataFile.read()
data = json.loads(jsonData)

db_data = {
    "host":data["host"],
    "user":data["user"],
    "password":data["password"],
    "database":data["database"]
}

class model:
    name = ""
    columns=[]
    def __init__(self) -> None:
        self.db = connect(
            host=db_data["host"],
            user=db_data["user"],
            password=db_data["password"],
            database=db_data["database"]
        )
        self.cursor = self.db.cursor()

    def get(self, item="*", where="", order="") -> list:
        sql = f"SELECT {item} FROM `{self.name}`"
        if where != "":
            sql += f" WHERE {where}"
        if order != "":
            sql += f" ORDER BY `{order}`;"
        else:
            sql += ';'
        
        print(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def newId(self) -> int:
        result = 1
        existingIDs = self.get(item=self.columns[0])
        for IDs in existingIDs:
            if IDs[0] == result:
                result += 1
                continue
            else:
                break
        return result

    def add(self, *argc) -> None:
        sql = f"INSERT INTO `{self.name}` ("
        for col in self.columns:
            sql += f"`{col}`,"
        sql = sql[0:-1]
        sql += ") VALUES ("
        for val in argc:
            sql += f"'{val}',"
        sql = sql[0:-1]
        sql += ");"
        
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
    
    def upd(self, where="1", **kwarg) -> None:
        sql = f"UPDATE `{self.name}` SET "
        for key, value in kwarg.items():
            sql += f"`{key}` = '{value}',"
        sql = sql[0:-1]
        sql += f" WHERE {where};"
        print("\n\n",sql,"\n\n")
        self.cursor.execute(sql)
        self.db.commit()

    def Del(self, where="1") -> None:
        sql = f"DELETE FROM `{self.name}` WHERE {where};"
        self.cursor.execute(sql)
        self.db.commit()

class staff(model):
    name = "staff"
    columns = ["id", "name", "password", "post", "status"]

class posts(model):
    name = "posts"
    columns = ["id", "name", "attendance", "examination", "management", "privileges", "staff"]

class sections(model):
    name = "sections"
    columns = ["id", "name", "fall", "program"]

class students(model):
    name = "students"
    columns = ["sr", "id", "name","father", "section"]

class staff_attendance(model):
    name = "staff_attendance"
    columns = ["sr","date","id","time_in","time_out"]

class staff_absence(model):
    name = "staff_absence"
    columns = ["sr","date","id","request"]

class visiting_record(model):
    name="visiting_record"
    columns = ["sr","program","subject"]

class lectures(model):
    name = "lectures"
    columns = ["id", "subject", "section", "staff", "day", "period"]

class lecture_attendance(model):
    name = "lecture_attendance"
    columns = ["sr", "lecture", "date"]

class student_attendance(model):
    name = "student_attendance"
    columns = ["sr", "lecture", "student", "attended"]