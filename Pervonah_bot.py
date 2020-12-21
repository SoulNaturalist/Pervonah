import vk_api 
import random
import time
from time import gmtime, strftime

LOGIN = 'number'

PASSW = 'user password'

DELAY = 4

mess_unput = [

]

photos = [

]


list_ids = []

api = vk_api.VkApi(LOGIN, PASSW)

api.auth()

api = api.get_api()

groups  = api.groups.get(filter='groups, publics', count=500)

groups_ids = groups['items'] 

while True:
    time.sleep(DELAY)

    post = api.wall.get(filters='owner',counts=1,owner_id=f'-{random.choice(groups_ids)}')

    comments = post['items'][0]['comments']['count']

    like = post['items'][0]['likes']['count']
   
    if comments < 5 and like < 90:

        postID = post['items'][0]['id']

        sourceID = post['items'][0]['owner_id']
        try:
            try:
                if postID not in list_ids:
                    message_text = random.choice(mess_unput)
                    if not photos:
                        list_ids.append(postID)
                        comment = api.wall.createComment(owner_id=sourceID,post_id=postID,message=message_text)
                        comment_id = comment['comment_id']
                        api.likes.add(type='comment', owner_id=sourceID, item_id=comment_id)
                        print('Комментарий оставлен ' + 'https://vk.com/wall' + str(sourceID) + '_' + str(postID) + ' |' + str(strftime('[%H:%M:%S]')) + ' |' + 'Сообщение оставил : ' +  message_text)
                        
                    else:
                        random_photo = random.choice(photos)
                        list_ids.append(postID)
                        comment = api.wall.createComment(owner_id=sourceID,post_id=postID,message=message_text, attachments=random_photo)
                        comment_id = comment['comment_id'] 
                        api.likes.add(type='comment', owner_id=sourceID, item_id=comment_id)
                        print('Комментарий оставлен ' + 'https://vk.com/wall' + str(sourceID) + '_' + str(postID) + ' |' + str(strftime('[%H:%M:%S]')) + ' |' + 'Сообщение оставил : ' +  message_text)
            except api.exceptions.Captcha as captcha:
                captcha.sid  
                print(f'Появилась капча - {captcha.get_url()}')
                captcha_key = input('Введите капчу:')
                captcha.try_again(captcha_key)
        except Exception as error:
            print(f'Ошибка {error}')

