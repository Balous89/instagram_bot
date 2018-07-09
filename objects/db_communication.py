import sqlite3
from pytz import timezone
from datetime import datetime
import base64
from Crypto import Random
from Crypto.Cipher import AES
import sys
#


#TODO try open db_connection before run and close it in the end

class CryptoData:

    AKEY = 'mysixteenbytekey'

    iv = Random.new().read(AES.block_size)

    def encode(self,text_password):
        obj = AES.new(self.AKEY, AES.MODE_CFB, self.iv)
        return base64.urlsafe_b64encode(obj.encrypt(text_password))

    def decode(self,encoded_password_from_db):
        obj2 = AES.new(self.AKEY, AES.MODE_CFB, self.iv)
        return obj2.decrypt(base64.urlsafe_b64decode(encoded_password_from_db))


class DataBase(CryptoData):

    def date_time_now(self):
        poland = timezone('Europe/Warsaw')
        date_time_now = datetime.now(tz=poland).strftime('%Y-%m-%d %H:%M:%S')
        return date_time_now

    def db_connection(self):
        connection = sqlite3.connect('/home/balous/django_project/instagram/followed_user.db')
        return connection

    def db_cursor(self,db_connection):
        db_cursor = db_connection.cursor()
        return db_cursor

    def check_instagram_user_in_db_or_add(self,instagram_user_login,instagram_user_password):
        self.instagram_user_login = instagram_user_login
        self.instagram_user_password = instagram_user_password
        db_connection = self.db_connection()
        db_cursor = self.db_cursor(db_connection)
        sql_query = "SELECT user_id FROM instagram_users WHERE user_login=?;"
        db_query = db_cursor.execute(sql_query, (self.instagram_user_login,))
        try:
            insagram_user_id = db_query.fetchone()[0]
        except:
            insagram_user_id = None
        if insagram_user_id != None:
            print('User: {} is in database his ID is: {} '.format(self.instagram_user_login, insagram_user_id))
        else:
            encoded_password = self.encode(self.instagram_user_password)
            sql_query = 'INSERT INTO instagram_users(user_login,user_password) VALUES(?,?)'
            db_cursor.execute(sql_query, (self.instagram_user_login,str(encoded_password),))
            db_connection.commit()
            insagram_user_id = db_cursor.execute('SELECT user_id FROM instagram_users WHERE user_login=?',(self.instagram_user_login,)).fetchone()[0]
            print('User: {} has been added to database his ID is: {} '.format(self.instagram_user_login,insagram_user_id))
        return insagram_user_id

    def insert_new_followed_to_db(self,insagram_user_id,followed_user_login):
        try:
            self.instagram_user_id = insagram_user_id
            self.followed_user_login = followed_user_login
            db_connection = self.db_connection()
            db_cursor = self.db_cursor(db_connection)
            status = 'FOLLOWED'
            sql_query = 'INSERT INTO followed_users(followed_login,followed_add_date,followed_status,user_id) VALUES(?,?,?,?);'
            db_cursor.execute(sql_query, (self.followed_user_login, self.date_time_now(), status,self.instagram_user_id,))
            db_connection.commit()
            print(('Followed user: {} added to database, status: {}').format(self.followed_user_login,status))
        except Exception as exc:
            print(exc, sys.exc_info()[0])
            print('The user has not been added to database!')

    def followed_users_list(self,instagram_user_login):
        self.instagram_user_login = instagram_user_login
        db_connection = self.db_connection()
        db_cursor = self.db_cursor(db_connection)
        sql = 'SELECT followed_login FROM followed_users WHERE followed_status="FOLLOWED" AND user_id=(SELECT user_id FROM instagram_users WHERE user_login=?) ORDER BY followed_add_date ASC;'
        data_from_db = db_cursor.execute(sql, (self.instagram_user_login,))
        followed_users_list=[db_user[0] for db_user in data_from_db]
        return followed_users_list

    def update_followed_user_status_unfollowed(self,followed_user_login):
        self.followed_user_login = followed_user_login
        db_connection = self.db_connection()
        db_cursor = self.db_cursor(db_connection)
        sql_update_status_and_rm_date = 'UPDATE followed_users SET followed_status="UNFOLLOWED",followed_rm_date=? WHERE followed_login=?'
        db_cursor.execute(sql_update_status_and_rm_date, (self.date_time_now(),self.followed_user_login,) )
        db_connection.commit()


