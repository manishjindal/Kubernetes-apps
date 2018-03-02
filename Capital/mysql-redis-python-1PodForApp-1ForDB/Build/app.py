from flask import Flask, render_template
from flask import Response
from flask import request
from datetime import datetime
import MySQLdb
import sys
import time
import hashlib
import os
import json
import random
import subprocess

app = Flask(__name__)
startTime = datetime.now()
db = MySQLdb.connect("mysql","root","password")
cursor = db.cursor()

@app.route('/')
def index():
    output=subprocess.check_output("cat /proc/self/cgroup | grep kubepods | sed s/\\\\//\\\\n/g | tail -1", shell=True);
    return render_template('index.html', str=output)

@app.route('/add')
def add():
    return render_template('add_user.html')


@app.route('/init')
def init():
    cursor.execute("DROP DATABASE IF EXISTS USERDB")
    cursor.execute("CREATE DATABASE USERDB")
    cursor.execute("USE USERDB")
    sql = """CREATE TABLE users (
         ID int NOT NULL AUTO_INCREMENT,
         USER char(30),
         CONTACT varchar(30),
         GAME_TYPE varchar(30),
         PRIMARY KEY ( ID )
     )"""
    cursor.execute(sql)
    db.commit()
    return "DB Init done" 

@app.route("/users/add", methods=['POST'])
def add_users():
    user = request.form['user']
    contact = request.form['contact']
    game_type = request.form['game_type']
    cursor.execute("INSERT INTO USERDB.users (USER,CONTACT,GAME_TYPE) VALUES (%s,%s,%s)", (user,contact,game_type))
    db.commit()
    return get_all_users()

@app.route('/users/<uid>')
def get_users(uid):
    cursor.execute("select * from USERDB.users where ID=" + str(uid))
    data = cursor.fetchone()
    if data:
        return render_template('users.html',id=data[0], name=data[1], contact=data[2], game_type=data[3])
    else:
        return "User doesn't exist for given ID!"

@app.route('/users/edit/<uid>')
def edit_users(uid):
    cursor.execute("select * from USERDB.users where ID=" + str(uid))
    data = cursor.fetchone()
    if data:
        return render_template('edit_user.html',id=data[0], name=data[1], contact=data[2], game_type=data[3])
    else:
        return "Record not found!"

@app.route("/users/update/<uid>", methods=['POST'])
def update_users(uid):
    user = request.form['user']
    contact = request.form['contact']
    game_type = request.form['game_type']
    cursor.execute("UPDATE USERDB.users SET USER='"+str(user)+"',CONTACT='"+str(contact)+"',GAME_TYPE='"+str(game_type)+"' WHERE ID="+str(uid))
    db.commit()
    return get_all_users()

@app.route("/users/delete/<uid>")
def delete_users(uid):
    cursor.execute("DELETE FROM USERDB.users WHERE ID="+str(uid))
    db.commit()
    return get_all_users()

@app.route('/users/all')
def get_all_users():
    cursor.execute("select * from USERDB.users")
    data = cursor.fetchall()
    if data:
        return render_template('all_users.html', data=data)
    else:
        return "No Records in the database!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)