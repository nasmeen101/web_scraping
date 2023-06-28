from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re  
from werkzeug.security import generate_password_hash, check_password_hash
from get_job import process_job
from datetime import datetime

app = Flask(__name__) 
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'
  
mysql = MySQL(app)  

def get_keyword(data):
    keyword = {}
    for i in data["keyword"]:
        keyword[i["job"]] = i["keyword"]
    return keyword

@app.route('/')
@app.route("/index")
def index():
        args = request.args
        if args.get("input_date"):
            input_date = args.get("input_date").split("/")
            input_date = datetime(
                int(input_date[2]), int(input_date[0]), int(input_date[1])
            )
        else:
            input_date = datetime.now()
        data, keyword, job_setting = process_job(input_date)
        keywords = get_keyword(keyword)
        data_list = []
        for i in job_setting:
            keyword = []
            for c in keywords[i["job"]]:
                keyword.append(
                    {
                        "keyword": list(c.keys())[0],
                        "frequency": c[list(c.keys())[0]]["frequency"],
                    }
                )
            keyword_group = []
            for x in i["group"]:
                frequency = 0
                for g in x[list(x.keys())[0]]:
                    for n in keyword:
                        if g == n["keyword"]:
                            frequency += n["frequency"]
                keyword_group.append({"keyword": list(x.keys())[0], "frequency": frequency})
            data_list.append(
                {"job": i["job"], "detail": data[i["job"]], "keyword": keyword_group}
            )
        return render_template("index.html", data=data_list)

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        print(password)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        user = cursor.fetchone()
        if user:            
            password_rs = user['password']
            print(password_rs)
            if check_password_hash(password_rs, password):
                if user['role'] == 'admin':
                # Create session data, we can access this data in other routes
                    session['loggedin'] = True
                    session['userid'] = user['userid']
                    session['name'] = user['name']
                    session['email'] = user['email']
                    mesage = 'Logged in successfully !'
                    return redirect(url_for('users'))
                else:
                    user['role'] == 'user'
                    # Create session data, we can access this data in other routes
                    session['loggedin'] = True
                    session['userid'] = user['userid']
                    session['name'] = user['name']
                    session['email'] = user['email']
                    mesage = 'Logged in successfully !'
                    return redirect(url_for('index'))
            else:
                mesage = 'Please enter correct email / password !'
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('userid',None)
    session.pop('email',None)
    session.pop('name',None)
    return redirect(url_for('login'))

@app.route("/users", methods =['GET', 'POST'])
def users():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user')
        users = cursor.fetchall()    
        return render_template("users.html", users = users)
    return redirect(url_for('login'))


@app.route("/view", methods =['GET', 'POST'])
def view():
    if 'loggedin' in session:
        viewUserId = request.args.get('userid')   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE userid = % s', (viewUserId, ))
        user = cursor.fetchone()   
        return render_template("view.html", user = user)
    return redirect(url_for('login'))

@app.route("/password_change", methods =['GET', 'POST'])
def password_change():
    mesage = ''
    if 'loggedin' in session:
        changePassUserId = request.args.get('userid')    
        if request.method == 'POST' and 'password' in request.form and 'confirm_pass' in request.form and 'userid' in request.form:
            password = request.form['password']   
            confirm_pass = request.form['confirm_pass'] 
            userId = request.form['userid']
            
            _hashed_password = generate_password_hash(password)

            if not password or not confirm_pass:
                mesage = 'Please fill out the form !'
            elif password != confirm_pass:
                mesage = 'Confirm password is not equal!'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE user SET  password =% s WHERE userid =% s', (_hashed_password, (userId, ), ))
                mysql.connection.commit()
                mesage = 'Password updated !'            
        elif request.method == 'POST':
            mesage = 'Please fill out the form !'        
        return render_template("password_change.html", mesage = mesage, changePassUserId = changePassUserId)
    return redirect(url_for('login'))

@app.route("/delete",methods =['GET'])
def delete():
    if 'loggedin' in session:
        deleteUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM user WHERE userid = % s', (deleteUserId, ))
        mysql.connection.commit()
        return redirect(url_for('users'))
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        country = request.form['country']

        _hashed_password = generate_password_hash(password)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'User already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user (name, email, password, role, country) VALUES ( % s, % s, % s, % s, % s)', (userName, email, _hashed_password, role, country))
            mysql.connection.commit()
            mesage = 'New user created!'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)


@app.route("/edit", methods =['GET', 'POST'])
def edit():
    msg = ''    
    if 'loggedin' in session:
        editUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE userid = % s', (editUserId, ))
        editUser = cursor.fetchone()
        if request.method == 'POST' and 'name' in request.form and 'userid' in request.form and 'role' in request.form and 'country' in request.form:
            userName = request.form['name']   
            role = request.form['role']
            country = request.form['country']            
            userId = request.form['userid']
            if not re.match(r'[A-Za-z0-9]+', userName):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE user SET  name =% s, role =% s, country =% s WHERE userid =% s', (userName, role, country, (userId, ), ))
                mysql.connection.commit()
                msg = 'User updated !'
                return redirect(url_for('users'))
        elif request.method == 'POST':
            msg = 'Please fill out the form !'        
        return render_template("edit.html", msg = msg, editUser = editUser)
    return redirect(url_for('login'))

@app.route('/register_index', methods =['GET', 'POST'])
def register_index():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        country = request.form['country']

        _hashed_password = generate_password_hash(password)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'User already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user (name, email, password, role, country) VALUES ( % s, % s, % s, % s, % s)', (userName, email, _hashed_password, role, country))
            mysql.connection.commit()
            mesage = 'New user created!'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register_index.html', mesage = mesage)


    

if __name__ == "__main__":
    app.run(debug=True)

