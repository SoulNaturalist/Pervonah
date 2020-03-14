import vk
import time
from random import randint
from time import gmtime, strftime

#getting a info
TOKEN = input('vk token:')
mess_unput = input('1 mess,2 mess,3 mess/messages:')
group_unput = input('group_id1,group_id2/groups and write file ids.txt:')

while True:
    #Time should not be changed
    time.sleep(150)
    session = vk.Session(access_token=TOKEN)
    api = vk.API(session ,v='5.92', lang='ru')
    post = api.newsfeed.get(filters='post',counts=1,source_ids=group_unput.split(','))
    #get information about new posts
    postID = post ['items'][0]['post_id']
    
    sourceID = post ['items'][0]['source_id']
    
    like = post['items'][0]['likes']['user_likes']
    
    mess = mess_unput.split(',')
    
    #generate random message
    mess_generate = mess[randint(0,len(mess)-1,)]
    
    with open("ids.txt") as file:

        ids = file.read().split(",")



    for _ in range(len(ids)):

     try:
        api.wall.createComment(owner_id=ids[_-1],post_id=postID,message=mess_generate)
        print('Комментарий оставлен ' + 'https://vk.com/wall' + str(sourceID) + '_' + str(postID) + ' |' + str(strftime('[%H:%M:%S]')) + ' |' + 'Сообщение оставил : ' + mess_generate)


     except vk.exceptions.VkAPIError:
         pass
