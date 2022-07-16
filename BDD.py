import sqlite3
import os

def creation_BDD() :
    db_name = input('Database name ?')
    print(os.getcwd() + '/' + db_name + '/' + db_name + '.db')
    con = sqlite3.connect(os.getcwd() + '/' + db_name + '/' + db_name + '.db')

    cur = con.cursor()

    cur.execute('''DROP TABLE IF EXISTS PROJECT''')
    cur.execute('''CREATE TABLE PROJECT 
                (IDX integer primary key AUTOINCREMENT, 
                DATE date, 
                NAME text, 
                CREATOR text)''')
    
    cur.execute('''DROP TABLE IF EXISTS PROJECT_DATA''')
    cur.execute('''CREATE TABLE PROJECT_DATA
                (IDX integer primary key AUTOINCREMENT,
                DATE date,
                PROJECT_NAME text,
                CLASS text,
                TYPE text,
                NAME text,
                VALUE real,
                SENDER text,
                RECIPIENT text,
                CREATOR text)
                ''')

    cur.execute('''DROP TABLE IF EXISTS TRANSACTION_TYPES''')
    cur.execute('''CREATE TABLE TRANSACTION_TYPES
                (IDX integer primary key AUTOINCREMENT,
                TYPE text)
                ''')
    
    cur.execute('''DROP TABLE IF EXISTS TRANSACTION_CLASSES''')
    cur.execute('''CREATE TABLE TRANSACTION_CLASSES
                (IDX integer primary key AUTOINCREMENT,
                CLASS text)
                ''')

    cur.execute('''DROP TABLE IF EXISTS TRANSACTION_SENDER''')
    cur.execute('''CREATE TABLE TRANSACTION_SENDER
                (IDX integer primary key AUTOINCREMENT,
                SENDER text)
                ''')

    cur.execute('''DROP TABLE IF EXISTS TRANSACTION_RECIPIENT''')
    cur.execute('''CREATE TABLE TRANSACTION_RECIPIENT
                (IDX integer primary key AUTOINCREMENT,
                RECIPIENT text)
                ''')
    
    con.commit()
    con.close()

creation_BDD()