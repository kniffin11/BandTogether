from flask_app.controllers import bands, users
from flask_app import app # pulls the app from the init py file that is within the flask_app folder

if __name__ == "__main__":
    app.run(debug = True)