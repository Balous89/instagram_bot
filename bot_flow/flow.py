from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions
import time
import random
from random import shuffle
from selenium.webdriver.common.action_chains import ActionChains
from objects.page_objects import LoginPage,SearchPage,PostPage, FollowedUserProfilePage
from objects.db_communication import DataBase
import sys

driver = webdriver.Chrome(executable_path='/home/balous/django_project/chromedriver')
action = ActionChains(driver)
key_words=['#security','#coding','#devops','#social','#testing',"#softwaretesting","#army","selfdevelopment"] 
instagram_user_login = ''#ENTER HERE YOUR`S INSTAGRAM LOGIN
password = '' #ENTER HERE YOUR`S INSTAGRAM PASSWORD
db = DataBase()
search_box = SearchPage(driver)
followed_user_profile = FollowedUserProfilePage(driver)

try:
    log_ing_user_id = db.check_instagram_user_in_db_or_add(instagram_user_login, password)
    login = LoginPage(driver)
    login.navigate()
    login.enter_login(instagram_user_login)
    login.enter_password(password)
    login.submit()
except Exception as exc:
    print(exc,sys.exc_info()[0])
    print('Check login data for user: ' + instagram_user_login)
try:
    search_box.getapp_box_turn_off()
    followed_user_list = db.followed_users_list(instagram_user_login)
    print(len(followed_user_list))
    if len(followed_user_list) >= 2500:
        try:
            for x in range(random.randint(35,51)):
                followed_user_list = db.followed_users_list(instagram_user_login)
                for followed_user_login in followed_user_list[:10]:
                    print(followed_user_login)
                    search_box.enter_word_to_search_box(followed_user_login)
                    time.sleep(random.randint(1, 3))
                    search_box.chose_followed_user_search_result(followed_user_login)
                    time.sleep(random.randint(2, 5))
                    followed_user_profile.unfollow_user(db, followed_user_login)
                    time.sleep(random.randint(22, 36))
        except Exception as exc:
            print(exc, sys.exc_info()[0])
except Exception as exc:
    print(exc, sys.exc_info()[0])
    print(exc)
    print('Check access data')
    raise
try:
    for x in range(len(key_words)):
        search_box.enter_word_to_search_box(key_words[random.randint(0, len(key_words)-1)])
        search_box.chose_top_search_result()
        post = PostPage(driver)
        post.newest_post()
        for x in range(6):
            followed_user_login = post.followed_user_login()
            db.insert_new_followed_to_db(log_ing_user_id, followed_user_login)
            post.like_follow()
            time.sleep(random.randint(30,40))
        post.close_post()
        search_box.navigate()
        print('Take a break!')
        time.sleep(random.randint(780, 1020))
except Exception as exc:
    print(exc,sys.exc_info()[0])
    print('Error in run with keyword!')
    raise


finally:
    driver.quit()



