from flask import Blueprint, render_template, request, session, flash, redirect
import models

Login = Blueprint('login',__name__)     # For making a divided file of flask-app


# Rendering Login form page

@Login.route("/login")
def loginForm():    # Login Page
    return render_template("login.html")


# Process login request

@Login.route("/login/request", methods=['POST'])
def loginSubmit():  # Check validity for login
    login = False

    usrnm = request.form["usrid"]       # User ID
    paswd = request.form["password"]    # Password

    #mycursor.execute("SELECT * FROM riphah.staf")
    myresult = models.staff().get()

    error_in_login = ["", ""]   # For flash messages

    for entity in myresult:     # Loop which searches user id and password match
        if str(entity[0]) == usrnm or str(entity[1]) == usrnm:
            if entity[2] == paswd:      # If username and password match user will login
                session["usrid"] = str(entity[0])
                login = True    # For procceding
            else:
                error_in_login[1] = "Wrong password"
        else:
            continue
    """
    _Error in login_

        As we have found error of password mismatch if loop is end and user is not login.
        It means user had enter wrong Id.
        So now we will flash wrong id error to the user.
    
    """
    if not login:   # Used to send only specific error on login
        if error_in_login == ["", ""]:
            error_in_login[0] = "ID not found"  # This is because if user id doesn't found
        
        flash(error_in_login[0])
        flash(error_in_login[1])

        return redirect(request.referrer)
    else:
        return redirect('/')    # _Required return_ If user login


# Loging out the user

@Login.route("/logout")
def logout():
    if "usrid" in session:
        session.pop("usrid")
    return redirect('/')