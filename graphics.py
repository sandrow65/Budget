import sqlite3
from datetime import datetime
import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

import locale

import config

# locale.setlocale(locale.LC_ALL, 'fr_FR.utf-8')
sns.set_context("paper", rc={"font.size":100,"axes.titlesize":100,"axes.labelsize":100})
sns.set(font_scale=7)   



def get_bars(project_name):
    con = sqlite3.connect(config.PATH_TO_DB)
    cur = con.cursor()
    sql = '''SELECT DATE, VALUE FROM PROJECT_DATA WHERE PROJECT_NAME = ? AND TYPE = ? ORDER BY DATE'''
    positive_transactions = pd.DataFrame(cur.execute(sql, [project_name, 'Crédit']).fetchall(), columns = ['Date', 'Recettes'])
    negative_transactions = pd.DataFrame(cur.execute(sql, [project_name, 'Débit']).fetchall(), columns = ['Date', 'Dépenses'])


    df = pd.concat([positive_transactions, negative_transactions], axis=0)
    df['Date'] = pd.to_datetime(df['Date'],format="%Y-%m-%d")
    # df = df.sort_values(by='Date', ascending=True)
    df['Date'] = df['Date'].dt.strftime('%B %Y')

    df['Recettes'] = df['Recettes'].fillna(0)
    df['Dépenses'] = - df['Dépenses'].fillna(0)

    df['Reste'] = df['Recettes'] + df['Dépenses']

    df = df.set_index('Date')

    df_agg = df.groupby(level='Date', sort=False).sum()
    df_agg = df_agg.reset_index()
    # df_agg = df_agg.sort_values(by=['Date'], axis = 0, ascending = 0)

    print(df, '\n', df_agg)

    ## plot
    sns.set_style('darkgrid', {"grid.color": ".6", "grid.linestyle": ":", "fontsize":"1000"})
    fig = plt.figure(figsize=(80,30))
    ax = fig.add_subplot(111)
    b1 = sns.barplot(data=df_agg, x='Date', y='Recettes', color='royalblue', alpha=0.7, ax=ax, label='big')

    b2 = sns.barplot(data=df_agg, x='Date', y='Dépenses', color='darkred', alpha=0.7, ax=ax, label='big')

    # df_agg.plot.bar(x='Date', y=['Recettes','Dépenses'], color={'Recettes':'green', 'Dépenses':'red'}, logy=True, ax=ax,
    #                 legend=False, alpha=0.7, rot=0)
    sns.lineplot(data=df_agg, x='Date', y='Reste', color='white', legend=False, linewidth=2, linestyle='dashed', marker='*', markersize=12)
    # df_agg.plot.line(x='Date', y='Reste',  color='blue', ax=ax,
    #                 legend=False, linewidth=2, linestyle='dashed', marker='*', markersize=12)
    for i in range(df_agg.shape[0]):
        v = df_agg.iloc[i]['Reste']
        y_lvl = df_agg.iloc[i]['Dépenses']
        ax.annotate(f'{v:n}', xy=(i, v + 10), color='white', fontsize=90) 
    cwd = os.getcwd()
    filename = 'plot_data_' + str.replace(project_name, ' ', '_')
    url = cwd + '/static/images/{}.png'.format(filename)
    total_eco = int(df['Reste'].sum())
    plt.title('Bilan des recettes-dépenses \n Total économisé : ' + str(total_eco) + ' €\n', color='white')
    plt.savefig(url, transparent=True, format='png')

    print("graphics ok")

    con.commit()
    con.close()
    return url, filename

