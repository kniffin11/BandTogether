from flask_app import app
from flask import render_template,redirect,request,session 
from flask_app.models.band import Band
from flask_app.models.user import User

# only an app route can use this carrot syntax
@app.route('/edit/<int:id>')
def edit_render(id):
    return render_template('index_edit_band.html', user_id = session["user_id"], first_name = session["first_name"], last_name = session["last_name"], id = id)

@app.route('/edit_band/<int:id>', methods=['POST'])
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

@app.route('/add_new')
def new_render():
    return render_template('index_new_band.html', user_id = session["user_id"], first_name = session["first_name"], last_name = session["last_name"])

@app.route('/new/sighting', methods = ['POST'])
def new_show(): 
    if not Band.validate_band(request.form): 
        return redirect('/add_new')
    # the founding member is the loggin in user

    # get use by join query
    first_name = session["first_name"]
    last_name = session["last_name"]
    founder = first_name + " " + last_name

    data = {
        "user_id": session['user_id'],
        "name": request.form['name'],
        "genre": request.form['genre'],
        "home_city": request.form['home_city'],
        "founding_member": founder
    }
    
    Band.add_new_band(data)
    return redirect('/dashboard')

@app.route('/mybands/<int:id>')
def mybands(id):
    data = {"id": id}
    all_bands = User.get_bands(data)
    return render_template('index_my_bands.html',all_bands = all_bands, user_id = session["user_id"], first_name = session["first_name"], last_name = session["last_name"])

@app.route('/delete/<int:id>')
def delete_band(id):
    data = {"id": id}
    Band.delete(data)
    return redirect('/dashboard')

@app.route('/join_band')
def join():
    pass

@app.route('/quit_band')
def quit():
    pass
