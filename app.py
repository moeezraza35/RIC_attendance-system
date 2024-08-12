from flask import Flask,render_template, request, redirect, session, flash
import models
#from sys import path
#path.insert(0,"/var/www/riphah/riphah")
from db_manage import valid, error_msg

app = Flask(__name__)
app.secret_key = "Riphah@654"       # Change this security key with in the ("")

# Files in which flask-app is divided
from login import Login             # Login function
from dashboard import Dashboard     # User dashboard
from management import Mngnt        # Management
from fomReq import FormReq          # Form requests
from printreport import prtRepo     # Printing result
from students import Students       # Students management

# Registring blueprints of object of Flask(__name__) from divided files
app.register_blueprint(Login)
app.register_blueprint(Dashboard)
app.register_blueprint(Mngnt)
app.register_blueprint(FormReq)
app.register_blueprint(prtRepo)
app.register_blueprint(Students)

# '/' is the root page which directs user to login page or dashboard page on specific condition

@app.route('/')
def home():
    if "usrid" in session:
        usr = session["usrid"]
        return redirect('/'+usr)
    else:
        return redirect("/login")

# Url according _user id_ opens dashboard page
@app.route("/<usrid>")
def dashboard(usrid):
    Name = ""   # Variable for returning user name

    if "usrid" in session:              # Check that user is login
        if session["usrid"] == usrid:   # Making sure that _user id_ in url is same of user trying to accessing
            myresult = valid(usrid)
            Name = myresult[0]
            mytuple = myresult[1]
            
            return render_template(
                "dashboard.html",
                usrnm = Name,
                usrid = usrid,
                attendance = mytuple[2],
                examination = mytuple[3],
                manage = mytuple[4],
                post = mytuple[5],
                staff = mytuple[6]
                )
        
        else:   # Error message if someone tries to open someone's else account
            return error_msg
    else:       # Sending user to '/' root if not login
        return redirect('/')
    
@app.route("/<usrid>/settings")
def settingPage(usrid):
    if "usrid" in session:
        if session["usrid"] == usrid:
            userData = models.staff().get(where=f"id = '{usrid}';")[0]
            Name = userData[1]
            paswd = userData[2]
            return render_template(
                "otherfeatures/setting.html",
                usrid = usrid,
                usrnm = Name,
                paswd = paswd
                )
        else:
            return error_msg
    else:
        return redirect("/")

if __name__ == "__main__":  # If file open with apache it will not work
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
