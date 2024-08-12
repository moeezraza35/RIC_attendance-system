from flask import Blueprint, render_template, session, redirect, request
from db_manage import rearranging, valid, error_msg, getReport, getAttendance
import models

Mngnt = Blueprint("Mngnt",__name__)
"""

    Manage Sections

"""
@Mngnt.route("/<usrid>/manage/sections/<section>")
def manageSection(usrid,section):
    if "usrid" in session:
        myresult = valid(usrid,3)
        Name = myresult[0]
        validity = myresult[1]
        secName = ""
        if session["usrid"] == usrid and validity == 1:
            sections = models.sections().get()

            for sec in sections:
                if str(sec[0]) == section:
                    secName = f"{sec[3]} {sec[1]} {sec[2]}"
                    secId = sec[0]
                    fall = sec[2]
                    break

            myresult = models.students().get(
                item="`sr`, `id`, `name`, `father`",
                where=f"`section` = '{section}'",
                order="id"
            )

            return render_template(
                "sections.html",
                usrnm = Name,
                fall = fall,
                usrid = usrid,
                sections = sections,
                students = myresult,
                section_name = secName,
                section_id = secId,
                section_selected = 1
            )
        else:
            return error_msg
    else:
        return redirect("/")

'''

=========   Manage lectures =========

'''

@Mngnt.route("/<usrid>/manage/sections/<section>/lectures")
def manageLecture(usrid, section):
    if "usrid" in session:
        myresult = valid(usrid,3)
        Name = myresult[0]
        validity = myresult[1]
        secName = ""
        if session["usrid"] == usrid and validity == 1:
            sections = models.sections().get()
            lectures = models.lectures().get(where=f"`section`='{section}'")
            staff = models.staff().get()

            for sec in sections:
                if str(sec[0]) == section:
                    secName = f"{sec[3]} {sec[1]} {sec[2]}"
                    secID = sec[0]
                    break

            return render_template(
                "lecture.html",
                usrnm = Name,
                usrid = usrid,
                sections = sections,
                lectures = lectures,
                staff = staff,
                students = myresult,
                days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                section_name = secName,
                section_id = secID
            )
        else:
            return error_msg
    else:
        return redirect("/")

'''

========    Manage Posts    ========

'''

@Mngnt.route("/<usrid>/manage/posts")
def managePost(usrid):
    if "usrid" in session:      # Checking is user login
        myresult = valid(usrid,4)
        Name = myresult[0]
        validity = myresult[1]
        if validity == 1 and session["usrid"] == usrid:  # Checking user validity to access
            myresult = models.posts().get()
            return render_template(     # Required return of this route
                "otherfeatures/posts.html",
                usrnm = Name,
                usrid = usrid,
                posts = myresult,
                headings = ["Posts", "Student Attendance", "Examination", "Management", "Staff Rolls", "Staff Attendance"]
            )
        else:
            return error_msg    # Error message when user tryies to login others account
    else:
        return redirect('/')


# Deleting a post

@Mngnt.route("/<usrid>/manage/posts/delete/<post_to_delete>")
def delete_post(usrid, post_to_delete):
    if "usrid" in session:      # Checking is user login
        staf = models.staff().get()
        for members in staf:
            if members[3] == post_to_delete:
                return error_msg
        myresult = valid(usrid, 4)
        validity = myresult[0]
        if session["usrid"] == usrid and validity:
            models.posts().Del(where=f"`id`='{post_to_delete}'")
        return redirect(f"/{usrid}/manage/posts")
    else:
        return redirect("/")

'''

========    Manage Staf    ========

'''

@Mngnt.route("/<usrid>/manage/staf")
def mgtimetable(usrid):
    if "usrid" in session:      # Checking is user login
        myresult = valid(usrid,3)
        Name = myresult[0]
        validity = myresult[1]

        if validity == 1 and session["usrid"] == usrid:  # Checking user validity to access
            staf = models.staff().get(order="id")
            posts = models.posts().get()

            return render_template(     # Required return of this route
                "otherfeatures/staf.html",
                usrnm = Name,
                usrid = usrid,
                staf = staf,
                posts = posts
                )
        else:
            return error_msg    # Error message when user tries to hack
    else:
        return redirect("/")    # If not login
    

# Deleting a member from staf

@Mngnt.route("/<usrid>/manage/staf/delete/<memberid>")
def delete_staf_member(usrid, memberid):
    if "usrid" in session:      # Checking is user login
        myresult = valid(usrid,3)
        validity = myresult[1]

        if usrid == session["usrid"] and validity == 1: # Checking user validity
            models.staff().Del(where=f"`id` = '{memberid}'")

            return redirect(f"/{usrid}/manage/staf")    # Required return of the program
        else:
            return error_msg    # Error message on attempt wrong or hacking
    else:
        return redirect("/")    # If not login

"""

    ======== Manage Staff Attendance ========

"""
@Mngnt.route("/<usrid>/manage/staf/attendance")
def staf_attendance_dash(usrid):
    if "usrid" in session:  # Checking is user login
        myresult = valid(usrid,5)
        Name = myresult[0]
        validity = myresult[1]

        if session["usrid"] == usrid and validity == 1: # Checking user validity
            return render_template(
                "otherfeatures/attendance.html",
                usrnm = Name,
                usrid = usrid,
            )
        else:
            return error_msg
    else:
        return redirect("/")

@Mngnt.route("/<usrid>/manage/staf/attendance/<status>")
def staf_attendance(usrid, status):
    if "usrid" in session:  # Checking is user login
        myresult = valid(usrid,5)
        Name = myresult[0]
        validity = myresult[1]

        if session["usrid"] == usrid and validity == 1: # Checking user validity
            staf = models.staff().get(where=f"`status` = '{status}'")
            sections = models.sections().get()

            report = getReport(status)
            
            Visiting = 0
            if status == "Visiting":
                Visiting = 1

            return render_template(
                "otherfeatures/attendance.html",
                usrid = usrid,
                usrnm = Name,
                staf = staf,
                status = status,
                sections = sections,
                Visiting = Visiting,
                reports = report
                )
        else:
            return error_msg    # If user makes an illegal attempt
    else:
        return redirect('/')    # If user logout

    

# Updating attendance of marked attendance of specific date

@Mngnt.route("/<usrid>/manage/staf/attendance/<status>/<date>")
def staf_attendance_date(usrid, status, date):
    if "usrid" in session:
        myresult = valid(usrid,5)
        Name = myresult[0]
        validity = myresult[1]

        if session["usrid"] == usrid and validity == 1: # Checking user validity
            staf = models.staff().get(where=f"`status` = '{status}'")
            sections = models.sections().get()
            report = getReport(status)
            record = getAttendance(status=status,date=date)
            vs_rec = []
            if status == "Visiting":
                vr = models.visiting_record()
                for rec in record:
                    for member in staf:
                        if rec[2] == member[0]:
                            vs_rec.append(vr.get(where=f"`sr` = '{rec[0]}'")[0])
            
            for rec in range(len(record)):
                record[rec] = list(record[rec])
                record[rec][1] = str(record[rec][1])
                if str(record[rec][3])[1] == ':':
                    record[rec][3] = '0' + str(record[rec][3])
                else:
                    record[rec][3] = str(record[rec][3])
                if str(record[rec][4])[1] == ':':
                    record[rec][4] = '0' + str(record[rec][4])
                else:
                    record[rec][4] = str(record[rec][4])

            Visiting = 0
            if status == "Visiting":
                Visiting = 1
                for rec in range(len(record)):
                    record[rec] = list(record[rec])
                    for i in vs_rec:
                        if i[0] == record[rec][0]:
                            record[rec].append(i[1])
                            record[rec].append(i[2])
                    record[rec] = tuple(record[rec])
            return render_template(
                "otherfeatures/attendance.html",
                usrid = usrid,
                usrnm = Name,
                staf = staf,
                Visiting = Visiting,
                status = status,
                sections = sections,
                reports = report,
                date_selected = date,
                record = record
            )
        else:
            return error_msg    # If user makes an illegal attempt
    else:
        return redirect('/')    # If user logout
        

"""

    ======== Staff Attendance Report ========

"""
@Mngnt.route("/<usrid>/manage/staf/report")
def staf_attendance_report_Page(usrid):
    if "usrid" in session:
        myresult = valid(usrid,5)
        Name = myresult[0]
        validity = myresult[1]
        if session["usrid"] == usrid and validity == 1:
            return render_template(
                "otherfeatures/report.html",
                usrid = usrid,
                usrnm = Name,
            )
        else:
            return error_msg    # If user makes an illegal attempt
    else:
        return redirect('/')    # If user logout

@Mngnt.route("/<usrid>/manage/staf/report/<status>")
def staf_attendance_report(usrid, status):
    if "usrid" in session:
        myresult = valid(usrid,5)
        Name = myresult[0]
        validity = myresult[1]
        if session["usrid"] == usrid and validity == 1:
            staf = models.staff().get(where=f"`status` = '{status}'")
            dates = getReport(status)

            return render_template(     # Required return of this route
                "otherfeatures/report.html",
                usrid = usrid,
                usrnm = Name,
                staf = staf,
                status = status,
                dates = dates,
                report_of = f"{status} staff"
            )
        else:
            return error_msg
    else:
        return redirect('/')


# Returning report of permanent staf

@Mngnt.route("/<usrid>/manage/staf/report/<status>/<members>/<dateFrom>/to/<dateTo>")
def return_the_staf_att_report(usrid, status, members, dateFrom, dateTo):
    if "usrid" in session:
        myresult = valid(usrid,5)
        Name = myresult[0]
        validity = myresult[1]
        if session["usrid"] == usrid and validity == 1:
            w = f"`date` >= '{dateFrom}' AND `date` <= '{dateTo}'"
            staf = None
            if members != "all":
                w += f" AND `sr` = '{members}'"
                staf = models.staff().get(where=f"`id` = '{members}'")
            else:
                staf = models.staff().get(where=f"`status` = '{status}'")
            report = getAttendance(status=status)

            # Making a datelist
            dateList = []
            for rows in report:
                if not rows[1] in dateList:
                    dateList.append(rows[1])
            
            # Adding visiting record
            if status == "visiting":
                vst_rep = models.visiting_record().get()
                for rows in range(len(report)):
                    for rows2 in vst_rep:
                        if report[rows][0] == rows2[0]:
                            report[rows] = list(report[rows])
                            section = models.sections().get(where=f"`id`='{rows2[1]}'")[0]
                            report[rows].append(section[3]+' '+section[1]+' '+section[2])
                            report[rows].append(rows2[2])
            
            # Removing white spaces in the record which shifts to left
            for member in staf:
                count = []
                for rows in report:
                    if rows[2] == member[0]:
                        count.append(rows[1])
                if len(count) < len(dateList):
                    for dates in dateList:
                        if not dates in count:
                            newTuple = (0,dates,member[0],"-","-","none","none")
                            report.append(newTuple)

            dates = getReport(status)

            # Re-aranging according to date after merging absents
            result = rearranging(report, dateList)

            return render_template(     # Required return of this route
                "otherfeatures/report.html",
                usrid = usrid,
                usrnm = Name,
                staf = staf,
                status = status,
                dates = dates,
                report_of = f"{status} staff",
                report=result,
                member=members,
                dateList=dateList,
                dateFrom=dateFrom,
                dateTo=dateTo
            )
        else:
            return error_msg
    else:
        return redirect('/')
