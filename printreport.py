from flask import Blueprint, redirect, render_template, session, make_response, send_file
from db_manage import error_msg, rearranging, valid, getAttendance, getReport
import models
import pdfkit

prtRepo = Blueprint("prtrepo",__name__)
config = pdfkit.configuration(wkhtmltopdf=".\\wkhtmltox\\bin\\wkhtmltopdf.exe")
pdf_options = {
        'page-size': 'A4',
        'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
    }

@prtRepo.route("/<usrid>/manage/staf/report/<status>/<members>/<dateFrom>/to/<dateTo>/print")
def printPermanentReport(usrid, status, members, dateFrom, dateTo):
    if "usrid" in session:
        myresult = valid(usrid,5)
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

            # Re-aranging according to date after merging absents
            result = rearranging(report, dateList)

            html = render_template(     # Required return of this route
                "toPrint/report.html",
                staf = staf,
                status = status,
                report_of = f"{status} staff",
                report=result,
                member=members,
                dateList=dateList,
            )
            pdf_options = {
                'page-size': 'A4',
                'orientation': 'Landscape',
                'margin-top': '0mm',
                'margin-right': '0mm',
                'margin-bottom': '0mm',
                'margin-left': '0mm',
            }

            pdf = pdfkit.from_string(html, False, options=pdf_options, configuration=config)
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=report.pdf'

            return response
        else:
            return error_msg
    else:
        return redirect('/')

@prtRepo.route("/<usrid>/manage/staf/report/<status>/<members>/<dateFrom>/to/<dateTo>/export")
def ExportPermanentReport(usrid, status, members, dateFrom, dateTo):
    if "usrid" in session:
        myresult = valid(usrid,5)
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

            # Re-aranging according to date after merging absents
            result = rearranging(report, dateList)
            
            toWrite=""

            myFile = open(".\\templates\\toPrint\\report.csv", "wt")
            if members == "all":
                toWrite += "Sr,Name,"
                for dates in dateList:
                    toWrite += str(dates)+',,'
                toWrite += "\n,"
                for dates in dateList:
                    toWrite += ",Time in,Time out"
                for rec in staf:
                    toWrite += f"\n{rec[0]},{rec[1]}"
                    for items in result:
                        if items[2] == rec[0]:
                            toWrite += ','+str(items[3])+','+str(items[4])
            else:
                for member in staf:
                    if str(member[0]) == str(members):
                        toWrite += member[1]
                    if status == "Visting":
                        toWrite += ",Visiting Staf Faculty,,,,"
                    else: toWrite += ",,,"
                    toWrite += "\nDate"
                    if status == "Visiting":
                        toWrite += ",Section,Subject"
                    toWrite += ",Time in,Time out"
                    for rec in result:
                        toWrite += "\n"+str(rec[1])
                        if status == "Visting":
                            toWrite += ','+str(rec[5])+','+str(rec[6])
                        toWrite += ','+str(rec[3])+','+str(rec[4])
            myFile.write(toWrite)
            myFile.close()
            file_path = ".\\templates\\toPrint\\report.csv"
            return send_file(file_path, as_attachment=True)
        else:
            return error_msg
    else:
        return redirect("/")

@prtRepo.route("/<usrid>/students/attendance/<section>/<datefrom>/<dateto>/print")
def PrintStudentsReport(usrid, section, datefrom, dateto):
    if "usrid" in session:          # Checking user is login
        myresult = valid(usrid,1)   # Checking user validity
        validity = myresult[1]      # His validity in boolean

        if validity == 1 and session["usrid"] == usrid:
            sections = models.sections().get()
            lect_att = models.lecture_attendance()
            lectures = models.lectures().get(where=f"`section`='{section}'")
            students = models.students().get(where=f"`section`='{section}'")
            attendances = lect_att.get()
            dateList = []
            for lecture in lectures:
                for attendance in attendances:
                    if lecture[0] == attendance[1] and not str(attendance[2]) in dateList:
                        dateList.append(str(attendance[2]))
            attendances = []
            stud_att = []
            fall = ""
            attendances = models.lecture_attendance().get(where=f"`date`>='{datefrom}' AND `date`<='{dateto}'", order="date")
            stud_att = models.student_attendance().get()
            
            myresult = []
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

            sec_name = ""
            for sec in sections:
                if str(sec[0]) == section:
                    fall = sec[2]
                    sec_name = sec[3] + sec[1]
                    break
            
            html = render_template(
                "toPrint/student.html",
                sec_name = sec_name,
                fall = fall,
                lectures = lectures,
                dateList = dateList,
                dates = myresult,
                attendances = attendances,
                stud_att = stud_att,
                students = students,
                datespan = myresult
            )
            pdf_options = {
                'page-size': 'A4',
                'orientation': 'Landscape',
                'margin-top': '0mm',
                'margin-right': '0mm',
                'margin-bottom': '0mm',
                'margin-left': '0mm',
            }

            pdf = pdfkit.from_string(html, False, options=pdf_options, configuration=config)
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=report.pdf'

            return response
