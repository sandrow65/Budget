
from flask import Blueprint, Flask, render_template, request, url_for, flash, redirect, send_from_directory, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, login_required, logout_user
from models import User
import auth, init_app

import navigation, graphics

from datetime import datetime
import os

import locale
b=os.getcwd()
os.system(f"echo '{b}'> test")
# locale.setlocale(locale.LC_ALL, 'fr_FR.utf-8')

app = init_app.create_app()

@app.before_first_request
def create_tables():
    init_app.db.create_all()

@app.route('/', methods=('GET', 'POST'))
@login_required
def index():
    
    project_list = navigation.list_projects()
    print( project_list)

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
            pass

    return render_template('index.html', projects = project_list)

@app.route('/project/<project_name>', methods=('GET', 'POST'))
@app.route('/project', defaults={'project_name': None}) 
@login_required
def project(project_name):
    print("ok")

    transaction_types, transaction_classes, transaction_senders, transaction_recipients = navigation.get_params()

    transaction_list = navigation.get_project_data(project_name)
    transaction_month = navigation.get_timelapse(project_name)
    url, filename = graphics.get_bars(project_name)
    print(url, filename)

    if request.method == 'POST':
        if request.form['submit_button'] == 'Ajouter une transaction':
            transaction_date = request.form["transaction_date"]
            transaction_type = request.form['transaction_type']
            transaction_class = request.form['transaction_class']
            transaction_sender = request.form['transaction_sender']
            transaction_recipient = request.form['transaction_recipient']
            transaction_name = request.form['transaction_name']
            transaction_value = request.form['transaction_value']
            navigation.add_transaction(project_name, transaction_date, transaction_name, transaction_type, transaction_class, transaction_sender, transaction_recipient, transaction_value)

    return render_template('project.html', project_name = project_name, transaction_list = transaction_list, transaction_month = transaction_month, \
        transaction_types = transaction_types, transaction_classes = transaction_classes, \
            transaction_sender = transaction_senders, transaction_recipient = transaction_recipients, \
                file_name = filename)

@app.route('/admin', methods=('GET', 'POST'))
@login_required
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
        redirect(url_for('index'))
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)