import sqlite3
from datetime import datetime
import config


def list_projects() :
    con = sqlite3.connect(config.PATH_TO_DB)
    cur = con.cursor()
    project_list = cur.execute('''SELECT NAME FROM PROJECT''').fetchall()
    con.commit()
    con.close()
    return project_list

def get_params():
    con = sqlite3.connect(config.PATH_TO_DB)
    cur = con.cursor()
    transaction_types = cur.execute('''SELECT TYPE FROM TRANSACTION_TYPES ORDER BY TYPE''').fetchall()
    transaction_classes = cur.execute('''SELECT CLASS FROM TRANSACTION_CLASSES ORDER BY CLASS''').fetchall()
    transaction_sender = cur.execute('''SELECT SENDER FROM TRANSACTION_SENDER ORDER BY SENDER''').fetchall()
    transaction_recipient= cur.execute('''SELECT RECIPIENT FROM TRANSACTION_RECIPIENT ORDER BY RECIPIENT''').fetchall()
    con.commit()
    con.close()

    return transaction_types, transaction_classes, transaction_sender, transaction_recipient

def add_project(project_name):
    con = sqlite3.connect(config.PATH_TO_DB)
    cur = con.cursor()
    max_idx = cur.execute('''SELECT MAX(IDX) FROM PROJECT''').fetchone()[0]
    if max_idx is None :
        max_idx = 0
    cur.execute('''INSERT INTO PROJECT VALUES (?, ?, ?, ?)''', [max_idx + 1, datetime.now(), project_name, 'Sandra'])
    con.commit()
    con.close()

def get_project_data(project_name):
    con = sqlite3.connect(config.PATH_TO_DB)
    cur = con.cursor()
    transactions_list = cur.execute('''SELECT * FROM PROJECT_DATA WHERE PROJECT_NAME = ? ORDER BY DATE DESC''', [project_name]).fetchall()
    for i in range(len(transactions_list)):
        list_i = list(transactions_list[i])
        date_int = datetime.strptime(list_i[1], '%Y-%m-%d')
        list_i[1] = datetime.strftime(date_int, "%d %B %Y")
        transactions_list[i] = tuple(list_i)
    con.commit()
    con.close()

    return transactions_list

def get_timelapse(project_name):
    con = sqlite3.connect(config.PATH_TO_DB)
    cur = con.cursor()
    transaction_month = cur.execute('''SELECT DISTINCT DATE FROM PROJECT_DATA WHERE PROJECT_NAME = ? ORDER BY DATE DESC''', [project_name]).fetchall()
    transaction_month_format = [(datetime.strftime(datetime.strptime(d[0], '%Y-%m-%d'), '%B %Y'), ) for d in transaction_month]
    con.commit()
    con.close()
    return list(sorted(set(transaction_month_format), key=transaction_month_format.index))


def add_transaction(project_name, transaction_date, transaction_name, transaction_type, transaction_class, transaction_sender, transaction_recipient, transaction_value):
    con = sqlite3.connect(config.PATH_TO_DB)
    cur = con.cursor()
    max_idx = cur.execute('''SELECT MAX(IDX) FROM PROJECT_DATA''').fetchone()[0]
    if max_idx is None :
        max_idx = 0
    cur.execute('''INSERT INTO PROJECT_DATA VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', \
            [max_idx + 1, transaction_date, project_name,\
            transaction_class, transaction_type, transaction_name, transaction_value, \
            transaction_sender, transaction_recipient, 'Sandra'])
    con.commit()
    con.close()

def add_param(param_type, new_value):
    con = sqlite3.connect(config.PATH_TO_DB)
    cur = con.cursor()
    if param_type == 'type' :
        max_idx = cur.execute('''SELECT MAX(IDX) FROM TRANSACTION_TYPES''').fetchone()[0]
        if max_idx is None :
            max_idx = 0
        cur.execute('''INSERT INTO TRANSACTION_TYPES VALUES(?, ?)''', [max_idx + 1, new_value])
    elif param_type == 'class' :
        max_idx = cur.execute('''SELECT MAX(IDX) FROM TRANSACTION_CLASSES''').fetchone()[0]
        if max_idx is None :
            max_idx = 0
        cur.execute('''INSERT INTO TRANSACTION_CLASSES VALUES(?, ?)''', [max_idx + 1, new_value])
    elif param_type == 'recipient' :
        max_idx = cur.execute('''SELECT MAX(IDX) FROM TRANSACTION_RECIPIENT''').fetchone()[0]
        if max_idx is None :
            max_idx = 0
        cur.execute('''INSERT INTO TRANSACTION_RECIPIENT VALUES(?, ?)''', [max_idx + 1, new_value])
    elif param_type == 'sender' :
        max_idx = cur.execute('''SELECT MAX(IDX) FROM TRANSACTION_SENDER''').fetchone()[0]
        if max_idx is None :
            max_idx = 0
        cur.execute('''INSERT INTO TRANSACTION_SENDER VALUES(?, ?)''', [max_idx + 1, new_value])
    else :
        print("No corresponding table")
    con.commit()
    con.close()
