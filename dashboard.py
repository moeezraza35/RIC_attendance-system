from flask import Blueprint, render_template, session, redirect
from db_manage import valid, error_msg
import models

Dashboard = Blueprint("dashboard",__name__)     # For making a divided file of flask-app

# Attendance page

@Dashboard.route("/<usrid>/students/attendance")
def attendance(usrid):
    if "usrid" in session:          # Checking user is login
        myresult = valid(usrid,1)   # Checking user validity
        Name = myresult[0]          # User name
        validity = myresult[1]      # His validity in boolean

        if validity == 1 and session["usrid"] == usrid: # Checking that same user in session is accessing
            myresult = models.sections().get()  # Get all the sections record

            return render_template(     # Required return
                "attendance.html",
                usrnm = Name,           # Username
                usrid = usrid,          # User Id
                sections = myresult     # List of sections
                )
        else:
            return error_msg    # If user with no permission to access the attendance
    else:
        return redirect('/')    # If user is logout


# Examination Page
@Dashboard.route("/<usrid>/students/examination")
def examination(usrid):
    if "usrid" in session:
        myresult = valid(usrid, 2)
        # Name = myresult[0]
        validitiy = myresult[1]

        if validitiy == 1 and session["usrid"] == usrid:
            return "<h1>This page will be come soon</h1>"
        else:
            return error_msg
    else:
        return redirect("/")

# Section page

@Dashboard.route("/<usrid>/manage/sections")
def Sections(usrid):
    if "usrid" in session:
        myresult = valid(usrid,3)
        Name = myresult[0]
        validity = myresult[1]
        if session["usrid"] == usrid and validity == 1:
            myresult = models.sections().get()
            return render_template(
                "sections.html",
                usrnm = Name,
                usrid = usrid,
                sections = myresult,
                section_selected = 0,
                edit = 1,
                )
        else:
            return error_msg    # If user with no permission to access the attendance
    else:
        return(redirect('/'))

@Dashboard.route("/<usrid>/students")
def ShowStudents(usrid):
    if "usrid" in session:
        myresult = valid(usrid,1)
        Name = myresult[0]
        if session["usrid"] == usrid:
            myresult = models.sections().get()
            return render_template(
                "sections.html",
                usrnm = Name,
                usrid = usrid,
                sections = myresult,
                section_selected = 0
            )
        else:
            return error_msg
    else:
        return redirect('/')
