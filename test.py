import sqlite3
from datetime import datetime
import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


con = sqlite3.connect(os.getcwd() + '/db/Budget.db')
cur = con.cursor()
project_name = 'Budget mensuel'
sql = '''SELECT CLASS, SUM(VALUE) FROM PROJECT_DATA WHERE PROJECT_NAME = ? AND TYPE = ? GROUP BY CLASS ORDER BY SUM(VALUE) DESC LIMIT 10'''
transactions = pd.DataFrame(cur.execute(sql, [project_name, 'Débit']).fetchall(), columns = ['Catégorie', 'Montant'])

colors = sns.color_palette('flare', 10)
plt.pie(transactions['Montant'], labels=transactions['Catégorie'], colors=colors, autopct='%.0f%%')
plt.title("Top 10 des dépenses sur la période")
plt.show()