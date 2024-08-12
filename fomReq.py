from flask import Blueprint, redirect, session, request, flash
from db_manage import valid, is_record_exist, error_msg, importCSV
import models
from datetime import datetime

FormReq = Blueprint("FormReq",__name__) # For making a divided file of flask-app


# Creating new section

@FormReq.route("/<usrid>/manage/sections/create_new", methods=["POST"])
def create_section(usrid):
    if "usrid" in session:
        if session["usrid"] == usrid:
            # All form data
            section = request.form["name"]      # Section name
            fall = request.form["fall"]         # Fall of section (AF / SF & year)
            program = request.form["program"]   # Program of section

            #mycursor.execute("SELECT * FROM sections ORDER BY Id")
            myresult = models.sections().get(order="id")

            Ids = 1         # For giving suitable id to the new section
            procced = True  # Should process continue or not

            for x in myresult:
                if x[0] == Ids:
                    Ids += 1    # Increase by one if id number already exist

                if x[1] == section and x[2] == fall and x[3] == program:
                    procced = False     # If same section exist it will stop procced
                else:
                    continue

            if procced:
                #mycursor.execute(f"INSERT INTO `sections` (`Id`, `Name`, `Fall`, `Program`) VALUES ({Ids},'{section.upper()}','{fall.upper()}','{program.upper()}');")
                models.sections().add(Ids,section.upper(),fall.upper(),program.upper())
                return redirect(f"/{usrid}/manage/sections")
            else :
                return error_msg
        else:
            return error_msg
    else:
        return redirect("/")


# Delete section

@FormReq.route("/<usrid>/manage/sections/<section_id>/delete_section")
def delete_section(usrid, section_id):
    if "usrid" in session:
        myresult = valid(usrid,3)
        validity = myresult[1]
        if session["usrid"] == usrid and validity:
            #mycursor.execute(f"DELETE FROM `sections` WHERE ")
            models.students().Del(where=f"`section`='{section_id}'")
            models.sections().Del(where=f"`id`='{section_id}'")
            models.lectures().Del(where=f"`section`='{section_id}'")
        return redirect(f"/{usrid}/manage/sections")
    else:
        return redirect("/")


# Adding students in a selected section

@FormReq.route("/<usrid>/manage/sections/<section>/add_student", methods=["POST"])
def add_student(usrid, section):
    if "usrid" in session:
        if session["usrid"] == usrid:
            id = request.form["id"]
            Name = request.form["name"].capitalize()
            father = request.form["father"].capitalize()

            mystudent = models.students()
            sections = models.sections()
            fall = sections.get(item="`fall`", where=f"`id`='{section}'")[0][0]
            sections = sections.get(where=f"`fall`='{fall}'")
            students = mystudent.get(where=f"`id`='{id}'", order="id")
            find = False
            for sect in sections:
                for student in students:
                    if str(sect[0]) == str(student[4]):
                        find = True
                        break
                if find: break
            if not find:
                newID = mystudent.newId()
                mystudent.add(newID,id,Name,father,section)
                # Marking old attendances
                lectures = models.lectures().get(where=f"`section`='{section}'")
                attendances = models.lecture_attendance().get()
                student_attendance = models.student_attendance()
                for lecture in lectures:
                    for attendace in attendances:
                        if lecture[0] == attendace[1]:
                            newID = student_attendance.newId()
                            student_attendance.add(newID, attendace[0], id, 'A')
            return redirect(f"/{usrid}/manage/sections/{section}")
        else:
            return error_msg
    else:
        return redirect('/')


# Deleting a student from selected section

@FormReq.route("/<usrid>/manage/sections/<section>/delete/<student>")
def delete_student(usrid, section, student):
    if "usrid" in session:
        myresult = valid(usrid, 3)
        validity = myresult[0]
        if session["usrid"] == usrid and validity:
            models.students().Del(where=f"`sr` = '{student}'")
        return redirect(f"/{usrid}/manage/sections/{ section }")
    else:
        return redirect("/")


# Uploading csv data of students and section

@FormReq.route("/<usrid>/manage/sections/import-csv/", methods=["POST"])
def import_csv(usrid):
    if "usrid" in session:
        myresult = valid(usrid, 3)
        validity = myresult[0]
        if session["usrid"] and validity:
            file = request.files["students"]
            file.save(".\\templates\\toPrint\\students.csv")
            importCSV(".\\templates\\toPrint\\students.csv").read()

        return redirect(request.referrer)
    else:
        return redirect("/")


# Create new lecture

@FormReq.route("/<usrid>/manage/sections/<section>/lectures/add", methods=["POST"])
def add_lecture(usrid, section):
    if "usrid" in session:
        myresult = valid(usrid, 3)
        validity = myresult[0]
        if session["usrid"] and validity:
            subject = request.form["subject"]
            section = section
            staff = request.form["member"]
            day = request.form["day"]
            period = request.form["period"]
            lectures = models.lectures()
            newID = lectures.newId()

            if len(lectures.get(item="`id`", where=f"`section`='{section}' AND `staff`='{staff}' AND `day`='{day}'")) == 0:
                lectures.add(newID, subject, section, staff, day, period)
            
            return redirect(request.referrer)
        else:
            return error_msg
    else:
        return redirect('/')
            

# Delete a lecture

@FormReq.route("/<usrid>/manage/sections/lectures/delete/<lecture>")
def delete_lecture(usrid, lecture):
    if "usrid" in session:
        myresult = valid(usrid,3)
        validity = myresult[1]
        if session["usrid"] == usrid and validity == 1:
            models.lectures().Del(where=f"`id`='{lecture}'")
            return redirect(request.referrer)
        else:
            return error_msg
    else:
        return redirect('/')


# Update a lecture

@FormReq.route("/<usrid>/manage/sections/lectures/update/<lecture>", methods=["POST"])
def update_lecture(usrid, lecture):
    if "usrid" in session:
        myresult = valid(usrid,3)
        validity = myresult[1]
        if session["usrid"] == usrid and validity == 1:
            subject = request.form["subject"]
            section = request.form["section"]
            member = request.form["member"]
            day = request.form["day"]
            period = request.form["period"]
            models.lectures().upd(
                where=f"`id`={lecture}",
                subject=subject,
                section=section,
                staff=member,
                day=day,
                period=period
            )
            return redirect(request.referrer)
        else:
            return error_msg
    else:
        return redirect('/')


# Marking Student attendance

@FormReq.route("/<usrid>/students/attendance/<section>/mark", methods=["POST"])
def mark_student_attendance(usrid, section):
    if "usrid" in session:
        if session["usrid"] == usrid:
            admin = int(request.args.get("admin"))
            print("\n\nAdmin = ", admin)
            students = models.students().get(where=f"`section`='{section}'")
            lecture = None
            date = None
            if admin == 1:
                lecture = request.form["lecture"]
                date = request.form["date"]
            else:
                day = datetime.now().strftime("%A")
                lecture = models.lectures().get(where=f"`section`='{section}' AND `staff`='{usrid}' AND `day`='{day}'")[0][0]
                date = datetime.now().date()

            lecture_attendance = models.lecture_attendance()
            where = f"`lecture`='{lecture}' AND `date`='{date}'"
            lec_sr = 0
            att_rslt = lecture_attendance.get(where=where)
            if len(att_rslt) == 0:
                lec_sr = lecture_attendance.newId()
                lecture_attendance.add(lec_sr, lecture, date)
            else:
                print(att_rslt, len(att_rslt))
                lec_sr = att_rslt[0][0]

            for student in students:
                attended = request.form[f"{student[0]}attendance"]
                student_attendance = models.student_attendance()
                where = f"`lecture`='{lec_sr}' AND `student`='{student[0]}'"
                if len(student_attendance.get(where=where)) == 0:
                    std_att = student_attendance.newId()
                    student_attendance.add(std_att, lec_sr, student[0], attended)
                else:
                    student_attendance.upd(where=where, attended=attended)
                
            return redirect(f"/{usrid}/students/attendance/{section}")
        else:
            return error_msg
    else:
        return redirect('/')


# Changing settings of a user

@FormReq.route("/<usrid>/settings/update_profile", methods=["POST"])
def update_profile(usrid):
    if "usrid" in session:
        if session["usrid"] == usrid:
            name = request.form["name"]
            paswd = request.form["password"]
            models.staff().upd(f"`id` = {usrid}", name=name, password=paswd)
            flash("Applied changes are saved successfully")
            return redirect(f"/{usrid}/settings")
        else:
            return error_msg
    else:
        return redirect('/')


# Marking attendance of staf

@FormReq.route("/<usrid>/manage/staf/attendance/<status>/mark", methods=['POST'])
def mark_staf_attendance(usrid, status):
    if "usrid" in session:
        if session["usrid"] == usrid:
            attended = ""                   # Present, Absent or leave will here
            date = request.form["date"]     # Date of which attendance is being marking
            time_in = ""                    # Time in, when someone entered
            time_out = ""                   # Time out, when someone leaved

            staf = models.staff().get(where=f"`status` = '{status}'")      # Getting staf information

            for member in staf:             # Loop which iterates each member for mark attendance
                attended = request.form[f"{member[0]}attendance"]       # Getting attended record
                program = None
                subject = None
                attendance = models.staff_attendance()

                w = f"`date` = '{date}' AND `id` = '{member[0]}'"
                if attended == "present":
                    time_in = request.form[f"{member[0]}_time_in"]
                    time_out = request.form[f"{member[0]}_time_out"]
                    if member[4] == "Visiting":
                        program = request.form[f"{member[0]}program"]
                        subject = request.form[f"{member[0]}subject"]
                    if is_record_exist(date=date, record_of=member[0]):
                        attendance.upd(
                            where=w,
                            time_in=time_in,
                            time_out=time_out,
                        )
                        models.staff_absence().Del(where=w)
                        select = attendance.get(item="`sr`", where=w) # result [(r,)]
                        
                        if select == []:
                            attendance.add(
                                attendance.newId(),
                                date,member[0],
                                time_in,
                                time_out
                            )
                        else:
                            models.visiting_record().upd(
                                where=f"`sr` = '{select[0][0]}'",
                                program = program,
                                subject = subject
                            )
                    else:
                        newID = attendance.newId()
                        attendance.add(
                            newID,
                            date,member[0],
                            time_in,
                            time_out
                        )
                        if member[4] == "Visiting":
                            models.visiting_record().add(
                                newID,
                                program,
                                subject
                            )
                else:
                    absence = models.staff_absence()
                    if attended == "absent":
                        rqst = 0
                    else:
                        rqst = 1

                    if is_record_exist(date=date,record_of=member[0]):
                        atteneds = models.staff_attendance()
                        select = atteneds.get(item="`sr`",where=w)   # result = [(r,)]
                        if select != []:
                            atteneds.Del(where=w)
                            models.visiting_record().Del(where=f"`sr` = '{select[0][0]}'")
                        select = absence.get(item="`sr`",where=w)
                        if select == []:
                            absence.add(
                                absence.newId(),
                                date,
                                member[0],
                                rqst
                            )
                        else:
                            absence.upd(
                                where=w,
                                request = rqst
                            )
                        if member[4] == "Visiting":
                            models.visiting_record().Del(where=w)
                    else:
                        absence.add(
                            absence.newId(),
                            date,
                            member[0],
                            rqst
                        )
                
            return redirect(request.referrer)
        else:
            return error_msg
    else:
        return redirect('/')


# Inserting a new staf member

@FormReq.route("/<usrid>/manage/staf/insert", methods=["POST"])
def inser_staf(usrid):
    if "usrid" in session:
        myresult = valid(usrid, 3)
        validity = myresult[0]
        if session["usrid"] and validity:
            id = request.form["id"]
            name = request.form["name"]
            paswd = request.form["password"]
            post = request.form["post"]
            status = request.form["status"]

            if post == "None":
                return redirect(request.referrer)
            staff = models.staff()
            staff.add(
                staff.newId(),
                name,
                paswd,
                post,
                status
            )

            return redirect(f"/{usrid}/manage/staf")
        else:
            return error_msg
    else:
        return redirect('/')


# Updating a staf member data

@FormReq.route("/<usrid>/manage/staf/update/<memberid>", methods=["POST"])
def update_staf_member(usrid, memberid):
    if "usrid" in session:
        myresult = valid(usrid, 4)
        validity = myresult[0]
        if session["usrid"] and validity:
            name = request.form["name"]
            password = request.form["password"]
            post = request.form["post"]
            status = request.form["status"]
            models.staff().upd(
                where=f"`id` = '{memberid}'",
                name=name,
                password=password,
                post=post,
                status=status
            )
            
            return redirect(f"/{usrid}/manage/staf")
        else:
            return error_msg
    else:
        return redirect('/')


# Insering new post

@FormReq.route("/<usrid>/manage/posts/insert", methods=["POST"])
def insert_post(usrid):
    if "usrid" in session:
        myresult = valid(usrid, 4)
        validity = myresult[0]
        if session["usrid"] and validity:
            GiveAccess = []
            fields = ["Student Attendance", "Examination", "Management", "Staff Rolls", "Staff Attendance"]
            access = request.form.getlist("access")
            new_post_name = request.form["post"]

            if new_post_name == "":
                return redirect(request.referrer)
            for field in fields:
                if field in access:
                    GiveAccess.append(1)
                else:
                    GiveAccess.append(0)
            
            posts = models.posts()
            myresult = posts.get()
            procced = True
            for x in myresult:
                if x[1] == new_post_name:
                    procced = False
            if procced:
                posts.add(
                    posts.newId(),
                    new_post_name,
                    GiveAccess[0],
                    GiveAccess[1],
                    GiveAccess[2],
                    GiveAccess[3],
                    GiveAccess[4]
                )

            return redirect(f"/{usrid}/manage/posts")
        else:
            return error_msg
    else:
        return redirect('/')


# Updating an existing post

@FormReq.route("/<usrid>/manage/posts/update/<post>", methods=["POST"])
def update_post(usrid, post):
    if "usrid" in session:
        myresult = valid(usrid, 4)
        validity = myresult[0]
        if session["usrid"] and validity:
            giveAccess = []
            fields = ["attendance", "examination", "management", "post", "staff"]
            access = request.form.getlist("access")
            for items in fields:
                if items in access:
                    giveAccess.append(1)
                else:
                    giveAccess.append(0)
            models.posts().upd(
                where = f"`id` = '{post}'",
                attendance=giveAccess[0],
                examination=giveAccess[1],
                management=giveAccess[2],
                privileges=giveAccess[3],
                staff=giveAccess[4]
            )
            return redirect(f"/{usrid}/manage/posts")
        else:
            return error_msg
    else:
        return redirect('/')