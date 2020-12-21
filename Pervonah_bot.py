import vk_api 
import random
import time
from time import gmtime, strftime

LOGIN = 'number'

PASSW = 'user password'

DELAY = 6.6

BANNER = '''
▒█░░▒█ ▒█░▄▀ 　 ▒█▀▀█ ▒█▀▀▀ ▒█▀▀█ ▒█░░▒█ ▒█▀▀▀█ ▒█▄░▒█ ░█▀▀█ ▒█░▒█ 
░▒█▒█░ ▒█▀▄░ 　 ▒█▄▄█ ▒█▀▀▀ ▒█▄▄▀ ░▒█▒█░ ▒█░░▒█ ▒█▒█▒█ ▒█▄▄█ ▒█▀▀█ 
░░▀▄▀░ ▒█░▒█ 　 ▒█░░░ ▒█▄▄▄ ▒█░▒█ ░░▀▄▀░ ▒█▄▄▄█ ▒█░░▀█ ▒█░▒█ ▒█░▒█
'''

mess_unput = [

]

photos = [

]


list_ids = []

api = vk_api.VkApi(LOGIN, PASSW)

api.auth()

api = api.get_api()

groups  = api.groups.get(filter='groups, publics', count=200)

account_info = api.account.getProfileInfo()

acount_name = account_info['first_name']

acount_lastname = account_info['last_name']

acount_id = account_info['id']

groups_ids = groups['items'] 

print(BANNER)

print(f'Активный аккаунт {acount_name} {acount_lastname} id{acount_id}.')

while True:
    time.sleep(DELAY)

    post = api.wall.get(filters='owner',counts=1,owner_id=f'-{random.choice(groups_ids)}')

    comments = post['items'][0]['comments']['count']

    like = post['items'][0]['likes']['count']
   
    if comments < 5 and like < 90:

        postID = post['items'][0]['id']

        sourceID = post['items'][0]['owner_id']
        try:
            if postID not in list_ids:
                message_text = random.choice(mess_unput)
                if not photos:
                    list_ids.append(postID)
                    comment = api.wall.createComment(owner_id=sourceID,post_id=postID,message=message_text)
                    comment_id = comment['comment_id']
                    api.likes.add(type='comment', owner_id=sourceID, item_id=comment_id)
                    print(f'''Комментарий оставлен ✅
                    Ссылка на комментарий - https://vk.com/wall{sourceID}_{postID}
                    Когда был оставлен комментарий - {strftime('[%H:%M:%S]')}
                    Сообщение оставил: {message_text}
                    ''')
                        
                else:
                    random_photo = random.choice(photos)
                    list_ids.append(postID)
                    comment = api.wall.createComment(owner_id=sourceID,post_id=postID,message=message_text, attachments=random_photo)
                    comment_id = comment['comment_id'] 
                    api.likes.add(type='comment', owner_id=sourceID, item_id=comment_id)
                    print(f'''Комментарий оставлен ✅
                    Ссылка на комментарий - https://vk.com/wall{sourceID}_{postID}
                    Когда был оставлен комментарий - {strftime('[%H:%M:%S]')}
                    Сообщение оставил: {message_text}
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



