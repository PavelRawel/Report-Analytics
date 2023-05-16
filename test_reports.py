import telegram
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandahouse
import pandas as pd
import io
import os

sns.set()
sns.set_style("whitegrid")



def test_report (Chat = None):
    bot = telegram.Bot(token = '5053394805:AAGrHouRQ2FYSRBJHrS31TaxWDFmWM7i7Go')
    chat_id = -708816698
    

    connection = {
    'host': 'https://clickhouse.lab.karpov.courses',
    'password': 'dpo_python_2020',
    'user': 'student',
    'database': 'simulator'
    }
 

    z = "SELECT toDate(time) AS days, countIf(user_id, action= 'like' ) AS like, countIf(user_id, action= 'view' ) AS view,\
    countIf(user_id, action='like')*100/countIf(user_id, action='view') AS ctr, count(user_id) AS user_uniq, uniq(user_id) AS dau\
    FROM simulator.feed_actions \
    WHERE days = today()-1 \
    GROUP BY days"

#отправляем отчёт за вчера
    
    df_yesterday = pandahouse.read_clickhouse(z, connection=connection)
    
    day = str(df_yesterday['days'].dt.date[0])
    dau = str(int(df_yesterday['dau'][0]/1000))
    ctr = str(round(df_yesterday['ctr'][0],2))
    view = str(int(df_yesterday['view'][0]/1000))
    like = str(int(df_yesterday['like'][0]/1000))

    msg = 'Лента новостей. Показатели за вчера ({}):\ndau - {} K\nview - {} K\nlike - {} K\nctr - {} %'.format(day,dau,view,like,ctr)
    bot.sendMessage(chat_id = chat_id, text =msg)

#отправляем графики за неделю

    w = "SELECT toDate(time) AS days, countIf(user_id, action= 'like' ) AS like, countIf(user_id, action= 'view' ) AS view,\
    countIf(user_id, action='like')*100/countIf(user_id, action='view') AS ctr, count(user_id) AS user_uniq, uniq(user_id) AS dau\
    FROM simulator.feed_actions \
    WHERE days > today() - 8 and days != today() \
    GROUP BY days\
    ORDER BY days"

    df_week = pandahouse.read_clickhouse(w, connection=connection)

#график DAU за 7 дней
    plt.figure(figsize = (12,8))
    plt.xlabel("ДАТА",size=20)
    plt.ylabel("Уникальных пользователей (DAU)",size=20)
    sns.lineplot(data = df_week, x = 'days', y = 'dau', label = 'dau', lw = 7,
             marker = '.', 
             markersize=7, 
             markeredgewidth=7, 
             markeredgecolor='black')
    plt.title ('DAU за 7 дней',size=20, color='red')

    plot_object2 = io.BytesIO()
    plt.savefig(plot_object2)
    plot_object2.name = 'test_plot2.png'
    plot_object2.seek(0)
    
    bot.sendPhoto(chat_id =chat_id, photo = plot_object2)

#График лайков за 7 дней
    plt.figure(figsize = (12,8))
    plt.xlabel("ДАТА",size=20)
    plt.ylabel("Лайки",size=20)
    sns.lineplot(data = df_week, x = 'days', y = 'like',label = 'like', lw = 7,
             marker = '.', 
             markersize=7, 
             markeredgewidth=7, 
             markeredgecolor='black')
    plt.title ('Лайки за 7 дней',size=20, color='red')

    plot_object3 = io.BytesIO()
    plt.savefig(plot_object3)
    plot_object3.name = 'test_plot3.png'
    plot_object3.seek(0)

    bot.sendPhoto(chat_id =chat_id, photo = plot_object3)

#График просмотров за 7 дней
    plt.figure(figsize = (12,8))
    plt.xlabel("ДАТА",size=20)
    plt.ylabel("Просмотры",size=20)
    sns.lineplot(data = df_week, x = 'days', y = 'view',label = 'view', lw = 7,
             marker = '.', 
             markersize=7, 
             markeredgewidth=7, 
             markeredgecolor='black')
    plt.title ('Просмотры за 7 дней',size=20, color='red')


    plot_object1 = io.BytesIO()
    plt.savefig(plot_object1)
    plot_object1.name = 'test_plot1.png'
    plot_object1.seek(0)
    
    bot.sendPhoto(chat_id =chat_id, photo = plot_object1)

#График CTR за 7 дней
    plt.figure(figsize = (12,8))
    plt.xlabel("ДАТА",size=20)
    plt.ylabel("CTR,%",size=20)
    sns.lineplot(data = df_week, x = 'days', y = 'ctr',label = 'ctr',lw = 7,
             marker = '.', 
             markersize=7, 
             markeredgewidth=7, 
             markeredgecolor='black')
    plt.title ('CTR за 7 дней',size=20, color='red')

    plot_object = io.BytesIO()
    plt.savefig(plot_object)
    plot_object.name = 'test_plot.png'
    plot_object.seek(0)

    bot.sendPhoto(chat_id =chat_id, photo = plot_object)

    
    

try:
    test_report()
   
except Exception as e:
    print(e)          
