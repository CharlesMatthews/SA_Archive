#import twint
import sqlite3

import os
import secrets

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



def insertintodb():
    with sqlite3.connect("scraped.db") as connection:
        c = connection.cursor()
        c.execute("SELECT id, date, time, tweet, likes, retweets, replies FROM tweets")
        rows = c.fetchall()



def scrapeaccount(handle):
    c = twint.Config()
    c.Username = handle
    c.Store_json = True
    c.Database = "scraped.db"

    print("==================")
    twint.run.Search(c)
    print("==================")
    twint.run.Profile(c)
