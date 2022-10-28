from typing import Optional

from fastapi import FastAPI, Path, Cookie, Body
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import sqlite3 as sq
import hashlib
import random
import string


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
        token TEXT NOT NULL
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


@app.post("/click")
def click(access_token: Optional[str] = Cookie(default=None)):
    if access_token != None and check_token(access_token):
        connection = sq.connect('db.sqlite')
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET score = score + 1 WHERE token = (?)",(access_token,))
        connection.commit()
        connection.close()
        return {"Status": "OK"}
    else:
        return {"Status": "Error"}


@app.get("/profile")
def profile(access_token: Optional[str] = Cookie(default=None)):
    if access_token != None and check_token(access_token):
        connection = sq.connect('db.sqlite')
        cursor = connection.cursor()
        cursor.execute("SELECT * from users WHERE token = (?)",(access_token,))
        result = cursor.fetchone()
        connection.close()

        data = {
            "username": result[1],
            "money": result[3],
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
