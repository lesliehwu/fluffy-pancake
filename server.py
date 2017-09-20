from flask import Flask, render_template, redirect, flash, request, session
import re
import datetime
from mysqlconnection import MySQLConnector
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app=Flask(__name__)
app.secret_key='poquitoPOQUITO'
mysql = MySQLConnector(app, 'login_registration')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('success.html')

@app.route('/validate', methods=['post'])
def validate():
    
    ##REGISTRATION VALIDATION
    if request.form['validate'] == 'register':
        session['first_valid'] = False
        session['last_valid'] = False
        session['is_logged_in'] = False
        session['email_valid'] = False
        session['password_valid'] = False
        
        if len(request.form['first_name']) < 2:
            flash("First name must be at least two characters long")
            return redirect('/')
        elif not (request.form['first_name']).isalpha():
            flash("First name can only contain letters")
            return redirect('/')
        else:
            session['first_valid'] = True

        #LAST NAME VALIDATION
        if len(request.form['last_name']) < 2:
            flash("Last name must be at least two characters long")
            return redirect('/')
        elif not(request.form['last_name']).isalpha():
            flash("Last name can only contain letters")
            return redirect('/')
        else:
            session['last_valid'] = True

        #EMAIL VALIDATION
        if len(request.form['email']) < 1:
            flash("Email cannot be empty")
            return redirect('/')
        elif not EMAIL_REGEX.match(request.form['email']):
            flash("Email must be valid")
            return redirect('/')
        else:
            session['email_valid'] = True

        #PASSWORD VALIDATION
        if len(request.form['password']) < 1:
            flash("Password cannot be empty")
            return redirect('/')
        elif len(request.form['password']) < 8:
            flash("Password must be at least 8 characters long")
            return redirect('/')
        else:
            session['password_valid'] = True

        #CONFIRMATION VALIDATION
        if request.form['confirm'] != request.form['password']:
            flash("This field must match with password")
            return redirect('/')

        if (session['first_valid'] and session['last_valid'] and session['email_valid'] and session['password_valid']):
            query = "INSERT INTO users (first_name, last_name, email, password, created_at) VALUES ('" + request.form['first_name'] + "', '" + request.form['last_name'] + "', '" + request.form['email'] + "', '" + request.form['password'] + "', NOW());"
            mysql.query_db(query)
            session['is_logged_in'] = True

    ##LOGIN VALIDATION
    if request.form['validate'] == 'login':

        session['is_logged_in'] = False
        session['email_valid'] = False
        session['password_valid'] = False

        query = "SELECT email FROM users WHERE email = '" + request.form['email'] + "';"
        
        if (mysql.query_db(query)):
            session['email_valid'] = True
            query2 = "SELECT password FROM users WHERE email = '" + request.form['email'] + "';"
            print query
            print query2
            print mysql.query_db(query)
            print mysql.query_db(query2)
            print request.form['email']
            print request.form['password']
            if (mysql.query_db(query2)[0]['password'] == request.form['password']): 
                session['password_valid'] = True
            else:
                flash ("Password is incorrect")
                return redirect('/')
        else:
            flash("Email not found, please register")
            return redirect('/')

        if (session['email_valid'] and session['password_valid']):
            session['is_logged_in'] = True

    ##CHECK TO SEE IF CAN BE LOGGED IN
    if (session['is_logged_in']):
        return redirect('/home')

app.run(debug=True)
