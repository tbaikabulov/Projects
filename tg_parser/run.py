import configparser
import json
import pandas as pd
import warnings
import asyncio
import nest_asyncio
import string
from functions import letters, name, action_to_text
warnings.filterwarnings("ignore")

import telethon
from telethon.sync import TelegramClient
from telethon import connection

# для корректного переноса времени сообщений в json
from datetime import date, datetime
# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import Channel, ChannelParticipantsSearch
# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Содержание конфиг файла:
# [Telegram]
# api_id = 8094641
# api_hash = cd74b346bfd50a9e2b1163f23209534a
# phone = +79191001922
# username = timuret

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

# Создаем клиент и подключаемся
client = TelegramClient(username, api_id, api_hash)
client.start()
print("Client Created")

# Проверяем, что мы авторизированы. На этом шаге телеграм запросит пароль и код.
if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        client.sign_in(phone, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))

nest_asyncio.apply()

async def dump_all_participants(channel):
    df = pd.DataFrame({'group': [], 'name': [], 'username':[],'id':[]})
    title = channel.title
    participants_ids = []   

    i = 0
    while True:
        # делаем поиск по 1 букве имени для всех букв, 
        # чтобы избежать ограничения на 10000
        filter_user = ChannelParticipantsSearch(letters[i])
        if i==0:
            participants = await client.get_participants(channel)
        else:
            participants = await client.get_participants(channel, filter = filter_user)
        for user in participants:
            if user.id not in participants_ids:
                participants_ids +=[user.id]
                df.loc[df.shape[0]] = [title, name(user.first_name, user.last_name), user.username, str(user.id)]
        #print(title, letters[i], len(participants_ids))
        if i>len(letters)-2 or (len(participants) < 8500 and i==0):
            break
        i+=1
        
    df.to_csv('chat_users.csv', index=False)


async def dump_all_messages(channel):
    df = pd.DataFrame({'group': [], 'name': [], 'username':[],'id':[],'message':[],'date':[]})
    title = channel.title

    messages = await client.get_messages(channel, limit = 3000)
    for m in messages:
        user = m.sender
        if m.message == None:
            t = action_to_text(m.action)
        if m.action == None:
            t = m.message
        if type(user) == telethon.tl.types.User:
            df.loc[df.shape[0]] = [title, name(user.first_name, user.last_name), user.username, str(user.id), t, m.date]
        if type(user) == telethon.tl.types.Channel:
            df.loc[df.shape[0]] = [title, user.title, None, user.id, t, m.date]

    df.to_csv('chat_messages.csv', index=False)


async def main(url):
    channel = await client.get_entity(url)
    await dump_all_participants(channel)
    print('users downloaded')
    await dump_all_messages(channel)
    print('messages downloaded')

url = 'https://telegram.me/startupchat'
ans = asyncio.run(main(url))
print("finished download")