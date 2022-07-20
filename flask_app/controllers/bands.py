from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.band import Band
from flask_app.models.user import User
from flask_app.models.member import Member

# ---------- Dashboard ----------

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session: 
        flash("Please log in or register before viewing site")

    bands = Band.get_all()
    data = {"id":session["user_id"]}
    joined_bands = Band.get_joined_bands(data)
    # joined bands is for the many to many that I have removed for now
    return render_template('dashboard.html', bands = bands, joined_bands = joined_bands, user_id = session["user_id"], first_name = session["first_name"], last_name = session["last_name"])

# ---------- New Band Routes ----------

@app.route('/new')
def new_render():
    return render_template('new_band.html', user_id = session["user_id"], first_name = session["first_name"], last_name = session["last_name"])

@app.route('/new/band', methods = ['POST'])
def new_band(): 
    if not Band.validate_band(request.form): 
        return redirect('/add_new')

    data = {
        "user_id": session['user_id'],
        "name": request.form['name'],
        "genre": request.form['genre'],
        "home_city": request.form['home_city'],
        # the founding member is the loggin in user
        "founding_member": session["first_name"] + " " + session["last_name"]
    }
    
    Band.add_new_band(data)
    return redirect('/dashboard')

# ---------- Edit Band Routes----------

@app.route('/edit/<int:id>')
def edit_render(id):
    data = {"id":id}
    band = Band.get_one(data)
    return render_template('edit_band.html', band = band, user_id = session["user_id"], first_name = session["first_name"], last_name = session["last_name"], id = id)

@app.route('/edit/band/<int:id>', methods=['POST'])
def edit(id):
    if not Band.validate_band(request.form): 
        return redirect(f'/edit/{id}') # use fstring for redirect- cant use the other syntax
    
    data = {
        "id": id,
        "name": request.form['name'],
        "genre": request.form['genre'],
        "home_city": request.form['home_city']
    }

    Band.edit_band(data)
    return redirect('/dashboard')

# ---------- View Bands ----------

@app.route('/my_bands/<int:user_id>')
def my_bands(user_id):
    data = {"user_id": user_id}
    my_bands = User.get_bands(data)
    # joined_bands = Band.get_joined_bands(data)
    # joined bands is for many to many, read /quit route below
    return render_template('my_bands.html',my_bands = my_bands, user_id = session["user_id"], first_name = session["first_name"])

@app.route('/band/<int:id>')
def one_band(id):
    data = {"id": id}
    band_info = Band.get_one(data)
    return render_template('one_band.html', band = band_info, user_id = session["user_id"], first_name = session["first_name"])

# ---------- Delete a Band ----------

@app.route('/delete/<int:id>')
def delete_band(id):
    data = {"id": id}
    Band.delete(data)
    return redirect('/dashboard')

# ---------- Join and Quit Band Routes ----------

@app.route('/join_band/<int:band_id>/<int:user_id>')
def join(band_id, user_id):
    # this is user, id
    data = {
        "band_id": band_id,
        # need the member id, not user ID
        "user_id": user_id
        }
    Member.join(data)
    return redirect('/dashboard')

# this needs to return the member_id, not user or band -- I havent yet found a way to get the member_id to be connected to the join/quit link, its required to be fully functional; everything else is complete.
@app.route('/quit_band/<int:member_id>')
def quit(member_id):
    data = {"member_id": member_id}
    Member.quit(data)
    return redirect('/dashboard')
