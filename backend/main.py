from typing import Optional

from fastapi import FastAPI, Path, Cookie, Form
from fastapi.responses import JSONResponse
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
        return {"message": "Куки нет"}
    else:
        return {"message": f"Вот ваш токен: {access_token}"}

def check_token(access_token):
    connection = sq.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * from users WHERE token = (?)",(access_token))
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
    cursor.execute(f"SELECT * from users WHERE username = (?) AND password = (?)",(username, password))
    result = cursor.fetchone()
    connection.close()
    hasAccount = False
    if result == None:
        hasAccount = True
    return hasAccount

def update_token(username, password, access_token):
    connection = sq.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE users SET token = (?) WHERE username = (?) AND password = (?)", (access_token, username, password))
    connection.commit()
    connection.close()

@app.post("/signin")
def postdata(username: str = Form(min_length=3, max_length=20),
             password: str =Form(min_length=3, max_length=20)):
    password = password.encode()
    password = hashlib.md5(password).hexdigest()
    access_token = generate_token(20)
    hasAccount = find_user(username, password)
    if(hasAccount):
        create_user(username, password, access_token)
    else:
        update_token(username, password, access_token)

    response = JSONResponse(content={"message": "OK"})
    response.set_cookie(key="access_token", value=access_token)
    return response

@app.get("/click")
def users(id: int = Path(ge = 1)):
    return {"user_id": id}

@app.get("/leaderboard")
def users(id: int = Path(ge = 1)):
    return {"user_id": id}