from flask import Blueprint, redirect, render_template,session, request
from db_manage import valid, error_msg
import models
from datetime import datetime

Students = Blueprint("SubRoute",__name__)

'''

==== Students attendance === 


'''

@Students.route("/<usrid>/students/attendance/<section>")
def takeAttendance(usrid, section):
    if "usrid" in session:
        myresult = valid(usrid)
        Name = myresult[0]
        myTuple = myresult[1]
        if myTuple[2] == 1 or myTuple[4] == 1 and session["usrid"] == usrid:
            sections = models.sections().get()
            attendances = models.lecture_attendance().get()
            lectures = None
            if myTuple[4] == 1:
                lectures = models.lectures().get(where=f"`section`='{section}'")
            else:
                day = datetime.now().strftime("%A")
                lectures = models.lectures().get(where=f"`section`='{section}' AND `staff`='{usrid}' AND `day` = '{day}'")
            for sec in sections:
                if str(sec[0]) == section:
                    secName = f"{sec[3]} {sec[1]} {sec[2]}"
                    secId = str(sec[0])
                    fall = sec[2]
                    break
            myresult = models.students().get(
                item="`sr`, `id`, `name`, `father`",
                where=f"`section` = '{section}'",
                order="id"
            )

            return render_template(
                "attendance.html",
                usrnm = Name,
                usrid = usrid,
                admin = myTuple[4],
                sections = sections,
                students = myresult,
                lectures = lectures,
                attendances = attendances,
                section_name = secName,
                section_id = secId,
                fall = fall
                )
        else:
            return redirect(f"/{usrid}/students/attendance")
    else:
        return redirect("/")

@Students.route("/<usrid>/students/attendance/<section>/<attendance>")
def updateAttendance(usrid, section, attendance):
    if "usrid" in session:
        myresult = valid(usrid)
        Name = myresult[0]
        validity = myresult[1]
        if validity[2] == 1 or validity[4] == 1 and session["usrid"] == usrid:
            sections = models.sections().get()
            attendances = models.lecture_attendance().get()
            lectures = None
            if validity[4] == 1:
                lectures = models.lectures().get(where=f"`section`='{section}'")
            else:
                day = datetime.now().strftime("%A")
                lectures = models.lectures().get(where=f"`section`='{section}' AND `staff`='{usrid}' AND `day` = '{day}'")
            for sec in sections:
                if str(sec[0]) == section:
                    secName = f"{sec[3]} {sec[1]} {sec[2]}"
                    secId = str(sec[0])
                    fall = sec[2]
                    break
            myresult = models.students().get(
                item="`id`, `name`, `father`",
                where=f"`section` = '{section}'",
                order="id"
            )
            curr_attendance = []
            for attends in attendances:
                if attends[0] == int(attendance):
                    
                    curr_attendance = [attends[1], attends[2], attends[0]]
                    break
            
            stud_att = models.student_attendance().get(where=f"`lecture`='{curr_attendance[2]}'")
            print(stud_att)

            return render_template(
                "attendance.html",
                usrnm = Name,
                usrid = usrid,
                admin = validity[4],
                sections = sections,
                curr_attendance = curr_attendance,
                students = myresult,
                stud_att = stud_att,
                lectures = lectures,
                attendances = attendances,
                section_name = secName,
                section_id = secId,
                fall = fall
                )
        else:
            return error_msg
    else:
        return redirect('/')
    
@Students.route("/<usrid>/students/attendance/report", methods=["GET"])
def reportPage(usrid):
    if "usrid" in session:          # Checking user is login
        myresult = valid(usrid,1)   # Checking user validity
        Name = myresult[0]          # User name
        validity = myresult[1]      # His validity in boolean

        if validity == 1 and session["usrid"] == usrid: # Checking that same user in session is accessing
            sections = models.sections().get()  # Get all the sections record
            if request.args.get("section"):
                section = request.args.get("section")
                dateList = []
                lect_att = models.lecture_attendance()
                attendances = lect_att.get()
                lectures = models.lectures().get(where=f"`section`='{section}'")
                students = models.students().get(where=f"`section`='{section}'")
                for lecture in lectures:
                    for attendance in attendances:
                        if lecture[0] == attendance[1] and not str(attendance[2]) in dateList:
                            dateList.append(str(attendance[2]))
                attendances = []
                stud_att = []
                fall = ""
                if request.args.get("datefrom") and request.args.get("dateto"):
                    dateFrom = request.args.get("datefrom")
                    dateTo = request.args.get("dateto")
                    attendances = models.lecture_attendance().get(where=f"`date`>='{dateFrom}' AND `date`<='{dateTo}'", order="date")
                    stud_att = models.student_attendance().get()

                    for sec in sections:
                        if str(sec[0]) == section:
                            fall = sec[2]
                            break
                        
                    date = str(attendances[0][2])+'0'
                    myresult=[]
                    colspan = 0
                    for attendance in attendances:
                        if date[:-1] == str(attendance[2]):
                            colspan+=1
                        else:
                            myresult.append(date)
                            colspan=1
                            date = str(attendance[2])+str(colspan)
                        date = date[:-1] + str(colspan)
                    myresult.append(date)
                return render_template(
                    "report.html",
                    usrid = usrid,
                    usrnm = Name,
                    sections = sections,
                    fall = fall,
                    lectures = lectures,
                    dateList = dateList,
                    dates = myresult,
                    section_id = section,
                    attendances = attendances,
                    stud_att = stud_att,
                    students = students
                )

            return render_template(     # Required return
                "report.html",
                usrnm = Name,           # Username
                usrid = usrid,          # User Id
                sections = sections     # List of sections
                )
        else:
            return error_msg
    else:
        return redirect('/')

@Students.route("/<usrid>/students/attendance/report/<section>/<date>")
def dateSectionReportPage(usrid, section, date):
    if "usrid" in session:          # Checking user is login
        myresult = valid(usrid,1)   # Checking user validity
        Name = myresult[0]          # User name
        validity = myresult[1]      # His validity in boolean

        if validity == 1 and session["usrid"] == usrid: # Checking that same user in session is accessing
            myresult = models.sections().get()  # Get all the sections record
            attendances = 0
            lectures = 0
            if date != 0:
                attendances = models.lecture_attendance().get(where=f"`date`='{date}'")
                lectures = models.lectures().get(where=f"`section`='{section}'")

            return render_template(     # Required return
                "report.html",
                usrnm = Name,           # Username
                usrid = usrid,          # User Id
                attendances = attendances,
                lectures = lectures,
                sections = myresult,     # List of sections
                section_id = section
                )
        else:
            return error_msg
    else:
        return redirect('/')