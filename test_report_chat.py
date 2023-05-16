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
 

    r = "SELECT toDate(time) AS days, count(reciever_id) AS message, uniq(reciever_id) AS chat\
    FROM simulator.message_actions \
    WHERE days > today() - 8 and days != today() \
    GROUP BY days\
    ORDER BY days"

    #Отчёт по сообщениям за вчера
    df_mes = pandahouse.read_clickhouse(r, connection=connection)

    #график чатов за неделю
    plt.figure(figsize = (12,8))
    plt.xlabel("ДАТА",size=20)
    plt.ylabel("Количество чатов",size=20)
    sns.lineplot(data = df_mes, x = 'days', y = 'chat', label = 'chat', lw = 7,
            marker = '.', 
             markersize=7, 
             markeredgewidth=7, 
             markeredgecolor='black')
    plt.title ('Количество чатов за 7 дней',size=20, color='red')

    plot_chat = io.BytesIO()
    plt.savefig(plot_chat)
    plot_chat.name = 'plot_chat.png'
    plot_chat.seek(0)
    
    bot.sendPhoto(chat_id =chat_id, photo = plot_chat)
    
    #график сообщений за неделю
    plt.figure(figsize = (12,8))
    plt.xlabel("ДАТА",size=20)
    plt.ylabel("Количество сообщений",size=20)
    sns.lineplot(data = df_mes, x = 'days', y = 'message', label = 'message', lw = 7,
            marker = '.', 
             markersize=7, 
             markeredgewidth=7, 
             markeredgecolor='black')
    plt.title ('Количество сообщений за 7 дней',size=20, color='red')

    plot_mes = io.BytesIO()
    plt.savefig(plot_mes)
    plot_mes.name = 'tplot_mes.png'
    plot_mes.seek(0)
    
    bot.sendPhoto(chat_id =chat_id, photo = plot_mes)

    
    

try:
    test_report()
   
except Exception as e:
    print(e)          
