from flask import Blueprint,render_template,session,request
import sqlite3

import sqlite3.test

webSqlite = Blueprint("sqlite",__name__)

def universalTest():
  sesFile = session.get("sqlite_file")
  if sesFile:
    print("SQLite in session, connecting to " + sesFile)
    try:
      conTest = sqlite3.connect(sesFile)
      print("Connection OK.")
      session["sqlite_file"] = sesFile
      try:
        cur = conTest.cursor()
        cur.execute("select name,rootpage from sqlite_master where type='table' order by name")
        tables = cur.fetchall()
        cur.close()
        conTest.close()
        return {"status":True,"file":sesFile,"tables":tables,"tablesLen":len(tables)}
      except BaseException as e:
        cur.close()
        conTest.close()
        return {"status":False,"file":sesFile,"error":e}
    except:
      print("Bad connection.")
      session.pop("sqlite_file",None)
      return {"status":False}
  else:
    print("No SQLite in session")
    return {"status":False}

@webSqlite.route("/",methods=["GET","POST"])
def index():
  if request.form.get("sqlite_file"):
    session["sqlite_file"] = request.form.get("sqlite_file")
  dbTest = universalTest()
  return render_template("sqlite/index.html",globalDetails=dbTest)

  
@webSqlite.route("/runsql",methods=["GET","POST"])
def runsql():
  dbTest = universalTest()
  if dbTest["status"]:
    sql_command = request.form.get("sql_command")
    if sql_command:
      conn = sqlite3.connect(dbTest["file"])
      cur = conn.cursor()
      try:
        cur.execute(sql_command)
        tresults = cur.fetchall()
        conn.commit()
        tchanges = conn.total_changes
        cur.close()
        conn.close()
        dbTest = universalTest()
      except BaseException as e:
        return render_template("sqlite/runsql.html",status=1,msg=e,sql_command=sql_command,globalDetails=dbTest)
      else:
        return render_template("sqlite/runsql.html",status=0,sql_command=sql_command,tchanges=tchanges,tresults=tresults,globalDetails=dbTest)
    else:
      return render_template("sqlite/runsql.html",status=1,globalDetails=dbTest)
  else:
    return render_template("sqlite/runsql.html",status=1,globalDetails=dbTest)
  
@webSqlite.route("/table/<tableName>",methods=["GET","POST"])
def viewTable(tableName):
  dbTest = universalTest()
  if dbTest["status"]:
    selectedTable = tableName
    page = request.args.get("page",1)
    exePage = page - 1
    orderby = request.args.get("orderby",None)
    fetchlimit = request.args.get("fetchlimit",10)
    conn = sqlite3.connect(dbTest["file"])
    cur = conn.cursor()
    try:
      cur.execute("PRAGMA table_info(%s)" % (selectedTable))
      columns = cur.fetchall()
      baseExe = "SELECT * FROM %s" % (selectedTable)
      if orderby:
        baseExe = baseExe + " ORDER BY %s" % (orderby)
      baseExe = baseExe + " LIMIT %s,%s" % (exePage * fetchlimit,fetchlimit)
      print(baseExe)
      cur.execute(baseExe)
      rows = cur.fetchall()
      cur.close()
      conn.close()
      print(rows)
      return render_template("sqlite/viewtable.html",status=1,selectedTable=selectedTable,page=page,fetchlimit=fetchlimit,rows=rows,columns=columns,globalDetails=dbTest)
    except:
      return render_template("sqlite/viewtable.html",status=1,selectedTable=selectedTable,page=page,fetchlimit=fetchlimit,globalDetails=dbTest)
  else:
    return render_template("sqlite/viewtable.html",status=1,globalDetails=dbTest)