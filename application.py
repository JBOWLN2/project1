import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from pprint import pprint

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    #return "Project 1: TODO"

    session['found'] = False
    return render_template("index.html")


@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def post_register():
    fname = request.form.get("fname")
    username = request.form.get("username")
    password = request.form.get("password")
    db.execute("INSERT INTO users (username, password) VALUES (:u, :p)",
        {"u": username, "p": password})
    db.commit()
    return render_template("regsuccess.html", username=username, fname=fname.capitalize())

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    result = db.execute("SELECT FROM users WHERE username=:u AND password=:p",
        {"u": username, "p": password})
    db.commit()
    session['logged_in'] = True
    return render_template("index.html")
    #return str(result.rowcount)

@app.route("/search", methods=["POST"])
def search():
        #session["found"] = False
        if not session['logged_in']:
            return 'error, please login'
        else:
            session["found"] = True
            search_term = request.form.get("loc_search")
            query = "SELECT * FROM zips WHERE city LIKE '%"+search_term+"%' OR zip LIKE '%"+search_term+"%'"

            query_results = db.execute(query)
            db.commit()
            results = []
            for row in query_results:
                results.append(row)
            print(results)
            return render_template("index.html", results=results)

@app.route("/location/<zipcode>")
def location(zipcode):
    if zipcode == '':
        return "error"
    else:
        query_results = db.execute("SELECT * FROM zips where zip=:z", {"z": zipcode})
        db.commit()

        results = []
        for row in query_results:
            results.append(row)

        results = results[0]

        return render_template("locations.html", results=results)

@app.route("/nav")
def nav():
    return render_template("nav.html")