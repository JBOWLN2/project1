import os
import json
import requests
from flask import Flask, session, render_template, request, redirect, url_for, jsonify, abort
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
    if 'logged_in' not in session:
        session['logged_in'] = False
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
    session['error'] = ''
    username = request.form.get("username")
    password = request.form.get("password")
    result = db.execute("SELECT FROM users WHERE username=:u AND password=:p",
        {"u": username, "p": password})
    db.commit()
    session['logged_in'] = True
    session['username'] = username
    return render_template("index.html")
    #return str(result.rowcount)

@app.route("/search", methods=["POST"])
def search():
        session["found"] = False
        session['search_error'] = ''
        session['error'] = ''
        if not session['logged_in']:
            session["error"] = "Please login to search"
            return render_template("index.html")
        else:
            session["found"] = True
            search_term = request.form.get("loc_search")
            query = "SELECT * FROM zips WHERE LOWER(city) LIKE '%"+search_term.lower()+"%' OR zip LIKE '%"+search_term+"%'"

            query_results = db.execute(query)
            db.commit()
            results = []
            for row in query_results:
                results.append(row)
            if not results:
                session['search_error'] = 'No results found'
                return render_template("index.html")
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

        weather = requests.get("https://api.darksky.net/forecast/560a289d9a108079c47564ebf2fbaad0/"+ str(results['lat']) +"," + str(results['long'])).json()
        data = weather['currently']
        data['zip'] = results['zip']
        data['city'] = results['city']
        data['state'] = results['state']
        data['lat'] = results['lat']
        data['long'] = results['long']
        data['population'] = results['pop']
        data['checkcount'] = results['checkcount']

        checkin_query_results = db.execute("SELECT * FROM checkins where userid=:u and loc=:z", {"u": session['username'], "z": zipcode})
        db.commit()
        checkin_results = []
        for row in checkin_query_results:
            checkin_results.append(row)

        if not checkin_results:
            data['comment'] = ''
        else:
            checkin_results = checkin_results[0]
            data['comment'] = checkin_results['comnts']
        return render_template("locations.html", results=data)

@app.route("/comment", methods=["POST"])
def comment():
    comment = request.form['comment']
    zipcode = request.form['zipcode']

    location_query = db.execute("UPDATE zips SET checkcount=checkcount+1 where zip=:z", {"z": zipcode})
    db.commit()

    comment_query = db.execute("INSERT INTO checkins(userid, loc, comnts) VALUES(:u, :l, :c)", {"u": session['username'], "l": zipcode, "c": comment})
    db.commit()
    return redirect(url_for("location", zipcode=zipcode))
@app.route("/api/<zipcode>")
def api(zipcode):
    if 'zipcode' == '':
        return jsonify({"error": "please specify a valid zipcode"})
    else:
        query_results = db.execute("SELECT * FROM zips where zip=:z", {"z": zipcode})
        db.commit()

        results = []
        for row in query_results:
            results.append(row)

        if not results:
            return abort(404)
        else:
            results = results[0]
            data = {}
            data['zip'] = results['zip']
            data['city'] = results['city']
            data['state'] = results['state']
            data['lat'] = results['lat']
            data['long'] = results['long']
            data['population'] = results['pop']
            return jsonify(data)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = ''
    return redirect(url_for("index"))


@app.route("/nav")
def nav():
    return render_template("nav.html")