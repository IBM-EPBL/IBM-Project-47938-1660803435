from flask import Flask,render_template,request,session, redirect,url_for
import ibm_db


app = Flask(__name__)
app.secret_key='vy@ur434'
#def connection():
# try:
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PROTOCOLO=TCPIP;PORT=30756;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=pbp31273;PWD=0mhmHAwaShMBEWZw","","")
print(conn)
print("connection successful...")
 # return conn
 #except:
  #print("Not Connected to Database")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/forgot')
def forgot():
    return render_template('forgotten-password.html')

@app.route('/discover')
def discover():
    stmt=ibm_db.exec_immediate(conn, "SELECT * FROM JOBS") 
    lt = []
    while ibm_db.fetch_row(stmt) != False:
        lt.append({"NAME":ibm_db.result(stmt, 0),"LOCATION":ibm_db.result(stmt, 1),"TYPE":ibm_db.result(stmt, 2),"SALARY":ibm_db.result(stmt, 3),"DEADLINE":ibm_db.result(stmt, 4)})   
    
    return render_template('discover.html', res=lt)

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        try:
            sql = "INSERT INTO USERS1 VALUES('{}','{}','{}','{}')".format(request.form["name"],request.form["phone"],request.form["email"],request.form["password"])
            print(sql)
            ibm_db.exec_immediate(conn,sql)
            print('ss')
            return render_template('login.html')
        except:
            return render_template('signup.html')
    else:
            return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        sql = "SELECT COUNT(*) FROM USERS1 WHERE EMAIL=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        res = ibm_db.fetch_assoc(stmt)
        if res['1'] == 1:
            session['loggedin'] = True
            session['email'] = email
            return render_template('userpage.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__=='__main__':
    app.config['SESSION_TYPE']= 'filesystem'
    app.run(debug=True)

       