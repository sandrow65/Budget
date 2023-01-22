
from flask import Blueprint, Flask, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb.cursors

import navigation, graphics
import config

from datetime import datetime
import os
import re

import locale
b=os.getcwd()
os.system(f"echo '{b}'> test")

app = Flask(__name__)
app.config['MYSQL_HOST'] = config.HOST
app.config['MYSQL_USER'] = config.USER
app.config['MYSQL_PASSWORD'] = config.PASSWORD
app.config['MYSQL_DB'] = config.DATABASE
app.secret_key = config.SECRET_KEY


print('test print 1')

@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        con = mysql.connector.connect(
                host = config.HOST,
                user = config.USER,
                password = config.PASSWORD,
                database = config.DATABASE
            )
        cursor = con.cursor()
        cursor.execute('SELECT * FROM USER WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        con = mysql.connector.connect(
                host = config.HOST,
                user = config.USER,
                password = config.PASSWORD,
                database = config.DATABASE
            )
        cursor = con.cursor()
        cursor.execute('SELECT * FROM USER WHERE username = %s', [(username)])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('SELECT MAX(IDX) FROM USER')
            max_idx_user = cursor.fetchone()[0]
            if max_idx_user is None :
                max_idx_user = 0
            cursor.execute('INSERT INTO USER VALUES (%s, %s, %s, %s)', (max_idx_user + 1, username, password, email))
            msg = 'You have successfully registered!'
        con.commit()
        con.close()
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/home', methods=('GET', 'POST'))
def home():
    print('blablabla',flush=True)
    print(os.getcwd())
    # Check if user is loggedin
    if 'loggedin' in session:
        project_list = navigation.list_projects()

        if request.method == 'POST':
            if request.form['submit_button'] == 'Créer':
                project_name = request.form['new_project']
                navigation.add_project(project_name)
                return redirect(url_for('project', project_name = str(project_name)))
            elif request.form['submit_button'] == 'Sélectionner':
                project_name = request.form['project']
                return redirect(url_for('project', project_name = str(project_name)))
            elif request.form['submit_button'] == 'Gérer' : 
                return redirect(url_for('admin'))
            else :
                return redirect(url_for('home'))

        return render_template('home.html', projects = project_list, username=session['username'])
    else :
        # User is not loggedin redirect to login page
        return redirect(url_for('login'))

@app.route('/home/project/<project_name>', methods=('GET', 'POST'))
@app.route('/home/project', defaults={'project_name': None}) 
def project(project_name):

    transaction_types, transaction_classes, transaction_senders, transaction_recipients = navigation.get_params()

    transaction_list = navigation.get_project_data(project_name)
    transaction_month = navigation.get_timelapse(project_name)
    url, filename = graphics.get_bars(project_name)
    url_cat, filename_cat = graphics.get_piechart(project_name)
    form_keys = list(request.form.to_dict().keys())
    if request.method == 'POST':
        if 'submit_button' in form_keys:
            if request.form['submit_button'] == 'Ajouter une transaction':
                transaction_date = request.form["transaction_date"]
                transaction_type = request.form['transaction_type']
                transaction_class = request.form['transaction_class']
                transaction_sender = request.form['transaction_sender']
                transaction_recipient = request.form['transaction_recipient']
                transaction_name = request.form['transaction_name']
                transaction_value = request.form['transaction_value']
                navigation.add_transaction(project_name, transaction_date, transaction_name, transaction_type, transaction_class, transaction_sender, transaction_recipient, transaction_value)
        else :
            selected_month = form_keys[0]
            url_cat, filename_cat = graphics.get_piechart(project_name, selected_month)

    return render_template('project.html', project_name = project_name, transaction_list = transaction_list, transaction_month = transaction_month, \
        transaction_types = transaction_types, transaction_classes = transaction_classes, \
            transaction_sender = transaction_senders, transaction_recipient = transaction_recipients, \
                file_name = filename, file_name2 = filename_cat)

@app.route('/admin', methods=('GET', 'POST'))
def admin():
    if request.method in ('POST'):
        if request.form['submit_button'] == "Ajouter le type":
            new_type = request.form["new_type"]
            navigation.add_param('type', new_type)
        elif request.form['submit_button'] == "Ajouter la catégorie":
            new_class = request.form["new_class"]
            navigation.add_param('class', new_class)
        elif request.form['submit_button'] == "Ajouter le destinataire":
            new_recipient = request.form["new_recipient"]
            navigation.add_param('recipient', new_recipient)
        elif request.form['submit_button'] == "Ajouter l'expéditeur":
            new_sender = request.form["new_sender"]
            navigation.add_param('sender', new_sender)
        redirect(url_for('home'))
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, use_reloader=True)