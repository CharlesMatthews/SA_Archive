#!/usr/bin/python3
import os
import requests
import secrets
import json
import collections


from flask import Flask, jsonify, session, render_template, request, redirect, url_for, redirect, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


import WEB.utils.utils as ut
import WEB.utils.scraper as scr
import DataPush.KingPush as kp
#import nn.rnn_handle as nn


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





#START OF WEBPAGE ROUTES===================================================

@app.route("/")
def index():
    ut.sessiongen(False)
    return render_template("index.html", logged_in=session["utoken"])


@app.route("/register", methods=['GET', 'POST'])
def register():
    ut.sessiongen(False)
    if request.method == 'POST':
        upw = request.form.get("Password")
        pwh = ut.hashpw(upw)
        ufn = request.form.get("Fname")
        uln = request.form.get("Lname")
        eml = request.form.get("Email")
        tok = ut.tokengen()
        #Check if username is unique
        if upw == "" or eml == "" or uln == "" or ufn == "":
            flash("Invalid form entry")
            return redirect(url_for('register'))

        if db.execute("SELECT * FROM users WHERE email = :eml", {"eml": eml}).rowcount != 0:
            db.close()
            flash("Account already exists - Please try again or reset your password")
            return redirect(url_for('register'))
        else:
            db.execute("INSERT INTO users(email, firstname, lastname, passwordhash, token) VALUES (:eml, :fname, :lname, :pwh, :tok)",
            {"eml": eml, "fname": ufn, "lname": uln, "pwh": pwh, "tok": tok})
            db.commit()
            db.close()
            return redirect(url_for('login'))
    return render_template("register.html", logged_in=session["utoken"])


@app.route("/login", methods=['GET', 'POST'])
def login():
    ut.sessiongen(False)
    if request.method == 'POST':
        eml = request.form.get("Email")
        upw = request.form.get("Password")
        if db.execute("SELECT * FROM users WHERE email = :eml", {"eml": eml}).rowcount == 0:
            flash("Invalid credentials - User does not exist")
        else:
            #Check password is correct
            pwh = db.execute("SELECT passwordhash FROM users WHERE email = :eml", {"eml": eml}).fetchone()
            if ut.verifyhash(upw,pwh[0]) == True:
                flash("Login Success")
                data = db.execute("SELECT token FROM users WHERE email = :eml", {"eml": eml}).fetchall()
                #Add token to user session
                for item in data:
                    session["utoken"].append(item)
                    db.close()
                return redirect(url_for('account'))
            else:
                db.close()
                flash("Invalid credentials - Password")
                return  redirect(url_for('login'))
            #error = db.execute("SELECT password FROM users WHERE username = :username", {"username": uun}).fetchone()
    return render_template("login.html", logged_in=session["utoken"])


@app.route("/forgot", methods=['GET', 'POST'])
def forgot():
    ut.sessiongen(False)
    if request.method == 'POST':
        eml = request.form.get("Email")
        flash("Thanks - Expect an email from us shortly! 👀")
        return redirect(url_for('index'))
    return render_template("forgot.html",logged_in=session["utoken"])



##############################################################
#
#
##############################################################


@app.route("/reset", methods=['GET', 'POST'])
def reset():
    ut.sessiongen(False)
    if request.method == 'POST':
        eml = request.form.get("Email")
        flash("Thanks - Expect an email from us shortly! 👀")
        return redirect(url_for('index'))
    return render_template("forgot.html",logged_in=session["utoken"])

@app.route("/verify", methods=['GET', 'POST'])
def verify():
    ut.sessiongen(False)
    if request.method == 'POST':
        eml = request.form.get("Email")
        flash("Thanks - Expect an email from us shortly! 👀")
        return redirect(url_for('index'))
    return render_template("forgot.html",logged_in=session["utoken"])
##############################################################
#
#
##############################################################


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    ut.sessiongen(False)
    if session["utoken"] != []:
        session["utoken"] = []
        flash("Logged out sucessfully!")
        return redirect(url_for('index'))



@app.route("/search")
def search():
    if ut.sessiongen(True) == False:
        return redirect(url_for('index'))
    query = request.args.get('search')
    query = '%' + query + "%"

    param = request.args.get('parameter')
    if param == "account":
        data = db.execute("SELECT * FROM author WHERE handle LIKE :query OR screename LIKE :query",{"query": query}).fetchall()

    else:
        data = db.execute("SELECT * FROM tweets WHERE text LIKE :query", {"query": query}).fetchall()
    print(data)

    return render_template("search.html", data=data, param=param, logged_in=session["utoken"])

@app.route("/app")
def dashboard():
    if ut.sessiongen(True) == False:
        return redirect(url_for('index'))

    CPU, MEM, UserTot, TweetTot, AuthorTot, DataTot = ut.getstats()



    RECENT3=data = db.execute("SELECT * FROM tweets LIMIT 3 ").fetchall()
    TOP3= db.execute("SELECT * FROM tweets ORDER BY retweets DESC LIMIT 3").fetchall()
    RANDOM = db.execute("SELECT * FROM tweets ORDER BY random() LIMIT 1").fetchall()

    ACLIST =  db.execute("SELECT handle, followertot FROM author ORDER BY followertot DESC LIMIT 5").fetchall()

    return render_template("webapp.html",aclist=aclist,TOP3=TOP3,RECENT3=RECENT3,RANDOM=RANDOM, ACLIST=ACLIST, logged_in=session["utoken"], CPU = CPU, MEM = MEM, UserTot = UserTot[0], TweetTot = TweetTot[0], AuthorTot = AuthorTot[0], DataTot = DataTot)


@app.route("/app/<handle>")
def AuthorPage(handle):
    if ut.sessiongen(True) == False:
      return redirect(url_for('index'))
    """Returns list of users following the specified account."""
    if db.execute("SELECT * FROM author WHERE handle = :hdl", {"hdl": handle}).rowcount == 0:
        flash("Requested user does not exist")
        return redirect(url_for('index'))
    authorid = ut.getauthoridhandle(handle)
    data =  db.execute("SELECT * FROM author WHERE handle = :hdl", {"hdl": handle}).fetchone()

    RECENT3= db.execute("SELECT * FROM tweets WHERE authorid = :aid LIMIT  3", {"aid": authorid}).fetchall()
    RANDOM = db.execute("SELECT * FROM tweets WHERE authorid =  :aid ORDER BY random() LIMIT 3", {"aid": authorid}).fetchall()
    TOP3 =db.execute("SELECT * FROM tweets WHERE authorid = :aid ORDER BY retweets DESC LIMIT 3 ", {"aid": authorid}).fetchall()

    db.close()
    trained=False
    if handle == "@realDonaldTrump":
        trained = True
    return render_template("author.html",data = data, trained=trained,TOP3=TOP3,RECENT3=RECENT3,RANDOM=RANDOM, logged_in=session["utoken"])

##############################################################
#           #
    #   #
#           #
###########################################################



@app.route("/app/<author>/tweets")
def AuthorTweetsPage(author):
    if ut.sessiongen(True) == False:
      return redirect(url_for('index'))
    """Returns list of users following the specified account."""
    if author != "*" and db.execute("SELECT * FROM author WHERE handle = :hdl", {"hdl": author}).rowcount == 0:
        flash("Requested user does not exist")
        return redirect(url_for('index'))
    return render_template("tweetspage.html", Account_Name = author, logged_in=session["utoken"])

@app.route("/scraper", methods=['GET', 'POST'])
def scraper():
    if ut.sessiongen(True) == False:
      return redirect(url_for('index'))
    """Returns the page for requesting an account to be scraped."""
    tok = ut.gettok()
    Credits =  db.execute("SELECT credits FROM users WHERE token = :tok", {"tok": tok}).fetchone()

    if request.method == 'POST':
        if Credits[0] == 0:
            flash("Insufficient Credits.")
            return redirect(url_for('scraper'))
        else:
            db.execute("UPDATE users SET credits = credits - 1 where token = :tok", {"tok": tok})
            db.commit()
            hdl = request.form.get("Handle")
            flash("Thanks! We've received your request for scraping @" +str(hdl) + ". Expect an email from us shortly! 👀")
            scr.scrapeaccount(hdl)
            db.close()
            return redirect(url_for('scraper'))
    db.close()
    return render_template("scraper.html", logged_in=session["utoken"], Credits=Credits[0])






@app.route("/api")
def api():
    """
    Page for API documentation.
    """
    if ut.sessiongen(True) == False:
      return redirect(url_for('index'))
    return render_template("api.html",logged_in=session["utoken"])

@app.route("/about")
def about():
    """
        About page of service.
    """
    if ut.sessiongen(True) == False:
      return redirect(url_for('index'))
    return render_template("about.html",logged_in=session["utoken"])


@app.route("/stats")
def stats():
    """
    Stats page for the service. Serverload + db etc.
    """
    if ut.sessiongen(True) == False:
      return redirect(url_for('index'))
    CPU, MEM, UserTot, TweetTot, AuthorTot, DataTot = ut.getstats()

    return render_template("stats.html",logged_in=session["utoken"], CPU = CPU, MEM = MEM, UserTot = UserTot[0], TweetTot = TweetTot[0], AuthorTot = AuthorTot[0], DataTot = DataTot)

@app.route("/aclist")
def aclist():
    """
    Displays list of scraped Accounts within the database
    """
    if ut.sessiongen(True) == False:
      return redirect(url_for('index'))

    aclist = db.execute("SELECT avatar, screename, handle, verified FROM author").fetchall()

    return render_template("aclist.html", aclist = aclist, logged_in=session["utoken"])

@app.route("/account")
def account():
    """
    User account page
    """
    if ut.sessiongen(True) == False:
      return redirect(url_for('index'))
    #Get logged in user's ID from session token
    tok = ut.gettok()
    FirstName = db.execute("SELECT firstname FROM users WHERE token = :tok", {"tok": tok}).fetchone()
    Credits =  db.execute("SELECT credits FROM users WHERE token = :tok", {"tok": tok}).fetchone()
    db.close()
    return render_template("account.html",logged_in=session["utoken"],FirstName = FirstName[0], Credits = Credits[0])



#API ROUTES  FROM HERE ON OUT =======================================================

@app.route("/api/<author>/data")
def ApiAuthorData(author):
    """Returns Account data for the specified user
    Example Request:

    Example Response:
    """
    authorid = ut.getauthoridhandle(author)
    if authorid == "":
        flash("Invalid Username parameter")
        return redirect(url_for('index'))

    tok = request.args.get('token')

    if ut.apitokverif(tok) == False:
        flash("Invalid Token")
        return redirect(url_for('index'))


    data = db.execute("SELECT * FROM author WHERE handle = :hdl", {"hdl": author}).fetchall()
    collist = ut.getcollist("author")
    db.close()
    return jsonify(ut.buildjson(collist, data))



@app.route("/api/<author>/toptweet")
def ApiAuthortTop(author, methods=['POST', 'GET']):
    """Returns the top tweet of the specified user"""
    end = request.args.get('end')
    tok = request.args.get('token')

    if author != "*":
        authorid = ut.getauthoridhandle(author)
        if authorid == "":
            flash("Invalid Username parameter")
            return redirect(url_for('index'))

    if ut.apitokverif(tok) == False:
        flash("Invalid Token")
        return redirect(url_for('index'))

    if author != "*":
        data = db.execute("SELECT * FROM tweets WHERE authorid = :aid ORDER BY retweets DESC LIMIT :lim", {"aid": authorid, "lim": end}).fetchall()
    else:
        data = db.execute("SELECT * FROM tweets ORDER BY retweets DESC LIMIT :lim", {"lim": end}).fetchall()

    db.close()
    collist = ut.getcollist("tweets")
    #message = data
    #return render_template("error.html", message =message, logged_in=session["utoken"])

    return jsonify(ut.buildjson(collist, data))

@app.route("/api/<author>/tweets")
def ApiAuthorTweets(author, methods=['POST', 'GET']):
    """Returns Tweet archive of specified user
        Example Request:

        Example Response:

    """
    tok = request.args.get('token')

    if ut.apitokverif(tok) == False:
        flash("Invalid Token")
        return redirect(url_for('index'))

    offset = request.args.get('offset')
    end = request.args.get('end')
    random = request.args.get('random')


    if author != "*":
        authorid = ut.getauthoridhandle(author)
        if random == "true":
            data = db.execute("SELECT * FROM tweets WHERE authorid =  :aid ORDER BY random() LIMIT :lim OFFSET :off ", {"off": offset, "lim": end, "aid": authorid}).fetchall()
        else:
            data = db.execute("SELECT * FROM tweets WHERE authorid =  :aid LIMIT :lim OFFSET :off ", {"off": offset, "lim": end, "aid": authorid}).fetchall()
    else:
        if random == "true":
            data = db.execute("SELECT * FROM tweets ORDER BY random() LIMIT :lim OFFSET :off ", {"off": offset, "lim": end}).fetchall()
        else:
            data = db.execute("SELECT * FROM tweets LIMIT :lim OFFSET :off ", {"off": offset, "lim": end}).fetchall()

    collist = ut.getcollist("tweets")
    db.close()

    return jsonify(ut.buildjson(collist, data))




##############################################################
#
#
#
#
###########################################################

@app.route("/api/<author>/export")
def ApiAuthorExport(author, methods=['POST', 'GET']):
    """Returns Tweet archive of specified user
        Example Request:

        Example Response:

    """
    tok = request.args.get('token')

    if ut.apitokverif(tok) == False:
        flash("Invalid Token")
        return redirect(url_for('index'))

    Action = kp.PUSHA(author, tok)
    link = Action.TweetExport()
    flash("Thanks - Expect an email from us shortly! 👀")
    flash("Or access the file here:")
    flash(link)

    db.close()
    return redirect(url_for('index'))



@app.route("/api/getsentiment")
def ApiSentiment():
    """Cleans Data and returns Textblob Output for sentiment
        Example request:
        /api/verify?tweetid=6383742937362836&token=hufildshuiey4739
        Response:


    """
    tok = request.args.get('token')
    tweetid = request.args.get('tweetid')
    if ut.apitokverif(tok) == False:
        flash("Invalid Token")
        return redirect(url_for('index'))
    if tweetid == "":
        flash("Invalid tweetid parameter")
        return redirect(url_for('index'))

    #Other possible fields: msg, desc, reason.
    return jsonify(data['valid'])

##############################################################
#
#
#
#
#
#
#
#
###########################################################




@app.route("/api/neuralnet")
def ApiRNN():
    """Cleans Data and returns Textblob Output for sentiment
        Example request:
        /api/verify?tweetid=6383742937362836&token=hufildshuiey4739
        Response:


    """
    tok = request.args.get('token')

    if ut.apitokverif(tok) == False:
        flash("Invalid Token")
        return redirect(url_for('index'))


    print(os.getcwd())

    filepath = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    filepath = os.path.join(filepath,"nn", "generated_output.txt")

    file = open(filepath, "r")

    message = file.read()
    #message = nn.rnn_getresult()


    return render_template("nnout.html", message =message)


@app.route("/api/authors", methods=['POST', 'GET'])
def ApiAuthorList():
    """Returns list of available accounts along with associated account data.
    """
    tok = request.args.get('token')

    if ut.apitokverif(tok) == False:
        flash("Invalid Token")
        return redirect(url_for('index'))

    offset = request.form.get("offset")
    end = request.form.get("end")
    objectlist =[]

    if src == "app":
        data = db.execute("SELECT * FROM author LIMIT :lim OFFSET :off ORDER BY followertot", {"off": offset, "lim": end}).fetchall()
    else:
        data = db.execute("SELECT * FROM author LIMIT :lim OFFSET :off", {"off": offset, "lim": end}).fetchall()
    collist = ut.getcollist("author")
    db.close()

    return jsonify(ut.buildjson(collist, data))




@app.route("/api/verify")
def ApiVerify():
    """Verifies the existance of a twitter username by making a request though the webhost rather than Twitterself.
        Example request:
        /api/verify?username=realDonaldTrump
        Response:
        Returns false if name is taken -> exists
        Otherwise if not taken returns false
    """
    tok = request.args.get('token')
    username = request.args.get('username')
    if ut.apitokverif(tok) == False:
        flash("Invalid Token")
        return redirect(url_for('index'))
    if username == "":
        flash("Invalid Username parameter")
        return redirect(url_for('index'))
    r = requests.get('https://twitter.com/users/username_available?username=' + username )
    data = r.json()
    #Other possible fields: msg, desc, reason.
    return jsonify(data['valid'])
