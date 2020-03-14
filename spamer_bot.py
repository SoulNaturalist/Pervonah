import vk
import time
from random import randint
from time import gmtime, strftime

#getting a token
TOKEN = input('vk token:')
mess_unput = input('1 mess,2 mess,3 mess/messages:')
group_unput = input('group_id1,group_id2/groups and write file ids.txt:')

while True:
    #Time should not be changed
    time.sleep(150)
    #Time should not be changed
    session = vk.Session(access_token=TOKEN)
    api = vk.API(session ,v='5.92', lang='ru')
    #groups in which this bot will spam
    #'-132364112,-188071916,-57992530,-84054237,-102087446,-164031005,-45739204,-111230293,-184352846,188071916,-138794053,-155464693,-163682546,-22751485,-47949197,-45745333,-23243883,-149152237,-45571312,-133761984,-164353993,-101072212,-73598440,-30316056,-53845179l,-88245281,-70147321,-92879038,-111230293,-114086029,-47949197,-103083994,-67580761,-143276111,-30316056,-163544068,-129071054,-66678575,-160710432,-132364112,-188526562,-147166906,-177318222,-150909727,186735596,-73672378,-188468307,-98699940,-144181254,-157193952,-154168174,-131382340,-24581636,-12353330,-182719373,-86886389,-120254617,-157116504,-173166698,-188755633,-93566453,-109317623,-165937659,-189250661,167127847,-126754563,-118140055,-169208615,-44901473,-189476988,-150550417,-96591297,-142918020,-43696984,-57876954,-135209264,-57846937,-23148107,-163195758,-126754563,-61166138,-172222275,-79145826,-169729973,-182136933,-160905377,-64701856,-98699940'
    post = api.newsfeed.get(filters='post',counts=1,source_ids=group_unput.split(','))
    #get information about new posts
    postID = post ['items'][0]['post_id']
    sourceID = post ['items'][0]['source_id']
    like = post['items'][0]['likes']['user_likes']
    #messages that the bot will use
    mess = mess_unput.split(',')
    # spam by groups from a file
    mess_generate = mess[randint(0,len(mess)-1,)]
    with open("ids.txt") as file:

        ids = file.read().split(",")



    for _ in range(len(ids)):

     #attempt to write a comment
     try:
        api.wall.createComment(owner_id=ids[_-1],post_id=postID,message=mess_generate)
        print('Комментарий оставлен ' + 'https://vk.com/wall' + str(sourceID) + '_' + str(postID) + ' |' + str(strftime('[%H:%M:%S]')) + ' |' + 'Сообщение оставил : ' + mess_generate)

     #error exception
     except vk.exceptions.VkAPIError:
         pass
