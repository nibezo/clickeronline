from fastapi import FastAPI, Path, Cookie, Form
from fastapi.responses import JSONResponse
import sqlite3 as sq
import hashlib


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
def main(access_token = Cookie()):

    return {"Status": "OK" + access_token}

@app.post("/signin")
def postdata(username: str = Form(min_length=3, max_length=20),
             password: str =Form(min_length=3, max_length=20)):
    password = password.encode()
    password = hashlib.md5(password).hexdigest()
    token = "qqqqqqq"

    connection = sq.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO users(username, password, score, token) VALUES (?,?,?,?);""",(username,password,0,token))
    connection.commit()
    connection.close()

    return {"token": token}

@app.post("/signup")
def postdata(username: str = Form(min_length=3, max_length=20),
             password: str =Form(min_length=3, max_length=20)):

    response = JSONResponse(content={"message": "куки установлены"})
    response.set_cookie(key="token", value=result)
    return response

@app.get("/click")
def users(id: int = Path(ge = 1)):
    return {"user_id": id}

@app.get("/leaderboard")
def users(id: int = Path(ge = 1)):
    return {"user_id": id}
