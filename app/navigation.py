import sqlite3
from datetime import datetime
import config
import mysql.connector


def list_projects() :
    con = mysql.connector.connect(
            host = config.HOST,
            user = config.USER,
            password = config.PASSWORD,
            database = config.DATABASE
        )
    cur = con.cursor()
    cur.execute('''SELECT NAME FROM PROJECT''')
    project_list = cur.fetchall()
    con.commit()
    con.close()
    return project_list

def get_params():
    con = mysql.connector.connect(
            host = config.HOST,
            user = config.USER,
            password = config.PASSWORD,
            database = config.DATABASE
        )
    cur = con.cursor()
    cur.execute('''SELECT TYPE FROM TRANSACTION_TYPES ORDER BY TYPE''')
    transaction_types = cur.fetchall()
    cur.execute('''SELECT CLASS FROM TRANSACTION_CLASSES ORDER BY CLASS''')
    transaction_classes = cur.fetchall()
    cur.execute('''SELECT SENDER FROM TRANSACTION_SENDER ORDER BY SENDER''')
    transaction_sender = cur.fetchall()
    cur.execute('''SELECT RECIPIENT FROM TRANSACTION_RECIPIENT ORDER BY RECIPIENT''')
    transaction_recipient= cur.fetchall()
    con.commit()
    con.close()

    return transaction_types, transaction_classes, transaction_sender, transaction_recipient

def add_project(project_name):
    con = mysql.connector.connect(
            host = config.HOST,
            user = config.USER,
            password = config.PASSWORD,
            database = config.DATABASE
        )
    cur = con.cursor()
    cur.execute('''SELECT MAX(IDX) FROM PROJECT''')
    max_idx = cur.fetchone()[0]
    if max_idx is None :
        max_idx = 0
    cur.execute('''INSERT INTO PROJECT VALUES (%s, %s, %s, %s)''', (max_idx + 1, datetime.now(), project_name, 'Sandra'))
    con.commit()
    con.close()

def get_project_data(project_name):
    con = mysql.connector.connect(
            host = config.HOST,
            user = config.USER,
            password = config.PASSWORD,
            database = config.DATABASE
        )
    cur = con.cursor()
    cur.execute('''SELECT * FROM PROJECT_DATA WHERE PROJECT_NAME = %s ORDER BY DATE DESC''', [(project_name)])
    transactions_list = cur.fetchall()
    for i in range(len(transactions_list)):
        list_i = list(transactions_list[i])
        list_i[1] = datetime.strftime(list_i[1], "%d %B %Y")
        transactions_list[i] = tuple(list_i)
    con.commit()
    con.close()

    return transactions_list

def get_timelapse(project_name):
    con = mysql.connector.connect(
            host = config.HOST,
            user = config.USER,
            password = config.PASSWORD,
            database = config.DATABASE
        )
    cur = con.cursor()
    cur.execute('''SELECT DISTINCT DATE FROM PROJECT_DATA WHERE PROJECT_NAME = %s ORDER BY DATE DESC''', [(project_name)])
    transaction_month = cur.fetchall()
    transaction_month_format = [(datetime.strftime(d[0], '%B %Y'), ) for d in transaction_month]
    con.commit()
    con.close()
    return list(sorted(set(transaction_month_format), key=transaction_month_format.index))


def add_transaction(project_name, transaction_date, transaction_name, transaction_type, transaction_class, transaction_sender, transaction_recipient, transaction_value):
    con = mysql.connector.connect(
            host = config.HOST,
            user = config.USER,
            password = config.PASSWORD,
            database = config.DATABASE
        )
    cur = con.cursor()
    cur.execute('''SELECT MAX(IDX) FROM PROJECT_DATA''')
    max_idx = cur.fetchone()[0]
    if max_idx is None :
        max_idx = 0
    cur.execute("""INSERT INTO PROJECT_DATA VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", \
            (max_idx + 1, transaction_date, project_name,\
            transaction_class, transaction_type, transaction_name, transaction_value, \
            transaction_sender, transaction_recipient, 'Sandra'))
    con.commit()
    con.close()

def add_param(param_type, new_value):
    con = mysql.connector.connect(
            host = config.HOST,
            user = config.USER,
            password = config.PASSWORD,
            database = config.DATABASE
        )
    cur = con.cursor()
    if param_type == 'type' :
        cur.execute('''SELECT MAX(IDX) FROM TRANSACTION_TYPES''')
        max_idx = cur.fetchone()[0]
        if max_idx is None :
            max_idx = 0
        cur.execute('''INSERT INTO TRANSACTION_TYPES VALUES(%s, %s)''', (max_idx + 1, new_value))
    elif param_type == 'class' :
        cur.execute('''SELECT MAX(IDX) FROM TRANSACTION_CLASSES''')
        max_idx = cur.fetchone()[0]
        if max_idx is None :
            max_idx = 0
        cur.execute('''INSERT INTO TRANSACTION_CLASSES VALUES(%s, %s)''', (max_idx + 1, new_value))
    elif param_type == 'recipient' :
        cur.execute('''SELECT MAX(IDX) FROM TRANSACTION_RECIPIENT''')
        max_idx = cur.fetchone()[0]
        if max_idx is None :
            max_idx = 0
        cur.execute('''INSERT INTO TRANSACTION_RECIPIENT VALUES(%s, %s)''', (max_idx + 1, new_value))
    elif param_type == 'sender' :
        cur.execute('''SELECT MAX(IDX) FROM TRANSACTION_SENDER''')
        max_idx = cur.fetchone()[0]
        if max_idx is None :
            max_idx = 0
        cur.execute('''INSERT INTO TRANSACTION_SENDER VALUES(%s, %s)''', (max_idx + 1, new_value))
    else :
        print("No corresponding table")
    con.commit()
    con.close()
