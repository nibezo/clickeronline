from typing import Optional

from fastapi import FastAPI, Path, Cookie, Body
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import sqlite3 as sq
import hashlib
import random
import string
import time

def generate_token(length):
    letters = string.ascii_lowercase
    access_token = ''.join(random.choice(letters) for i in range(length))
    return access_token


app = FastAPI()

with sq.connect('db.sqlite') as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        score INTEGER NOT NULL,
        token TEXT NOT NULL,
        boost TEXT NOT NULL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS king(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL
    )""")


@app.get("/")
def main(access_token: Optional[str] = Cookie(default=None)):
    if access_token == None:
        return FileResponse("frontend/login/login.html")
    else:
        if(check_token(access_token)):
            return FileResponse("frontend/app/app.html")
        else:
            return {"message": "Такого токена не существует"}


def check_token(access_token):
    connection = sq.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * from users WHERE token = (?)",(access_token,))
    result = cursor.fetchone()
    connection.close()
    isTokenValid = False
    if result != None:
        isTokenValid = True
    return {"isTokenValid": isTokenValid}


def create_user(username, password, access_token):
    connection = sq.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO users(username, password, score, token) VALUES (?,?,?,?);""",(username,password,0,access_token))
    connection.commit()
    connection.close()


def find_user(username, password):
    connection = sq.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * from users WHERE username = (?) AND password = (?)",(username, password))
    result = cursor.fetchone()
    connection.close()
    hasAccount = False
    if result == None:
        hasAccount = True
    return hasAccount


def wrong_password(username, password):
    connection = sq.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * from users WHERE username = (?)",(username,))
    result = cursor.fetchone()
    connection.close()

    wrong_password = False
    if result != None and result[2] != password:
        wrong_password = True

    return wrong_password


def update_token(username, password, access_token):
    connection = sq.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET token = (?) WHERE username = (?) AND password = (?)", (access_token, username, password))
    connection.commit()
    connection.close()


@app.post("/signin")
def postdata(username: str = Body(embed=True,min_length=3, max_length=11),
             password: str =Body(embed=True,min_length=3, max_length=11)):
    password = password.encode()
    password = hashlib.md5(password).hexdigest()
    access_token = generate_token(20)
    hasAccount = find_user(username, password)
    if(hasAccount):
        if(wrong_password(username, password)):
            return False
        else:
            create_user(username, password, access_token)
    else:
        update_token(username, password, access_token)

    response = JSONResponse(content={"message": "OK"})
    response.set_cookie(key="access_token", value=access_token, max_age=250000)
    return response


@app.post("/logout")
def logout():
    response = JSONResponse(content={"message": "OK"})
    access_token = "False"
    response.set_cookie(key="access_token", value=access_token, max_age=-1)
    return response


app.mount("/frontend", StaticFiles(directory="frontend"))


@app.get("/click")
def click(access_token: Optional[str] = Cookie(default=None)):
    if access_token != None and check_token(access_token):
        connection = sq.connect('db.sqlite')
        cursor = connection.cursor()
        cursor.execute("SELECT * from users WHERE token = (?)", (access_token,))
        result = cursor.fetchone()
        current_time = int(time.time())
        click_count = 1
        try:
            if current_time - int(result[5]) <= 60:
                click_count = 5
        except:
            click_count = 1

        cursor.execute("UPDATE users SET score = score + (?) WHERE token = (?)",(click_count,access_token,))
        connection.commit()
        connection.close()
        return {"click": click_count}
    else:
        return {"Status": "Error"}


@app.get("/profile")
def profile(access_token: Optional[str] = Cookie(default=None)):
    if access_token != None and check_token(access_token):
        connection = sq.connect('db.sqlite')
        cursor = connection.cursor()
        cursor.execute("SELECT * from users WHERE token = (?)",(access_token,))
        result = cursor.fetchone()
        cursor.execute("SELECT * from king ORDER BY id DESC LIMIT 1")
        king = cursor.fetchone()

        if king == None:
            king = "Короля нет!"
        else:
            king = king[1]

        connection.close()

        data = {
            "username": result[1],
            "money": result[3],
            "king": king,
        }

        return data
    else:
        return {"Status": "Error"}


@app.get("/leaderboard")
def leaderboard():
    connection = sq.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users ORDER BY score DESC")
    result = cursor.fetchmany(50)
    connection.close()

    data = {}
    id = 1

    for i in range(len(result)):
        tmp = {
            "username": result[i][1],
            "money": result[i][3],
        }
        data[id] = tmp
        id += 1

    return data


@app.get("/buymeme")
def profile(access_token: Optional[str] = Cookie(default=None)):
    if access_token != None and check_token(access_token):
        meme_price = 100
        connection = sq.connect('db.sqlite')
        cursor = connection.cursor()
        cursor.execute("SELECT * from users WHERE token = (?)",(access_token,))
        result = cursor.fetchone()
        connection.close()

        if(result[3] >= meme_price):
            connection = sq.connect('db.sqlite')
            cursor = connection.cursor()
            cursor.execute("UPDATE users SET score = score - 100 WHERE token = (?)", (access_token,))
            connection.commit()
            connection.close()
            return {"Status": "OK"}
        else:
            return {"Status": "Error"}


@app.get("/king")
def king(access_token: Optional[str] = Cookie(default=None)):
    if access_token != None and check_token(access_token):
        king_price = 1000
        connection = sq.connect('db.sqlite')
        cursor = connection.cursor()
        cursor.execute("SELECT * from users WHERE token = (?)",(access_token,))
        result = cursor.fetchone()
        connection.close()

        if(result[3] >= king_price):
            connection = sq.connect('db.sqlite')
            cursor = connection.cursor()
            cursor.execute("UPDATE users SET score = score - 1000 WHERE token = (?)", (access_token,))
            cursor.execute("""INSERT INTO king(username) VALUES (?);""",(result[1],))
            connection.commit()
            connection.close()
            return {"Status": "OK"}
        else:
            return {"Status": "Error"}


@app.get("/boost")
def boost(access_token: Optional[str] = Cookie(default=None)):
    if access_token != None and check_token(access_token):
        boost_price = 300
        connection = sq.connect('db.sqlite')
        cursor = connection.cursor()
        cursor.execute("SELECT * from users WHERE token = (?)",(access_token,))
        result = cursor.fetchone()
        connection.close()

        if(result[3] >= boost_price):
            connection = sq.connect('db.sqlite')
            cursor = connection.cursor()
            boost_time = int(time.time())
            cursor.execute("UPDATE users SET score = score - 300 WHERE token = (?)", (access_token,))
            cursor.execute("UPDATE users SET boost = (?) WHERE token = (?)", (boost_time,access_token))
            connection.commit()
            connection.close()
            return {"Status": "OK"}
        else:
            return {"Status": "Error"}


@app.get("/wipe")
def wipe(access_token: Optional[str] = Cookie(default=None)):
    if access_token != None and check_token(access_token):
        wipe_price = 1000000
        connection = sq.connect('db.sqlite')
        cursor = connection.cursor()
        cursor.execute("SELECT * from users WHERE token = (?)",(access_token,))
        result = cursor.fetchone()
        connection.close()

        if(result[3] >= wipe_price):
            connection = sq.connect('db.sqlite')
            cursor = connection.cursor()
            cursor.execute("UPDATE users SET score = 0")
            connection.commit()
            connection.close()
            return {"Status": "OK"}
        else:
            return {"Status": "Error"}