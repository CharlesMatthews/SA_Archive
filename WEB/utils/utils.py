import os
import secrets
from flask import Flask, jsonify, session, render_template, request, redirect, url_for, redirect, flash
from flask_session import Session
import psutil
#from textblob import TextBlob

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def getstats():
    CPU = psutil.cpu_percent()
    MEM = psutil.virtual_memory()
    UserTot = db.execute("SELECT COUNT(*) FROM users;").fetchone()
    TweetTot = db.execute("SELECT COUNT(*) FROM tweets;").fetchone()
    AuthorTot = db.execute("SELECT COUNT(*) FROM author;").fetchone()
    DataTot = (UserTot[0] * 7) + (AuthorTot[0]*12) + (TweetTot[0]*7)
    db.close()
    return CPU, MEM, UserTot, TweetTot, AuthorTot, DataTot


def cleantweet(tweet):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    emoji_patternII =	re.compile(u'['
    u'\U0001F300-\U0001F64F'
    u'\U0001F680-\U0001F6FF'
    u'\u2600-\u26FF\u2700-\u27BF]+',
    re.UNICODE)

    tweet =emoji_pattern.sub(r'', tweet)
    tweet =emoji_patternII.sub(r'', tweet)

    tweet = re.sub(r'http\S+', '', tweet)
    tweet = re.sub(r'pic.twitter.com\S+', '', tweet)
    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])(\w:\/\/\S+)", " ", tweet).split())

    return "".join(i for i in tweet if ord(i)<128)



def getsentiment(tweet):
    tweet = cleantweet(tweet)
    #tweet = TextBlob(tweet)
    return #tweet.sentiment

def apitokverif(utoken):
    if db.execute("SELECT * FROM users WHERE token = :tok", {"tok": utoken}).rowcount ==0:
        db.close()
        return False
    db.close()


def gettok():
    tok = session["utoken"]
    if tok:
        tok = str(''.join(tok[0]))
    return tok


def tokenverif(AuthWall):
    """Checks the user token's validity -
    >> if it has been revoked then resets the session utoken.
    >> Handles AuthWall"""
    utoken = gettok()
    if utoken:
        if db.execute("SELECT * FROM users WHERE token = :tok", {"tok": utoken}).rowcount == 0:
            session["utoken"] = []
            flash("Invalid Token")
            db.close()
            return False
        db.close()
    if AuthWall:
        if db.execute("SELECT * FROM users WHERE token = :tok", {"tok": utoken}).rowcount == 0:
            flash("You need to be logged in to perform this action.")
            db.close()
            return False
        db.close()
    return True


def sessiongen(AuthWall):
    """Creates a user session if does not already exist - calls token verification if not empty"""
    if session.get("utoken") is None:
        session["utoken"] = []
    else:
        return tokenverif(AuthWall)

def getauthoridhandle(handle):
    result = db.execute("SELECT authorid FROM author WHERE handle =  :hdl", {"hdl": handle}).fetchone()

    return result[0]



def getcollist(table):
    collist =[]
    results = db.execute("SELECT column_name FROM information_schema.columns WHERE table_name = :table", {"table": table})
    for item in results:
        for extract in item:
            collist.append(extract)
    return collist


def buildjson(collist, data):
    objectlist=[]
    for item in data:
        temphold = []
        for index, value in enumerate(collist):
            temphold.append(str(collist[index]) +":"+ str(item[index]))
        objectlist.append(temphold)
    return objectlist



def tokengen():
    return secrets.token_urlsafe(30)
def hashpw(pw):
    return sha256_crypt.encrypt(pw)
def verifyhash(pw, pwh):
    return sha256_crypt.verify(pw, pwh)
