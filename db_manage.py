import models
import csv

def valid(usrid,post_item_no=0):
    returnList = []     # List for returning 2 values
    user_tuple = models.staff().get(where=f"`id` = '{usrid}'")[0]
    # Output structure is "[(val1, val2,...)]"; for accessing inner tuple.
    Name = str(user_tuple[1])
    returnList.append(Name) # 1st item to return
    myresult = models.posts().get(where=f"`id` = '{user_tuple[3]}'")  # Get user previllages
    mytuple = myresult[0]   # Output structure is "[(val1, val2,...)]"; for accessing inner tuple.
    """

    "post_item_no = 0 or any other"

        "post_item_no" is the number of coloumn which contains access to specific item.
        Default is 0 which means program requires a complete list of user privillages.
        If there is a number above 0, it means specific access.

    """
    if post_item_no == 0:               # Returning complete list
        returnList.append(mytuple)      # 2nd item to return

    else:
        returnList.append(mytuple[post_item_no+1] == 1)    # 2nd item to return

    return returnList   # Main retrun of the program

# Variable for returning an error if user access page which he/she is not allowed.
error_msg = """
        <script>
            alert(\"Error on Login!\\nYou are not allowed to open this page.\");
            window.open('/','_self');
        </script>
        """

def getAttendance(status:str, date="") -> list:
    if date != "":
        w = f"`date` = '{date}'"
        attendance = models.staff_attendance().get(where=w)
        absence = models.staff_absence().get(where=w)
    else:
        attendance = models.staff_attendance().get()
        absence = models.staff_absence().get()

    for rec in range(len(absence)):
        absence[rec] = list(absence[rec])
        if absence[rec][3] == 1:
            absence[rec][3] = "Leave"
            absence[rec].insert(-1,"Leave")
        else:
            absence[rec][3] = "Absent"
            absence[rec].insert(-1,"Absent")
        absence[rec] = tuple(absence[rec])

    attendance.extend(absence)
    staff = models.staff().get(where=f"`status` = '{status}'")
    result = []
    for rec in attendance:
        for members in staff:   # Removing other status attendance record
            if members[0] == rec[2]:
                result.append(rec)
                break
    return result

def getReport(status:str):
    myresult = []
    report = getAttendance(status=status)
    for items in report:
        if not (str(items[1]) in myresult):
            myresult.append(str(items[1]))
    return myresult

def is_record_exist(date, record_of):
    w = f"`date` = '{date}' AND `id` = '{record_of}'"
    p_record = models.staff_attendance().get(where=w)
    a_record = models.staff_absence().get(where=w)

    if p_record != [] or a_record != []:
        return True
    else:
        return False

def rearranging(report:list, dateList:list):
    result = []
    for dates in dateList:
        for rec in report:
            if rec[1] == dates:
                result.append(rec)
    for x in range(len(result)):
        result[x] = list(result[x])
        if result[x][3] != "Absent" and result[x][3] != "Leave" and result[x][3] != "-":
            i=3
            while i < 5:
                n=1
                if str(result[x][i])[2] == ':':
                    n=2
                hr = int(str(result[x][i])[0:n])
                p = " AM"
                if hr >= 12:
                    p = " PM"
                if hr > 12:
                    hr -= 12
                elif hr == 0:
                    hr = 12
                result[x][i] = str(hr) + str(result[x][i])[n : -3] + p
                i += 1
    return result

class importCSV():
    def __init__(self, file_path:str) -> None:
        file = open(file_path, "rt")
        self.data = file.readlines()
        file.close
        self.columns = ["id","name","father","section","program"]
        self.rows = {}
    
    def read(self) -> None:
        lineCount = 0
        reader = csv.reader(self.data)
        section = models.sections()
        students = models.students()
        for line in reader:
            if lineCount > 0:
                for col in range(len(self.columns)):
                    self.rows[self.columns[col]] = line[col]

                secID = 0
                thatSection = section.get(where=f"`name`='{self.rows["section"]}' AND `fall`='{str(self.rows["id"][:4]).upper()}' AND `program`='{self.rows["program"]}'")
                if len(thatSection) == 0:
                    secID = section.newId()
                    section.add(secID, self.rows["section"], self.rows["id"][:4], self.rows["program"])
                else:
                    secID = thatSection[0][0]
                
                print("fall =", self.rows["id"][:4])
                print("id =", self.rows["id"][-4:])
                mysections = section.get(where=f"`fall`='{str(self.rows["id"][:4]).upper()}'")
                mystudents = students.get(where=f"`id`='{self.rows["id"][-4:]}'")
                find = False
                for sect in mysections:
                    for student in mystudents:
                        if str(sect[0]) == str(student[4]):
                            find = True
                            break
                    if find: break
                if not find:
                    newID = students.newId()
                    students.add(newID, self.rows["id"][-4:], self.rows["name"], self.rows["father"], secID)
                    
            lineCount += 1

