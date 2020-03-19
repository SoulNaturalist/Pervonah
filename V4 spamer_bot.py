import vk
import random
import time
from random import randint
from time import gmtime, strftime
from array import *

#getting a info
TOKEN = input('vk token:')
mess_unput = input('1 mess,2 mess,3 mess/messages:')
group_unput = input('group_id1,group_id2/groups and write file ids.txt:')
photos = input('photo348382404_457251335 or not photo write -/photos:')
a = []
while True:
    #Time should not be changed
    time.sleep(2.2)
    session = vk.Session(access_token=TOKEN)
    api = vk.API(session ,v='5.92', lang='ru')
    post = api.newsfeed.get(filters='post',counts=1,source_ids=group_unput.split(','))
    #get information about new posts
    postID = post ['items'][0]['post_id']

    sourceID = post ['items'][0]['source_id']

    like = post['items'][0]['likes']['user_likes']

    mess = mess_unput.split(',')

    photo = photos.split(',')

    #generate random message
    mess_generate = mess[randint(0,len(mess)-1,)]

    #generate random photo
    photo_generate = random.choice(photo)
    
    with open("ids.txt") as file:

        ids = file.read().split(",")
        
    for _ in range(len(ids)):
        
        try:
            if not postID  in a:
                if photos == '-':
                    api.wall.createComment(owner_id=ids[_-1],post_id=postID,message=mess_generate)
                    print('Комментарий оставлен ' + 'https://vk.com/wall' + str(sourceID) + '_' + str(postID) + ' |' + str(strftime('[%H:%M:%S]')) + ' |' + 'Сообщение оставил : ' + mess_generate)
                    a.append(postID)
                elif photos == '':
                    api.wall.createComment(owner_id=ids[_-1],post_id=postID,message=mess_generate)
                    print('Комментарий оставлен ' + 'https://vk.com/wall' + str(sourceID) + '_' + str(postID) + ' |' + str(strftime('[%H:%M:%S]')) + ' |' + 'Сообщение оставил : ' + mess_generate)
                    a.append(postID)
                else:
                    api.wall.createComment(owner_id=ids[_-1],post_id=postID,message=mess_generate,attachments=photo_generate)
                    print('Комментарий оставлен ' + 'https://vk.com/wall' + str(sourceID) + '_' + str(postID) + ' |' + str(strftime('[%H:%M:%S]')) + ' |' + 'Сообщение оставил : ' + mess_generate)
                    a.append(postID)
                    
            if postID in a:
                pass

        except vk.exceptions.VkAPIError:
            pass
