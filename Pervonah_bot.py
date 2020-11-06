import vk
import random
import time
from datetime import datetime, timedelta
from random import randint
from time import gmtime, strftime



token = 'Вставь сюда свой токен'

mess_unput = [
    'Не понял',
    'поясните',
    'а в чом прикол?',
    'А в чём шутка?',
    'пояснительная бригада помоги!!!!',
    'хм'


]

photos = [
    
]


list_ids = []

session = vk.Session(access_token=token)

api = vk.API(session, v='5.92', lang='ru')

groups  = api.groups.get(filter='groups, publics', count=150)

groups_ids = groups['items'] #получение подписок пользователя 

while True:
    time.sleep(6.4)

    post = api.wall.get(filters='owner',counts=1,owner_id=f'-{random.choice(groups_ids)}')

    comments = post['items'][0]['comments']['count']

    like = post['items'][0]['likes']['count']
   
    if comments < 5 and like < 90:

        postID = post['items'][0]['id']

        sourceID = post['items'][0]['owner_id']
        try:
            if postID not in list_ids:
                message_text = random.choice(mess_unput)
                if photos == '-' or photos == '':
                    list_ids.append(postID)
                    api.wall.createComment(owner_id=sourceID,post_id=postID,message=message_text)
                    #comment_id = comment['comment_id']
                    #api.likes.add(type='comment', owner_id=sourceID, item_id=comment_id)
                    print('Комментарий оставлен ' + 'https://vk.com/wall' + str(sourceID) + '_' + str(postID) + ' |' + str(strftime('[%H:%M:%S]')) + ' |' + 'Сообщение оставил : ' +  message_text)
                    
                else:
                    random_photo = random.choice(photos)
                    list_ids.append(postID)
                    api.wall.createComment(owner_id=sourceID,post_id=postID,message=message_text, attachments=random_photo)
                    #comment_id = comment['comment_id'] 
                    #api.likes.add(type='comment', owner_id=sourceID, item_id=comment_id)
                    print('Комментарий оставлен ' + 'https://vk.com/wall' + str(sourceID) + '_' + str(postID) + ' |' + str(strftime('[%H:%M:%S]')) + ' |' + 'Сообщение оставил : ' +  message_text)
        except vk.exceptions.VkAPIError as error:
            print(error)
