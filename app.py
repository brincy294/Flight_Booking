from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('C:/Users/brima/Desktop/flights/templates'))
template = env.get_template('reserve.html')
template1 = env.get_template('booking_info.html')
template2 = env.get_template('passengers_table.html')


app = Flask(__name__)
  
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Godislove@2020*'
app.config['MYSQL_DB'] = 'dbms'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE u_eid = % s AND u_password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['u_id']
            session['name'] = user['u_name']  
            session['email'] = user['u_eid']
            mesage = 'Logged in successfully !'
            return render_template('dashboard_test.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login_test.html', mesage = mesage)

@app.route('/')
@app.route('/admin', methods =['GET', 'POST'])
def admin():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE a_eid = % s AND a_password = % s', (email, password, ))
        admin = cursor.fetchone()
        if admin:
            session['loggedin'] = True
            session['name'] = admin['a_name']
            session['email'] = admin['a_eid']
            mesage = 'Logged in as admin successfully !'
            return render_template('admin_options.html', mesage = mesage)
        else:
            mesage = 'AUTHORIZATION ONLY FOR ADMINS!'
    return render_template('login_test.html', mesage = mesage)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE u_eid = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL,% s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register_test.html', mesage = mesage)

@app.route('/find')
def find():
    return render_template('search.html')

@app.route('/show',methods =['GET', 'POST'])
def show():
    return render_template('passengers.html')

@app.route('/front',methods =['GET', 'POST'])
def front():
    return render_template('login_test.html')

@app.route('/searchpass', methods =['GET', 'POST'])
def searchpass():
    print("bhagbsdkkely")
    # if request.method == 'POST':
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #data = []
    flight_id=request.form['flight_id']
    col_names=("Passenger_id","User_Name","Age")
    data=[]
    cursor.execute('SELECT p_id,u_name,age FROM user,passenger WHERE passenger.flight_id=%s AND user.u_id=passenger.users_id', (flight_id,))
    res1=cursor.fetchall()
    for r in res1:
        # print(r)
        data.append(r)
            
        for j in r:

            print(r[j])
    data=res1
    # print(data)
        # flight = cursor.fetchone()
    return template2.render(col_names=col_names, data = data)

@app.route('/dashboard_test', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('find'))

@app.route('/result', methods =['GET', 'POST'])
def result():
    # print("bhagbsdk")
    if request.method == 'POST':
        arrival = request.form['pick']
        final = request.form['drop']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #data = []
        headings=("f_id","a_name","f_adest","f_fdest","f_adatetime","f_fdatetime","f_cost")
        data=[]
        print(arrival)
        print(final)
        cursor.execute('SELECT * FROM flight WHERE f_adest = %s AND f_fdest = % s', (arrival, final))
        res=cursor.fetchall()
        p=[]

        data=res
        flight = cursor.fetchone()
        return template.render(headings=headings, data = data)

@app.route("/reservation",methods= ['GET','POST'])
def reservation():
    mesage=''
    if request.method == 'POST':
        adate = request.form['d1']
        fdate = request.form['d2']
        flight_id = request.form['flight_id']
        age=request.form['age']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO reservation VALUES (NULL,% s, % s, % s,% s)', (session['userid'], flight_id, adate,fdate,))
        cursor.execute ('INSERT INTO passenger VALUES(NULL,%s,%s,%s)',(session['userid'],flight_id,age, ))
        mysql.connection.commit()
        mesage = 'Flight reserved!'
        return render_template('dashboard_test.html',mesage=mesage)
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('reserve.html', mesage = mesage)

@app.route("/add",methods =['GET', 'POST'])
def add():
    return render_template('add_flight.html')

@app.route("/dash",methods =['GET', 'POST'])
def dash():
    return render_template('dashboard_test.html')

@app.route('/addflight', methods =['GET', 'POST'])
def addflight():
    mesage = ''
    if request.method == 'POST' and 'f_id' in request.form and 'a_name' in request.form and 'f_adest' in request.form and 'f_fdest' in request.form and 'f_atime' in request.form and 'f_ftime' in request.form and 'f_cost' in request.form:
        flight_id = request.form['f_id']
        airline_name = request.form['a_name']
        adest = request.form['f_adest']
        fdest=request.form['f_fdest']
        atime=request.form['f_atime']
        ftime=request.form['f_ftime']
        cost=request.form['f_cost']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM flight WHERE f_id = % s' , (flight_id, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not flight_id or not airline_name or not adest or not fdest or not atime or  not ftime :
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO flight VALUES (%s,%s,%s,% s, % s, % s,%s)', (flight_id, airline_name, adest, fdest, atime,ftime,cost, ))
            mysql.connection.commit()
            mesage = 'You have successfully added !'
            return render_template('admin_options.html', mesage = mesage)

    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
        return render_template('add_flight.html', mesage = mesage)

@app.route("/delete",methods =['GET', 'POST'])
def delete():
    return render_template('delete_flight.html')

@app.route("/fronts",methods =['GET', 'POST'])
def fronts():
    return render_template('admin_options.html')

@app.route('/deleteflight', methods =['GET', 'POST'])
def deleteflight():
    mesage = ''
    if request.method == 'POST' and 'f_id' in request.form:
        flight_id = request.form['f_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM flight WHERE f_id = % s' , (flight_id, ))
        account = cursor.fetchone()
        if account:
            cursor.execute('DELETE FROM flight WHERE f_id = % s' , (flight_id, ))
            mysql.connection.commit()
            mesage = 'You have successfully deleted !' 
            return render_template('admin_options.html', mesage = mesage)

        elif not flight_id :
            mesage = 'Please enter valid flight number!'
            return render_template('delight_flight.html', mesage = mesage)
        else:
            return render_template('admin_options.html', mesage = mesage)

    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
        return render_template('delete_flight.html', mesage = mesage)

@app.route('/booking_info', methods =['GET', 'POST'])
def booking_info():
    print("bhagbsdkkely")
    # if request.method == 'POST':
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #data = []
    col_names=("r_id","f_id","a_name","f_adest","f_fdest","f_adatetime","f_fdatetime","f_cost")
    data=[]
    cursor.execute('SELECT r_id,f_id,a_name,f_adest,f_fdest,f_atime,f_ftime,f_cost FROM flight,reservation WHERE reservation.user_id=%s AND flight.f_id=reservation.flight_id', (session['userid'],))
    res1=cursor.fetchall()
    for r in res1:
        # print(r)
        data.append(r)
            
        for j in r:

            print(r[j])
    data=res1
    # print(data)
        # flight = cursor.fetchone()
    return template1.render(col_names=col_names, data = data)



if __name__ == "__main__":
    app.run(debug=True)


