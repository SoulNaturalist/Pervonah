import os
import time
import vk_api 
import random
import config
import requests
from sys import platform
from time import gmtime, strftime


class VK_Sender(config.Settings):
    def __init__(self):
        self.config = config.Settings()
        self.list_ids = []
    
    def get_proxy_state_and_session(self):        
        if self.config.PROXY:
            active_sesion = requests.Session()

            #IF YOU USE PROXY, UNCOMMENT CODE 

            #active_sesion.proxies.update({'http': 'http://203.30.189.46:80'})

            api = vk_api.VkApi(self.config.LOGIN, self.config.PASSWORD)#session=active_sesion)

            api.auth()

            return api.get_api()

        elif not self.config.PROXY:
            api = vk_api.VkApi(self.config.LOGIN, self.config.PASSWORD)

            api.auth()

            api = api.get_api()

            return api
            
    def get_groups_user(self, api):
        groups  = api.groups.get(filter='groups, publics', count=200)

        groups_ids = groups['items'] 

        if platform == "linux" or platform == "linux2":
            os.system('clear')
        elif platform == "win32":
            os.system('cls')

        return groups_ids

    def vk_send_messages(self, api):
        self.get_groups_user = VK_Sender.get_groups_user(self, api)
        while True:
            try:
                time.sleep(self.config.DELAY)

                post = api.wall.get(filters='owner',counts=1,owner_id=f'-{random.choice(self.get_groups_user)}')
                try:
                    comments = post['items'][0]['comments']['count']
                except IndexError:
                    comments = 0
                try:
                    likes = post['items'][0]['likes']['count']
                except IndexError:
                    likes = 0
                if comments < 5 and likes < 90:
                    postID = post['items'][0]['id']

                    sourceID = post['items'][0]['owner_id']

                    if postID not in self.list_ids:
                        if not self.config.PHOTOS:
                            self.list_ids.append(postID)
                            message_text = random.choice(self.config.LIST_MESSAGE)
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
                        elif not self.list_message:
                            self.list_ids.append(postID)
                            random_photo = random.choice(self.photos)
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
                            self.list_ids.append(postID)
                            random_photo = random.choice(self.photos)
                            message_text = random.choice(self.list_message)
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
                print(f'Появилась капча - {captcha.get_url()}')
                captcha_key = input('Введите капчу:')
                captcha.try_again(captcha_key)
            except vk_api.exceptions.AccountBlocked:
                print('Ваш аккаунт заблокировали')
                break
            except vk_api.exceptions.VkApiError as e:
                print(e)

    def starting(self):
        self.banner = config.Settings.get_banner(self)
        print(self.banner)
        self.api = VK_Sender.get_proxy_state_and_session(self)
        self.get_groups_user = VK_Sender.get_groups_user(self, self.api)
        self.vk_send_messages = VK_Sender.vk_send_messages(self, self.api)




class MainStart(VK_Sender):
    if __name__ == "__main__":
        Started_class = VK_Sender()
        Started_class.starting()
        
        

    



