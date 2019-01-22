import os

from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#User database setup
#Need essentials + auth & credit sys.
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.TEXT, nullable=False)
    lastname = db.Column(db.TEXT, nullable=False)
    token = db.Column(db.TEXT, nullable=False)
    credits = db.Column(db.Integer, nullable=False, default=0)
    verified = db.Column(db.Boolean,nullable=False, default=f)

# Author of tweets
    # Overall summary data here & Account information.
class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String, nullable=False)
    screenname = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=False)
    followertot = db.Column(db.Integer,nullable=False)
    followingtot = db.Column(db.Integer,nullable=False)
    liketot = db.Column(db.Integer,nullable=False)
    mediatot = db.Column(db.Integer,nullable=False)
    verified = db.Column(db.Boolean,nullable=False)
    private = db.Column(db.Boolean,nullable=False)
    joindatetime = db.Column(db.DATETIME,nullable=False)
    avatar = db.Column(db.String, nullable=False)

# Tweet entry themselves
    # Key properties of the tweet.
    #  + Storage of the summary & sentiment results to reduce repeated requests & assoc. processing.
class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    authorid = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    hashtags = db.Column(db.String, nullable=False)
    mentions = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer,nullable=False)
    retweets = db.Column(db.Integer,nullable=False)
    replies = db.Column(db.Integer,nullable=False)
    updatetime = db.Column(db.DATETIME,nullable=False)
    sentimentscore =  db.Column(db.Decimal,nullable=False)

#Followers table:
    # Many to many relationship for displaying the following
    # / followed users of a particular author.
class Followers(db.Model):
    __tablename__ = 'Followers'
    userid = db.Column(db.Integer, primary_key=True)
    followerid = db.Column(db.Integer, nullable=False)
