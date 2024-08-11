import sqlite3,os,re
from datetime import datetime, timedelta
from flask import *
from flask_cors import CORS
from flask_caching import Cache
app = Flask(__name__)
CORS(app)
app.secret_key = "asdlkjqwepoirtyiuyzxc,mncvbnbv0912398735=-0`12"
abs = os.path.abspath(__file__)
uploadPath = abs[0:-9]+"uploads"
app.config['UPLOAD_FOLDER'] = uploadPath
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

@app.route('/logOut',methods=['GET'])
def logOut():
  session['user']=None
  session['role']=None
  return jsonify({"SUCCESS":"Logout successful!"}), 200

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
      if(user==None or len(user)==0):
        cur.execute("INSERT INTO user VALUES(?,?,?)",(username,password,int(isAdmin)))
        print("User added successfully !")
        cache.clear()
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
      data = cur.fetchall()
      print(data)
      role = data[0][-1]
      print("User found successfully !")
      session['user'] = username
      session['role'] = role
      cache.clear()
      if(role == 1):
        return jsonify({"MSG":"Successful Login", "Name":username, "Role": role})
      elif(role==0):
        return jsonify({"MSG":"Successful Login", "Name":username, "Role": role})
  except Exception as e:
    print("User data not found in database",str(e))
    return jsonify({"ERROR":"User data not found in database"}), 400

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
@cache.cached(timeout=60, query_string=True)
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
        cache.clear()
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
        cache.clear()
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
        cache.clear()
        return jsonify({"SUCCESS":"Updated section successfully!"}), 200
    except Exception as e:
      return jsonify({"Error":"Internal Server Error"}), 500

@app.route('/manageBooks',methods=['GET','POST','PUT','DELETE'])
@cache.cached(timeout=60, query_string=True)
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
    print(request.form)
    if edit == '0':
        if file:
            try:
                print(request.form.get('secID'))
                with sqlite3.connect("library.db") as con:
                    cur = con.cursor()
                    cur.execute(
                        "SELECT * FROM Section WHERE id = ?",(request.form.get('secID'),)
                    )
                    sec = cur.fetchall()
                    print(sec)
                    if(not sec or len(sec)==0):
                      return jsonify({"ERROR":"Section ID doesn't exist!"}), 400
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
                    cache.clear()
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
                cache.clear()
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
                cache.clear()
            else:
                return jsonify({"Error": "Book not found"}), 404
        return jsonify({"SUCCESS": "Book deleted successfully"}), 200
    except Exception as e:
        print("Unable to delete data:", str(e))
        return jsonify({"Error": "Internal Server Error"}), 500
  
@app.route('/searchBooks',methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def searchBooks():
  data = request.args
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
@cache.cached(timeout=60)
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
  uname = request.json.get('user')
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
          cache.clear()
          return jsonify({"msg":"already requested"}), 200
        cur.execute("SELECT id FROM book WHERE name = ?",(bookname,))
        bookID = cur.fetchone()[0]
        print(bookID)
        cur.execute("INSERT INTO borrowed VALUES (?,?,0,?,?)",(uname,bookID,None,None))
        cache.clear()
        return jsonify({"msg":"Request submitted"}), 200
  except Exception as e:
    print("Internal Server Error: ",e)
    return jsonify({"ERR":"Internal Server Error"}), 5500

@app.route('/manageIssueRevoke',methods=["GET"])
@cache.cached(timeout=120)
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
      print(request.json)
      currDate = datetime.now().date()
      revokeDate = currDate + timedelta(days=7)
      cur.execute("UPDATE borrowed SET issueDate = ?, returnDate = ?, status = 1 WHERE uname = ? AND bookid = ?",(currDate,revokeDate,request.json.get('user'),request.json.get('bookid')))
      cur.execute("UPDATE book SET avail = avail - 1 WHERE id = ?",(request.json.get('bookid'),))
      cache.clear()
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
      cache.clear()
      return jsonify({"MSG":"Book revoked successfully"}), 200
  except Exception as e:
    print("Internal Server Error: ",e)
    return jsonify({"ERR":"Internal Server Error"}), 500

@app.route('/readBooks',methods=["GET"])
@cache.cached(timeout=120)
def readBooks():
  try:
    user = request.args.get('user')
    if not user:
        return jsonify({"Error": "User not provided"}), 400
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("SELECT b.name, b.author, s.name FROM book b JOIN section s ON b.sectionID = s.id WHERE b.id IN (SELECT bookid FROM borrowed WHERE uname = ? AND status = 1)",(user,))
      data = cur.fetchall()
      print(data)
      return jsonify({"books":data}), 200
  except Exception as e:
    print("Internal Server Error: ",e)
    return jsonify({"Error":"Internal Server Error"}), 500

@app.route('/view-file')
def view_file():
    filename = request.args.get('filename')
    print(filename)
    if not filename:
      return jsonify({"ERROR":'Filename is required'}), 400
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
      return jsonify({"ERROR":'file path not found!'}), 400
    response = send_file(filepath, mimetype='application/pdf')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/readSection',methods=["GET"])
def readSection():
  return render_template("readSection.html",filename = request.args.get('book'))

@app.route('/returnBook',methods=["POST"])
def returnBook():
  try:
    print(request.json)
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("DELETE FROM borrowed WHERE bookid = (SELECT id FROM book WHERE name = ?) AND uname = ?",(request.json.get('book'), request.json.get('user')))
      cur.execute("UPDATE book SET avail = avail + 1 WHERE name = ?",(request.json.get('book'),))
      cache.clear()
      return jsonify({"MSG":"Successfully returned the book!"}), 200
  except Exception as e:
    print("Internal Server Error: ",e)
    return jsonify({"Error":"Internal Server Error"}), 500

@app.route('/getAllUserDetails', methods=["GET"])
@cache.cached(timeout=300)
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