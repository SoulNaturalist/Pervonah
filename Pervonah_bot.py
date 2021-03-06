import os
import time
import vk_api 
import random
import requests
from sys import platform
from time import gmtime, strftime
from colorama import Fore, Back, Style


LOGIN = ''

PASSW = ''

DELAY = 6.6

list_message = []

photos = []

list_ids = []

BANNER = '''
▒█░░▒█ ▒█░▄▀ 　 ▒█▀▀█ ▒█▀▀▀ ▒█▀▀█ ▒█░░▒█ ▒█▀▀▀█ ▒█▄░▒█ ░█▀▀█ ▒█░▒█ 
░▒█▒█░ ▒█▀▄░ 　 ▒█▄▄█ ▒█▀▀▀ ▒█▄▄▀ ░▒█▒█░ ▒█░░▒█ ▒█▒█▒█ ▒█▄▄█ ▒█▀▀█ 
░░▀▄▀░ ▒█░▒█ 　 ▒█░░░ ▒█▄▄▄ ▒█░▒█ ░░▀▄▀░ ▒█▄▄▄█ ▒█░░▀█ ▒█░▒█ ▒█░▒█
'''

active_sesion = requests.Session()

active_sesion.proxies.update({'http': 'http://203.30.189.46:80'})

api = vk_api.VkApi(LOGIN, PASSW, session=active_sesion)

api.auth()

api = api.get_api()

groups  = api.groups.get(filter='groups, publics', count=200)

account_info = api.account.getProfileInfo()

acount_name = account_info['first_name']

acount_lastname = account_info['last_name']

acount_id = account_info['id']

groups_ids = groups['items'] 

if platform == "linux" or platform == "linux2":
    os.system('clear')
elif platform == "win32":
    os.system('cls')
print(Fore.BLUE + BANNER)
print(f'Активный аккаунт {acount_name} {acount_lastname} {acount_id}ID')

while True:
    try:
        time.sleep(DELAY)

        post = api.wall.get(filters='owner',counts=1,owner_id=f'-{random.choice(groups_ids)}')

        comments = post['items'][0]['comments']['count']

        like = post['items'][0]['likes']['count']
    
        if comments < 5 and like < 90:
            postID = post['items'][0]['id']

            sourceID = post['items'][0]['owner_id']
            if postID not in list_ids:
                if not photos:
                    list_ids.append(postID)
                    message_text = random.choice(list_message)
                    comment = api.wall.createComment(owner_id=sourceID,post_id=postID,message=message_text)
                    comment_id = comment['comment_id']
                    api.likes.add(type='comment', owner_id=sourceID, item_id=comment_id)
                    print(f'''
-----------------------------------------------------------------
Комментарий оставлен ✅
Ссылка на комментарий - https://vk.com/wall{sourceID}_{postID}
Когда был оставлен комментарий - {strftime('%H:%M:%S')}
Сообщение: {message_text}
-----------------------------------------------------------------
                    ''')
                elif not list_message:
                    list_ids.append(postID)
                    random_photo = random.choice(photos)
                    comment = api.wall.createComment(owner_id=sourceID,post_id=postID,attachments=random_photo)
                    comment_id = comment['comment_id']
                    api.likes.add(type='comment', owner_id=sourceID, item_id=comment_id)
                    print(f'''
-----------------------------------------------------------------
Комментарий оставлен ✅
Ссылка на комментарий - https://vk.com/wall{sourceID}_{postID}
Когда был оставлен комментарий - {strftime('%H:%M:%S')}
Сообщение: {message_text}
-----------------------------------------------------------------
                    ''')
                        
                else:
                    list_ids.append(postID)
                    random_photo = random.choice(photos)
                    message_text = random.choice(list_message)
                    comment = api.wall.createComment(owner_id=sourceID,post_id=postID,message=message_text, attachments=random_photo)
                    comment_id = comment['comment_id'] 
                    api.likes.add(type='comment', owner_id=sourceID, item_id=comment_id)
                    print(f'''
-----------------------------------------------------------------
Комментарий оставлен ✅
Ссылка на комментарий - https://vk.com/wall{sourceID}_{postID}
Когда был оставлен комментарий - {strftime('%H:%M:%S')}
Сообщение: {message_text}
-----------------------------------------------------------------
                    ''')
                   
    except vk_api.exceptions.Captcha as captcha:
        captcha.sid  
        print(f'Появилась капча - {captcha.get_url()}')
        captcha_key = input('Введите капчу:')
        captcha.try_again(captcha_key)
    except vk_api.exceptions.AccountBlocked:
        print('Ваш аккаунт заблокировали')
        break
    except vk_api.exceptions.VkApiError:
        pass




