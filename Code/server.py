import sqlite3,os,re
from datetime import datetime, timedelta
from flask import *
app = Flask(__name__)
app.secret_key = "asdlkjqwepoirtyiuyzxc,mncvbnbv0912398735=-0`12"
abs = os.path.abspath(__file__)
uploadPath = abs[0:-9]+"uploads"
app.config['UPLOAD_FOLDER'] = uploadPath

@app.route('/')
def home():
  return redirect('/login')

@app.route('/login',methods=['GET'])
def login():
  return render_template("login.html")

@app.route('/logOut',methods=['GET'])
def logOut():
  session['user']=None
  session['role']=None
  return redirect('/login')

@app.route('/signUp',methods=['GET','POST'])
def signUp():
  return render_template("signUp.html")

@app.route('/addUser',methods=['POST'])
def addUser():
  username = request.form["userName"]
  password = request.form["password"]
  isAdmin = request.form.get("isAdmin")
  regex = r"^[a-zA-Z0-9]{8,}$"
  if(username=="" or password=="" or not re.match(regex,password)):
    return jsonify({"BAD_REQUEST":"Invalid credentials!"})
  if(isAdmin==None):
    isAdmin="0"
  print(username,password,isAdmin)
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("INSERT INTO user VALUES(?,?,?)",(username,password,int(isAdmin)))
      print("User added successfully !")
      return jsonify({"SUCCESS":"User created successfully!"})
  except Exception as e:
    print("Error while adding data in database",e)
  return jsonify({"ERROR":"User Already Exists"})

@app.route("/loginUser",methods=['POST'])
def loginUser():
  username = request.form.get("userName")
  password = request.form.get("password")
  if(username=="" or password==""):
    return jsonify({"BAD_REQUEST":"Invalid credentials!"})
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
        return redirect("/adminHome")
      elif(role==0):
        return redirect("/userHome")
  except Exception as e:
    print("User data not found in database",str(e))
  return redirect("/login")

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
        return render_template("sections.html",sections=sections)
    except Exception as e:
      print("User data not found in database",str(e))
  elif request.method == 'POST':
    currDate = datetime.now().date()
    print(currDate)
    try:
      with sqlite3.connect("library.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO section(name,creationDate,description) VALUES(?,?,?)",(request.form['sectionName'],currDate,request.form['description']))
        sections = cur.fetchall()
        print(sections)
        return redirect('/manageSections')
    except Exception as e:
      print("User data not found in database",str(e))
  elif request.method == 'DELETE':
    try:
      with sqlite3.connect("library.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM book WHERE sectionID = ?",(request.args.get('secID')))
        cur.execute("DELETE FROM section WHERE id = ?",(request.args.get('secID')))
    except Exception as e:
      print("Unable to delete data: ",str(e))
    return redirect('/manageSections')
  elif request.method == 'PUT':
    currDate = datetime.now().date()
    data = request.get_json()
    print("****************",data)
    try:
      with sqlite3.connect("library.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE section SET name=?, creationDate=?, description=? WHERE id=?",(data['name'],currDate,data['desc'],int(data['id'])))
        return redirect('/manageSections')
    except Exception as e:
      print("User data not found in database",str(e))

@app.route('/manageBooks',methods=['GET','POST','PUT','DELETE'])
def manageBooks():
  if request.method == 'GET':
    try:
      with sqlite3.connect("library.db") as con:
        cur = con.cursor()
        cur.execute("SELECT id,name,author,sectionID,avail FROM book")
        books = cur.fetchall()
        print(books)
        return render_template("books.html",books=books)
    except Exception as e:
      print("Internal Server Error",str(e))
  elif request.method == 'POST':
    edit = request.form.get('isEdit','0')
    file = request.files['book']
    if edit=='0':
      if file:
        try:
          save_path = os.path.join(app.config.get('UPLOAD_FOLDER'),file.filename)
          file.save(save_path)
          # with open(save_path, 'wb') as f:
          #   f.seek(0)
          #   print(file.read())
          #   f.write(file.read())
          with sqlite3.connect("library.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO book(name,content,author,sectionID,avail) VALUES(?,?,?,?,?)",(file.filename,file.read(),request.form['author'],request.form['secID'],request.form['noOfBooks']))
            return redirect('/manageBooks')
        except Exception as e:
          print("Internal Server Error:",str(e))
          return("ERROR")
    elif edit=='1':
      params = []
      query = "UPDATE book SET "
      if(request.form['author']!=''):
        query+='author = ?, '
        params.append(request.form['author'])
      if request.form['noOfBooks']!='':
        query+='avail = ?, '
        params.append(request.form['noOfBooks'])
      if(request.form['secID']!=''):
        query+='sectionID = ?, '
        params.append(request.form['secID'])
      if(file.filename!=''):
        query+='name = ?, content = ?, '
        params.append(file.filename)
        params.append(file.read())
      query = query.rstrip(', ')
      query+=" WHERE id = ?"
      params.append(request.form['bookID'])
      try:
        with sqlite3.connect("library.db") as con:
          cur = con.cursor()
          cur.execute(query,params)
          sections = cur.fetchall()
          print(sections)
          return redirect('/manageBooks')
      except Exception as e:
        print("User data not found in database",str(e))
  elif request.method == 'DELETE':
    try:
      with sqlite3.connect("library.db") as con:
        cur = con.cursor()
        cur.execute("SELECT name FROM book WHERE id = ?",(request.args.get('bookID')))
        filename = cur.fetchone()
        print(filename[0])
        cur.execute("DELETE FROM Book WHERE id = ?",(request.args.get('bookID')))
        delete_path = os.path.join(app.config.get('UPLOAD_FOLDER'),filename[0])
        os.remove(delete_path)
    except Exception as e:
      print("Unable to delete data: ",str(e))
    return redirect('/manageBooks')
  
@app.route('/searchBooks',methods=['GET','POST'])
def searchBooks():
  if(request.method == 'GET'):
    try:
      with sqlite3.connect("library.db") as con:
        cur = con.cursor()
        cur.execute("SELECT b.id,b.name,b.author,s.name FROM Book b, Section s WHERE s.id = b.sectionID")
        data = cur.fetchall()
        print(data)
      return render_template("searchBooks.html",books=data)
    except Exception as e:
      print("Internal Server Error: ",e)
  elif request.method == 'POST':
    try:
      with sqlite3.connect("library.db") as con:
        cur = con.cursor()
        book_search = '%' + request.form['bookSearch'] + '%'
        author_search = '%' + request.form['authorSearch'] + '%'
        cur.execute("SELECT b.id,b.name,b.author,s.name FROM Book as b JOIN Section as s ON s.id = b.sectionID WHERE b.name LIKE ? AND b.author LIKE ?",(book_search,author_search))
        data = cur.fetchall()
        print(data)
        return render_template("searchBooks.html",books=data)
    except Exception as e:
      print("Internal Server Error: ",e)

@app.route('/userHome',methods=["GET"])
def userHome():
  return render_template('userHome.html', name=session['user'])

@app.route("/userBooks",methods=["GET"])
def userBooks():
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("SELECT b.name,b.author,s.name,b.avail FROM Book as b JOIN Section as s ON s.id = b.sectionID")
      data = cur.fetchall()
      print(data)
  except Exception as e:
    print("Internal Server Error: ",e)
  return render_template("userBooks.html",books=data)

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
        return jsonify({"msg":"Already have 5 books, cannot borrow more!"})
      else:
        cur.execute("SELECT bw.uname FROM borrowed as bw JOIN book as b ON bw.bookid = b.id WHERE bw.uname = ? AND b.name = ?",(uname,bookname))
        data = cur.fetchall()
        print(data)
        if(len(data)>0):
          return jsonify({"msg":"already requested"})
        cur.execute("SELECT id FROM book WHERE name = ?",(bookname,))
        bookID = cur.fetchone()[0]
        print(bookID)
        cur.execute("INSERT INTO borrowed VALUES (?,?,0,?,?)",(uname,bookID,None,None))
  except Exception as e:
    print("Internal Server Error: ",e)
  return jsonify({"msg":"Request submitted"})

@app.route('/manageIssueRevoke',methods=["GET"])
def manageIssueRevoke():
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("SELECT bw.bookid, bw.uname, b.name, b.author, b.avail, bw.issueDate, bw.returnDate, bw.status FROM borrowed bw JOIN book b ON bw.bookid = b.id ORDER BY bw.status")
      data = cur.fetchall()
      return render_template('manageIssueRevoke.html',books = data)
  except Exception as e:
    print("Internal Server Error: ",e)

@app.route('/issueBook',methods=["POST"])
def issueBook():
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      currDate = datetime.now().date()
      revokeDate = currDate + timedelta(days=7)
      cur.execute("UPDATE borrowed SET issueDate = ?, returnDate = ?, status = 1 WHERE uname = ? AND bookid = ?",(currDate,revokeDate,request.json.get('user'),request.json.get('bookid')))
      cur.execute("UPDATE book SET avail = avail - 1 WHERE id = ?",(request.json.get('bookid'),))
      return redirect('/manageIssueRevoke')
  except Exception as e:
    print("Internal Server Error: ",e)

@app.route('/revokeBook',methods=["POST"])
def revokeBook():
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("DELETE FROM borrowed WHERE bookid = ? AND uname = ?",(request.json.get('bookid'),request.json.get('user')))
      cur.execute("UPDATE book SET avail = avail + 1 WHERE id = ?",(request.json.get('bookid'),))
      return redirect('/manageIssueRevoke')
  except Exception as e:
    print("Internal Server Error: ",e)

@app.route('/readBooks',methods=["GET"])
def readBooks():
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      cur.execute("SELECT b.name, b.author, s.name FROM book b JOIN section s ON b.sectionID = s.id WHERE b.id IN (SELECT bookid FROM borrowed WHERE uname = ? AND status = 1)",(session.get('user'),))
      data = cur.fetchall()
      return render_template('readBooks.html', books = data)
  except Exception as e:
    print("Internal Server Error: ",e)
  return "Error"

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

if __name__ == '__main__':
  try:
    with sqlite3.connect("library.db") as con:
      cur = con.cursor()
      # role 1-User 2-Admin
      cur.execute("CREATE TABLE IF NOT EXISTS User(uname varchar(50), password varchar(255), role integer, primary key(uname,password))")
      cur.execute("CREATE TABLE IF NOT EXISTS Section(id integer primary key autoincrement, name varchar(255), creationDate date, description varchar(255))")
      cur.execute("CREATE TABLE IF NOT EXISTS Book(id integer primary key autoincrement , name varchar(255), content blob, author varchar(255), avail integer, sectionID integer, foreign key (sectionID) references Section(id))")
      cur.execute("CREATE TABLE IF NOT EXISTS Borrowed(uname varchar(255), bookid integer, status integer, issueDate date, returnDate date, foreign key (bookid) references Book(id), foreign key (uname) references User(uname) )")
      cur.execute("")
      print("Tables created successfully !")
  except Exception as e:
    print("Error in table creation or connecting to server: ",e)
  app.run(debug=True)