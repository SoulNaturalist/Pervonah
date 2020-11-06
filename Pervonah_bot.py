import vk
import random
import time
from random import randint
from time import gmtime, strftime



token = input('Введите вк токен:')


mess_unput = input('Введите сообщения:')

group_unput = input('Введите id групп:')

photos = input('Введите фото:')
list_ids = []
session = vk.Session(access_token=token)
api = vk.API(session ,v='5.92', lang='ru')
while True:
    time.sleep(2.2)

    post = api.newsfeed.get(filters='post',counts=1,source_ids=group_unput.split(','))

    postID = post['items'][0]['post_id']

    sourceID = post['items'][0]['source_id']

    like = post['items'][0]['likes']['user_likes']

    mess = mess_unput.split(',')

    photo = photos.split(',')


    mess_generate = mess[randint(0,len(mess)-1,)]


    photo_generate = random.choice(photo)
    
    with open("ids.txt") as file:

        ids = file.read().split(",")
        
    for _ in range(len(ids)):
        try:
            if postID not in list_ids:
                if photos == '-' or photos == '':
                    list_ids.append(postID)
                    comment = api.wall.createComment(owner_id=ids[_-1],post_id=postID,message=mess_generate)
                    comment_id = comment['comment_id']
                    api.likes.add(type='comment', owner_id=sourceID, item_id=comment_id)
                    print('Комментарий оставлен ' + 'https://vk.com/wall' + str(sourceID) + '_' + str(postID) + ' |' + str(strftime('[%H:%M:%S]')) + ' |' + 'Сообщение оставил : ' + mess_generate)
                
                else:
                    list_ids.append(postID)
                    comment = api.wall.createComment(owner_id=ids[_-1],post_id=postID,message=mess_generate,attachments=photo_generate)
                    comment_id = comment['comment_id'] 
                    api.likes.add(type='comment', owner_id=sourceID, item_id=comment_id)
                    print('Комментарий оставлен ' + 'https://vk.com/wall' + str(sourceID) + '_' + str(postID) + ' |' + str(strftime('[%H:%M:%S]')) + ' |' + 'Сообщение оставил : ' + mess_generate)
                   
        except vk.exceptions.VkAPIError:
            pass