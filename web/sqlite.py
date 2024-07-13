from flask import Blueprint,render_template,session,request
import sqlite3

import sqlite3.test

webSqlite = Blueprint("sqlite",__name__)

@webSqlite.route("/",methods=["GET","POST"])
def index():
  if request.form.get("sqlite_file"):
    session["sqlite_file"] = request.form.get("sqlite_file")
  sesFile = session.get("sqlite_file")
  if sesFile:
    print("SQLite in session, connecting to " + sesFile)
    conTest = sqlite3.connect(sesFile)
    if conTest:
      print("Connection OK.")
      session["sqlite_file"] = sesFile
      cur = conTest.cursor()
      cur.execute("select name from sqlite_master where type='table' order by name")
      tables = cur.fetchall()
      print("Tables:")
      print(tables)
      return render_template("sqlite/index.html",status=0,working=sesFile,tables=tables,tablesLen=len(tables))
    else:
      print("Bad connection.")
      session.pop("sqlite_file",None)
      return render_template("sqlite/index.html",status=2)
  else:
    print("No SQLite in session")
    return render_template("sqlite/index.html",status=1)
  
