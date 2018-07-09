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

class BasePage(object):
    url = None

    def __init__(self, driver):
        self.driver = driver
        self.driver.set_page_load_timeout(60)
        self.WebDriverWait = WebDriverWait
        self.action = ActionChains(self.driver)

    def find_by_name(self, name):
        return self.WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.NAME, name))
        )
    def find_by_id(self, id):
        return self.WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.ID, id))
        )

    def find_by_css(self, css_selector):
        return self.WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )

    def find_by_xpath(self, xpath):
        return self.WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    def move_to_element(self,element):
        self.action.move_to_element(element).click().perform()


    def navigate(self):
        self.driver.get(self.url)

class LoginPage(BasePage):
    url = "https://www.instagram.com/accounts/login/"

    def enter_login(self, login):
        self.find_by_name('username').send_keys(login)

    def enter_password(self, password):
        self.find_by_name('password').send_keys(password)

    def submit(self):
        submit_button = self.find_by_css('form.HmktE span button')
        submit_button.click()


class SearchPage(BasePage):
    url = "https://www.instagram.com"

    def enter_word_to_search_box(self,word):
        search_box = self.find_by_xpath('//span[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        search_box.clear()
        search_box.send_keys(word)

    def chose_top_search_result(self):
        top_search_result = self.find_by_xpath('//span[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a')
        top_search_result.click()

    def chose_followed_user_search_result(self,followed_user_login):
        followed_user_search_result = self.find_by_xpath('//a[@href="/' + followed_user_login + '/"]')
        followed_user_search_result.click()

    def getapp_box_turn_off(self):
        try:
            app_box_close_button = self.find_by_xpath('//body/div[1]/div/div/div/div/button[contains(text(),"Close")]')
            app_box_close_button.click()
        except:
            print('No get app box')
            pass



class PostPage(BasePage):

    def like(self):
        like_button = self.find_by_xpath('//button[contains(@class,"coreSpriteHeartOpen")]/span')
        if 'glyphsSpriteHeart__filled__24__red_5' in like_button.get_attribute('class'):
            pass
        else:
            like_button.click()

    def follow(self):
        follow_button = self.find_by_xpath('//button[contains(text(),"Follow") or contains(text(),"Following")]')
        if 'Following' in follow_button.text:
            pass
        else:
            follow_button.click()
    def next_post(self):
        next_button = self.find_by_xpath('//a[contains(@class,"coreSpriteRightPaginationArrow")]')
        next_button.click()

    def close_post(self):
        close_button = self.find_by_xpath('//button[contains(text(),"Close")]')
        close_button.click()

    def newest_post(self):
        post = self.find_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div[1]/div[1]/a/div/div[2]')
        post.location_once_scrolled_into_view
        time.sleep(random.randint(1, 3))
        self.action.move_to_element(post).click().perform()

    def followed_user_login(self):
        followed_user_login = self.find_by_xpath('//a[contains(@class,"notranslate")]')
        return followed_user_login.text


    def like_follow(self):
        time.sleep(random.randint(1, 3))
        if random.randint(0, 1):
            time.sleep(random.randint(2, 5))
            self.like()
            time.sleep(random.randint(4, 7))
            self.follow()
            time.sleep(random.randint(1, 3))
        else:
            time.sleep(random.randint(3, 8))
            self.follow()
            time.sleep(random.randint(4, 6))
            self.like()
            time.sleep(random.randint(1, 3))
        self.next_post()
        time.sleep(random.randint(12,16))


class FollowedUserProfilePage(BasePage):


    def get_followed_user_profile(self, followed_user_login):
        self.driver.get('https://www.instagram.com/' + str(followed_user_login) + '/')


    def following_button(self):
        following_button = self.find_by_xpath('//button[text()="Following"]')
        following_button.click()

    def confirm_unfollow(self):
        unfollow_button = self.find_by_xpath('//button[text()="Unfollow"]')
        unfollow_button.click()

    def unfollow_user(self, db, followed_user_login):
        self.followed_user_login = followed_user_login
        self.db = db
        self.following_button()
        self.confirm_unfollow()
        self.db.update_followed_user_status_unfollowed(self.followed_user_login)


