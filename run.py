import configparser
import json
import pandas as pd
import warnings
import asyncio
import nest_asyncio
import string
from functions import letters, name
warnings.filterwarnings("ignore")

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

urls = '''https://t.me/wbchat_wb
https://t.me/MarketplaceChati
https://t.me/stat4marketcom
https://t.me/WBchatik
https://t.me/sert_ru2
https://t.me/wildberries_ozon_yandex
https://t.me/ozon_mplace
https://t.me/mpstatsio
https://t.me/tandemseller_4at
https://t.me/gildia_marketplace
https://t.me/sellercenter_online
https://t.me/tovarohkas
https://t.me/Marketplace_WB
https://t.me/wbcon4us'''
urls = urls.split()

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
df = pd.DataFrame({'group': [], 'name': [], 'username':[],'id':[]})
df.to_csv('chat_users.csv', index=False)

async def dump_all_participants(channel):
    title = channel.title
    offset_user = 0    # номер участника, с которого начинается считывание
    limit_user = 100   # максимальное число записей, передаваемых за один раз
    all_participants = []   # список всех участников канала
    participants_ids = []   

    i = 0
    big_chat = False

    participants = await client.get_participants(channel)

    for user in participants:
        if user.id not in participants_ids:
            all_participants+=[user]
            participants_ids +=[user.id]
    print(title, letters[i], len(all_participants))
    if len(participants) > 8500:
        big_chat = True


    while big_chat:
        # собираем всех участников чата, делая сначала общий поиск, а потом по 1 букве имени, 
        # чтобы избежать ограничения offset_user < 10000
        filter_user = ChannelParticipantsSearch(letters[i])
        participants = await client.get_participants(channel, filter = filter_user)
        for user in participants:
            if user.id not in participants_ids:
                all_participants+=[user]
                participants_ids +=[user.id]
        print(title, letters[i], len(all_participants))
        i+=1
        if i>len(letters)-2:
            break
        

    print('Start saving')
    try:
        df = pd.read_csv('chat_users.csv')
    except FileNotFoundError:
        df = pd.DataFrame({'group': [], 'name': [], 'username':[],'id':[]})
    for i in range(len(all_participants)):
        participant = all_participants[i]
        df.loc[df.shape[0]] = [title, name(participant.first_name, participant.last_name), participant.username, participant.id]
    df.to_csv('chat_users.csv', index=False)


async def dump_all_messages(channel):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0    # номер записи, с которой начинается считывание
    limit_msg = 100   # максимальное число записей, передаваемых за один раз

    all_messages = []   # список всех сообщений
    total_messages = 0
    total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

    class DateTimeEncoder(json.JSONEncoder):
        '''Класс для сериализации записи дат в JSON'''
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        print('offset_msg = ' + str(offset_msg))
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            #print(message.message)
            all_messages.append(message.to_dict())
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    with open('channel_messages.json', 'w', encoding='utf8') as outfile:
         json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main(url):
    channel = await client.get_entity(url)
    await dump_all_participants(channel)
    print('users downloaded')
    #await dump_all_messages(channel)

ans = asyncio.run(main(urls[0]))
print("finished download")