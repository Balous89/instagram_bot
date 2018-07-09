# import sqlite3
# connection = sqlite3.connect('/home/balous/django_project/instagram/followed_user.db')
# cursor = connection.cursor()
# sql = "INSERT INTO followed_users VALUES (?,?);"
# data = (None, 'Json1',)
# sql2="""CREATE TABLE followed_users (
# 	followed_id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
# 	followed_status	TEXT DEFAULT 'UNFOLLOWED',
# 	followed_login	TEXT NOT NULL UNIQUE,
# 	followed_add_date	INTEGER,
# 	followed_rm_date	INTEGER,
# 	user_id	INTEGER UNIQUE,
# 	FOREIGN KEY(user_id) REFERENCES instagram_users(user_id)
# );"""
#
# cursor.execute(sql2,)
# connection.commit()