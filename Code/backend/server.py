import sqlite3,os,re
from datetime import datetime, timedelta
from flask import *
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.secret_key = "asdlkjqwepoirtyiuyzxc,mncvbnbv0912398735=-0`12"
abs = os.path.abspath(__file__)
uploadPath = abs[0:-9]+"uploads"
app.config['UPLOAD_FOLDER'] = uploadPath

@app.route('/addUser',methods=['POST'])
def addUser():
  data = request.json
  username = data.get("userName")
  password = data.get("password")
  isAdmin = int(data.get("isAdmin"))
  regex = r"^[a-zA-Z0-9]{8,}$"
  if(username=="" or password=="" or not re.match(regex,password)):
    return jsonify({"BAD_REQUEST":"Invalid credentials!"}), 400
  if(isAdmin==None):
    isAdmin="0"
  print(username,password,isAdmin)
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("SELECT * FROM user WHERE uname = ? AND password = ?",(username, password))
      user = cur.fetchall()
      print("#####",user)
      if(user==None or user==""):
        cur.execute("INSERT INTO user VALUES(?,?,?)",(username,password,int(isAdmin)))
        print("User added successfully !")
        return jsonify({"SUCCESS":"User created successfully!"}), 200
      else:
        return jsonify({"ERROR":"User Already Exists"}), 400
  except Exception as e:
    print("Error while adding data in database",e)
  return jsonify({"ERROR":"User Already Exists"}), 400

@app.route("/loginUser",methods=['POST'])
def loginUser():
  data = request.json
  username = data.get("userName")
  password = data.get("password")
  if(username=="" or password==""):
    return jsonify({"BAD_REQUEST":"Invalid credentials!"}), 400
  print(username,password)
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("SELECT * FROM user WHERE uname = ? AND password = ?",(username,password))
      role = cur.fetchall()[0][-1]
      print("User found successfully !")
      session['user'] = username
      session['role'] = role
      if(role == 1):
        return jsonify({"MSG":"Successful Login", "Name":username, "Role": role})
      elif(role==0):
        return jsonify({"MSG":"Successful Login", "Name":username, "Role": role})
  except Exception as e:
    print("User data not found in database",str(e))
    return jsonify({"ERROR":"User data not found in database"}), 400
  return jsonify({"ERROR":"Login Failed!"})

@app.route("/adminHome",methods=['GET'])
def adminHome():
  if(session.get('role') == None):
    return render_template("unAuth.html")
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("SELECT uname,role from User")
      userData = cur.fetchall()
  except Exception as e:
    print("Internal Server Error: ",e)
  return render_template("adminHome.html",name=session.get('user'),userData=userData)

@app.route('/manageSections',methods=['GET','POST','PUT','DELETE'])
def manageSections():
  if request.method == 'GET':
    try:
      with sqlite3.connect("library.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM section")
        sections = cur.fetchall()
        print(sections)
        return jsonify({"sections":sections}), 200
    except Exception as e:
      print("User data not found in database",str(e))
      return jsonify({"Error":"Internal Server Error"}), 500
  elif request.method == 'POST':
    currDate = datetime.now().date()
    print(currDate)
    data = request.json
    section_name = data.get('name')
    description = data.get('description')
    try:
      with sqlite3.connect("library.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO section(name,creationDate,description) VALUES(?,?,?)",(section_name,currDate,description))
        sections = cur.fetchall()
        print(sections)
        return jsonify({"SUCCESS ":"Section added successfully"}), 200
    except Exception as e:
      print("User data not found in database",str(e))
      return jsonify({"Error":"Internal Server Error"}), 500
  elif request.method == 'DELETE':
    try:
      secID = request.args.get('secID')
      if secID == None:
        return jsonify({"ERR":"SectionID is not found!"})
      else:
        secID = int(secID)
      with sqlite3.connect("library.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM book WHERE sectionID = ?",(secID,))
        cur.execute("DELETE FROM section WHERE id = ?",(secID,))
        return jsonify({"SUCCESS":"Successfully deleted the entry!"}),200
    except Exception as e:
      print("Unable to delete data: ",str(e))
      return jsonify({"Error":"Internal Server Error"}), 500
  elif request.method == 'PUT':
    currDate = datetime.now().date()
    data = request.json
    section_id = data.get('id')
    section_name = data.get('name')
    description = data.get('description')
    try:
      with sqlite3.connect("library.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE section SET name=?, creationDate=?, description=? WHERE id=?",(section_name,currDate,description,int(section_id)))
        return jsonify({"SUCCESS":"Updated section successfully!"}), 200
    except Exception as e:
      return jsonify({"Error":"Internal Server Error"}), 500

@app.route('/manageBooks',methods=['GET','POST','PUT','DELETE'])
def manageBooks():
  if request.method == 'GET':
    try:
        with sqlite3.connect("library.db") as con:
            cur = con.cursor()
            cur.execute("SELECT id, name, author, sectionID, avail FROM book")
            books = cur.fetchall()
            formatted_books = [{"id": book[0], "name": book[1], "author": book[2], "sectionID": book[3], "avail": book[4]} for book in books]
            return jsonify({"books": formatted_books}), 200
    except Exception as e:
        print("Internal Server Error:", str(e))
        return jsonify({"Error": "Internal Server Error"}), 500

  elif request.method == 'POST':
    edit = request.form.get('isEdit', '0')
    file = request.files.get('book', None)
    print(edit)
    if edit == '0':
        if file:
            try:
                with sqlite3.connect("library.db") as con:
                    cur = con.cursor()
                    cur.execute(
                        "SELECT * FROM Section WHERE id = ?",
                        (request.form.get('secID'))
                    )
                    sec = cur.fetchall()
                    if(not sec or len(sec)):
                      return jsonify({"ERR":"Section ID doesn't exist!"}), 400
                filename = file.filename
                file_content = file.read()
                save_path = os.path.join(app.config.get('UPLOAD_FOLDER'), filename)
                
                with open(save_path, 'wb') as f:
                    f.write(file_content)
                
                with sqlite3.connect("library.db") as con:
                    cur = con.cursor()
                    cur.execute(
                        "INSERT INTO book(name, content, author, sectionID, avail) VALUES(?,?,?,?,?)",
                        (filename, file_content, request.form.get('author'), request.form.get('secID'), request.form.get('noOfBooks'))
                    )
                return jsonify({"SUCCESS": "Book added successfully"}), 200
            except Exception as e:
                print("Internal Server Error:", str(e))
                return jsonify({"Error": "Internal Server Error"}), 500
        else:
          return jsonify({"ERR":"No file present"}), 400
    elif edit == '1':
        params = []
        query = "UPDATE book SET "
        if request.form.get('author'):
            query += 'author = ?, '
            params.append(request.form.get('author'))
        if request.form.get('noOfBooks'):
            query += 'avail = ?, '
            params.append(request.form.get('noOfBooks'))
        if request.form.get('secID'):
            query += 'sectionID = ?, '
            params.append(request.form.get('secID'))
        if file and file.filename:
                query += 'name = ?, content = ?, '
                params.append(file.filename)
                file_content = file.read()
                params.append(file_content)
        query = query.rstrip(', ')
        query += " WHERE id = ?"
        params.append(request.form.get('bookID'))

        try:
            with sqlite3.connect("library.db") as con:
                cur = con.cursor()
                cur.execute(query, params)
            return jsonify({"SUCCESS": "Book updated successfully"}), 200
        except Exception as e:
            print("Internal Server Error:", str(e))
            return jsonify({"Error": "Internal Server Error"}), 500

  elif request.method == 'DELETE':
    bookID = request.args.get('bookID')
    if not bookID:
        return jsonify({"Error": "BookID is required"}), 400
    
    try:
        with sqlite3.connect("library.db") as con:
            cur = con.cursor()
            cur.execute("SELECT name FROM book WHERE id = ?", (bookID,))
            filename = cur.fetchone()
            if filename:
                filename = filename[0]
                cur.execute("DELETE FROM book WHERE id = ?", (bookID,))
                delete_path = os.path.join(app.config.get('UPLOAD_FOLDER'), filename)
                if os.path.exists(delete_path):
                    os.remove(delete_path)
            else:
                return jsonify({"Error": "Book not found"}), 404
        return jsonify({"SUCCESS": "Book deleted successfully"}), 200
    except Exception as e:
        print("Unable to delete data:", str(e))
        return jsonify({"Error": "Internal Server Error"}), 500
  
@app.route('/searchBooks',methods=['POST'])
def searchBooks():
  data = request.json
  print(data)
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      book_search = '%' + data['bookSearch'] + '%'
      author_search = '%' + data['authorSearch'] + '%'
      cur.execute("SELECT b.id,b.name,b.author,s.name FROM Book as b JOIN Section as s ON s.id = b.sectionID WHERE b.name LIKE ? AND b.author LIKE ?",(book_search,author_search))
      data = cur.fetchall()
      print(data)
      return jsonify({"books":data}), 200
  except Exception as e:
    return jsonify({"Error": "Internal Server Error"}), 500

@app.route("/userBooks",methods=["GET"])
def userBooks():
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("SELECT b.name,b.author,s.name,b.avail FROM Book as b JOIN Section as s ON s.id = b.sectionID")
      data = cur.fetchall()
      print(data)
      return jsonify({"Books":data}), 200
  except Exception as e:
    print("Internal Server Error: ",e)
    return jsonify({"Error": "Internal Server Error"}), 500

@app.route('/requestBooks',methods=['POST'])
def requestBooks():
  uname = session.get('user')
  bookname = request.json.get('book')
  print(uname,bookname)
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("SELECT uname FROM borrowed WHERE uname = ?",(uname,))
      borrowedNo = len(cur.fetchall())
      print(borrowedNo)
      if(borrowedNo==5):
        return jsonify({"msg":"Already have 5 books, cannot borrow more!"}), 200
      else:
        cur.execute("SELECT bw.uname FROM borrowed as bw JOIN book as b ON bw.bookid = b.id WHERE bw.uname = ? AND b.name = ?",(uname,bookname))
        data = cur.fetchall()
        print(data)
        if(len(data)>0):
          return jsonify({"msg":"already requested"}), 200
        cur.execute("SELECT id FROM book WHERE name = ?",(bookname,))
        bookID = cur.fetchone()[0]
        print(bookID)
        cur.execute("INSERT INTO borrowed VALUES (?,?,0,?,?)",(uname,bookID,None,None))
        return jsonify({"msg":"Request submitted"}), 200
  except Exception as e:
    print("Internal Server Error: ",e)
    return jsonify({"ERR":"Internal Server Error"}), 5500

@app.route('/manageIssueRevoke',methods=["GET"])
def manageIssueRevoke():
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("SELECT bw.bookid, bw.uname, b.name, b.author, b.avail, bw.issueDate, bw.returnDate, bw.status FROM borrowed bw JOIN book b ON bw.bookid = b.id ORDER BY bw.status")
      data = cur.fetchall()
      print(data)
      return jsonify({"Books":data}), 200
  except Exception as e:
    print("Internal Server Error: ",e)
    return jsonify({"ERR":"Internal Server Error"}), 500
  
@app.route('/issueBook',methods=["POST"])
def issueBook():
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      currDate = datetime.now().date()
      revokeDate = currDate + timedelta(days=7)
      cur.execute("UPDATE borrowed SET issueDate = ?, returnDate = ?, status = 1 WHERE uname = ? AND bookid = ?",(currDate,revokeDate,request.json.get('user'),request.json.get('bookid')))
      cur.execute("UPDATE book SET avail = avail - 1 WHERE id = ?",(request.json.get('bookid'),))
      return jsonify({"MSG":"Book issued successfully"}), 200
  except Exception as e:
    print("Internal Server Error: ",e)
    return jsonify({"ERR":"Internal Server Error"}), 500

@app.route('/revokeBook',methods=["POST"])
def revokeBook():
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("DELETE FROM borrowed WHERE bookid = ? AND uname = ?",(request.json.get('bookid'),request.json.get('user')))
      cur.execute("UPDATE book SET avail = avail + 1 WHERE id = ?",(request.json.get('bookid'),))
      return jsonify({"MSG":"Book revoked successfully"}), 200
  except Exception as e:
    print("Internal Server Error: ",e)
    return jsonify({"ERR":"Internal Server Error"}), 500

@app.route('/readBooks',methods=["GET"])
def readBooks():
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("SELECT b.name, b.author, s.name FROM book b JOIN section s ON b.sectionID = s.id WHERE b.id IN (SELECT bookid FROM borrowed WHERE uname = ? AND status = 1)",(session.get('user'),))
      data = cur.fetchall()
      return jsonify({"books":data}), 200
  except Exception as e:
    print("Internal Server Error: ",e)
    return jsonify({"Error":"Internal Server Error"}), 500

@app.route('/view-file')
def view_file():
    filename = request.args.get('filename')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=False)


@app.route('/readSection',methods=["GET"])
def readSection():
  return render_template("readSection.html",filename = request.args.get('book'))

@app.route('/returnBook',methods=["POST"])
def returnBook():
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("DELETE FROM borrowed WHERE bookid = (SELECT id FROM book WHERE name = ?) AND uname = ?",(request.json.get('book'),session.get('user')))
      cur.execute("UPDATE book SET avail = avail + 1 WHERE name = ?",(request.json.get('book'),))
      return redirect('/readBooks')
  except Exception as e:
    print("Internal Server Error: ",e)

@app.route('/getAllUserDetails', methods=["GET"])
def getAllUserDetails():
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("SELECT uname, role FROM User")
      data = cur.fetchall()
      print(data)
      return jsonify({"User Data":data}), 200
  except Exception as e:
    print("Internal Server Error: ",e)
    return jsonify({"Error":"Internal Server Error"}), 500

if __name__ == '__main__':
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      # role 1-User 2-Admin
      con.execute("PRAGMA foreign_keys = ON")
      cur.execute("CREATE TABLE IF NOT EXISTS User(uname varchar(50), password varchar(255), role integer, primary key(uname,password))")
      cur.execute("CREATE TABLE IF NOT EXISTS Section(id integer primary key autoincrement, name varchar(255), creationDate date, description varchar(255))")
      cur.execute("CREATE TABLE IF NOT EXISTS Book(id integer primary key autoincrement , name varchar(255), content blob, author varchar(255), avail integer, sectionID integer, foreign key (sectionID) references Section(id))")
      cur.execute("CREATE TABLE IF NOT EXISTS Borrowed(uname varchar(255), bookid integer, status integer, issueDate date, returnDate date, foreign key (bookid) references Book(id), foreign key (uname) references User(uname) )")
      cur.execute("")
      print("Tables created successfully !")
  except Exception as e:
    print("Error in table creation or connecting to server: ",e)
  app.run(debug=True)