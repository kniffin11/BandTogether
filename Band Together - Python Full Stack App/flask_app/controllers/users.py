from wsgiref import validate
from flask_app import app
from flask import render_template,redirect,request,session,flash 
from flask_app.models.user import User
from flask_app.models.band import Band
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def log_in():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def new_user():
    # validate user, if false return to page and try again
    if not(User.validate_registration(request.form)):
        return redirect('/')

    # if user is validated successfully
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }

    user_id = User.new_user(data)
    session['user_id'] = user_id
    # if user is created and doesnt log in - name still needed
    logged_in_user = User.get_by_email(data)
    session['first_name'] = logged_in_user.first_name
    session['last_name'] = logged_in_user.last_name
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')

    data = {
        "email" : request.form["email"]
    }
    logged_in_user = User.get_by_email(data)
    # this sets teh session id
    session['user_id'] = logged_in_user.id
    session['first_name'] = logged_in_user.first_name
    session['last_name'] = logged_in_user.last_name
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session: 
        flash("Please log in or register before viewing site")
    bands = Band.get_all()
    return render_template('index_dashboard.html', bands = bands, user_id = session["user_id"], first_name = session["first_name"], last_name = session["last_name"])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')