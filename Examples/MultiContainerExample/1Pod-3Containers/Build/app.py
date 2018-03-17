from flask import Flask, render_template
from flask import Response
from flask import request
from redis import Redis
from datetime import datetime
import MySQLdb
import sys
import redis 
import time
import hashlib
import os
import json
import random
import subprocess

app = Flask(__name__)
startTime = datetime.now()
R_SERVER = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis'), port=6379)
db = MySQLdb.connect("127.0.0.1","root","password")
cursor = db.cursor()

# list of cat images
images = [
    "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26388-1381844103-11.gif",
    "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr01/15/9/anigif_enhanced-buzz-31540-1381844535-8.gif",
    "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26390-1381844163-18.gif",
    "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr06/15/10/anigif_enhanced-buzz-1376-1381846217-0.gif",
    "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr03/15/9/anigif_enhanced-buzz-3391-1381844336-26.gif",
    "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr06/15/10/anigif_enhanced-buzz-29111-1381845968-0.gif",
    "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr03/15/9/anigif_enhanced-buzz-3409-1381844582-13.gif",
    "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr02/15/9/anigif_enhanced-buzz-19667-1381844937-10.gif",
    "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26358-1381845043-13.gif",
    "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr06/15/9/anigif_enhanced-buzz-18774-1381844645-6.gif",
    "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr06/15/9/anigif_enhanced-buzz-25158-1381844793-0.gif",
    "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr03/15/10/anigif_enhanced-buzz-11980-1381846269-1.gif"
]

@app.route('/')
def index():
    url = random.choice(images)
    sample_string = "mjindal";
    output=subprocess.check_output("cat /proc/self/cgroup | grep kubepods | sed s/\\\\//\\\\n/g | tail -1", shell=True);
    return render_template('index.html', url=url , str=output)

@app.route('/add')
def add():
    return render_template('add_user.html')


@app.route('/init')
def init():
    cursor.execute("DROP DATABASE IF EXISTS USERDB")
    cursor.execute("CREATE DATABASE USERDB")
    cursor.execute("USE USERDB")
    sql = """CREATE TABLE users (
         ID int,
         USER char(30)
     )"""
    cursor.execute(sql)
    db.commit()
    return "DB Init done" 

@app.route("/users/add", methods=['POST'])
def add_users():
    uid = request.form['uid']
    user = request.form['user']
    cursor.execute("INSERT INTO USERDB.users (ID, USER) VALUES (%s,%s)", (uid,user))
    db.commit()
    return Response("Added", status=200, mimetype='application/json')

@app.route('/users/<uid>')
def get_users(uid):
    hash = hashlib.sha224(str(uid)).hexdigest()
    key = "sql_cache:" + hash
    
    if (R_SERVER.get(key)):
        return R_SERVER.get(key) + "(c)" 
    else:
        cursor.execute("select USER from USERDB.users where ID=" + str(uid))
        data = cursor.fetchone()
        if data:
            R_SERVER.set(key,data[0])
            R_SERVER.expire(key, 36);
            return R_SERVER.get(key)
        else:
            return "Record not found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)