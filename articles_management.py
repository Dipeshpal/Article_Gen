import mysql.connector as MySQLdb
from datetime import datetime
import streamlit as st


class Articles:
    def __init__(self, db_user, db_pass, db_host, db_database):
        self.db = MySQLdb.connect(user=db_user, password=db_pass,
                                  host=db_host, database=db_database)
        print("Connection Established")

    def __del__(self):
        try:
            self.db.close()
            print("Connection closed")
        except ImportError as e:
            print(e)

    def create_post(self, username, title=None, description=None,
                    tags=None, category=None,
                    thumbnail=None, post=None):
        try:
            cursor = self.db.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS tbl_posts (id INT(6) PRIMARY KEY AUTO_INCREMENT, '
                'username VARCHAR(255) NOT NULL,'
                'title VARCHAR(255) DEFAULT "None",'
                'description VARCHAR(255) DEFAULT "None",'
                'tags VARCHAR(255) DEFAULT "None",'
                'category VARCHAR(255) DEFAULT "None",'
                'thumbnail VARCHAR(255) DEFAULT "None",'
                'date VARCHAR(255) DEFAULT "None",'
                'author VARCHAR(255) DEFAULT "None",'
                'link VARCHAR(255) DEFAULT "None",'
                'post VARCHAR(10000) DEFAULT "None");')
            self.db.commit()
            author = username
            date = datetime.today()
            date = date.strftime("%Y-%m-%d")
            link = title.replace(" ", "-")
            # link = re.sub("[^A-Za-z]", "", link)
            post = post.replace("'", "$value$")
            post = post.replace('"', "$value2$")
            post = post.replace(",", "$value3$")
            sql = "insert into tbl_posts (username, title, description, tags, category, thumbnail, post, date, author, link) values (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s);"
            cursor.execute(sql,
                           [username, title, description, tags, category, thumbnail, post, date, author, link])
            self.db.commit()
            return True, "Post Created"
        except Exception as e:
            return False, f"Unable to Create Post. Error: {e}"

    def create_post_by_parser(self, username="Adonis", title=None, description=None,
                              tags=None, category=None,
                              thumbnail=None, post=None):
        try:
            cursor = self.db.cursor()
            sql = f"select * from tbl_posts where LOWER(title) LIKE '{title[:20].lower()}%'"
            cursor.execute(sql)
            cursor.fetchall()
            if cursor.rowcount > 0:
                print("Data already exists", cursor.rowcount)
                self.db.commit()
                return False, "Data already exists"
            cursor = self.db.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS tbl_posts (id INT(6) PRIMARY KEY AUTO_INCREMENT, '
                'username VARCHAR(255) NOT NULL,'
                'title VARCHAR(255) DEFAULT "None",'
                'description VARCHAR(255) DEFAULT "None",'
                'tags VARCHAR(255) DEFAULT "None",'
                'category VARCHAR(255) DEFAULT "None",'
                'thumbnail VARCHAR(255) DEFAULT "None",'
                'date VARCHAR(255) DEFAULT "None",'
                'author VARCHAR(255) DEFAULT "None",'
                'link VARCHAR(255) DEFAULT "None",'
                'post VARCHAR(10000) DEFAULT "None");')
            self.db.commit()
            author = username
            date = datetime.today()
            date = date.strftime("%Y-%m-%d")
            link = title.lower().replace(" ", "-")
            # link = re.sub("[^A-Za-z]", "", link)
            post = post.replace("'", "$value$")
            post = post.replace('"', "$value2$")
            post = post.replace(",", "$value3$")
            sql = "insert into tbl_posts (username, title, description, tags, category, thumbnail, post, date, author, link) values (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s);"
            cursor.execute(sql,
                           [username, title, description, tags, category, thumbnail, post, date, author, link])
            self.db.commit()
            return True, "Post Created"
        except Exception as e:
            print(e)
            return False, f"Unable to Update Post. Error: {e}"

    def update_post(self, username, title=None, description=None,
                    tags=None, category=None,
                    thumbnail=None, post=None, post_id=None):
        try:
            cursor = self.db.cursor()
            author = username
            date = datetime.today()
            date = date.strftime("%Y-%m-%d")
            link = title.lower().replace(" ", "-")
            # link = re.sub("[^A-Za-z]", "", link)
            post = post.replace("'", "$value$")
            post = post.replace('"', "$value2$")
            post = post.replace(",", "$value3$")
            sql = f"update tbl_posts set username='{username}', title='{title}', description='{description}', tags='{tags}', category='{category}', thumbnail='{thumbnail}', date='{date}', author='{author}', link='{link}'"
            sql = sql + ', post="""{post}""" '.format(post=post)
            sql = sql + f"WHERE id={post_id}"
            # print(sql)
            cursor.execute(sql)
            self.db.commit()
            return True, "Post Updated"
        except Exception as e:
            print(e)
            return False, f"Unable to Update Post. Error: {e}"

    def get_single_post(self, post_id):
        try:
            cursor = self.db.cursor(buffered=True)
            sql = f"""select * from tbl_posts where id={post_id}"""
            cursor.execute(sql)
            result = cursor.fetchone()
            post = result[10].replace("$value$", "'")
            post = post.replace('$value2$', '"')
            post = post.replace("$value3$", ",")
            di = {
                'id': result[0],
                'username': result[1],
                'title': result[2],
                'description': result[3],
                'tags': result[4],
                'category': result[5],
                'thumbnail': result[6],
                'date': result[7],
                'author': result[8],
                'post': post,
                'link': result[9]
            }
            return di, True
        except Exception as e:
            return None, f"Something went wrong. Error {e}"

    def get_all_posts(self, category=False):
        try:
            cursor = self.db.cursor(buffered=True)
            if not category:
                sql = f"""select * from tbl_posts"""
            else:
                sql = f"""select * from tbl_posts where category='{category}'"""
            cursor.execute(sql)
            result = cursor.fetchall()
            result = result[::-1]
            li = []
            # post = result[10].replace("$value$", "'")
            # post = post.replace('$value2$', '"')
            # post = post.replace("$value3$", ",")
            for i in result:
                di = {
                    'id': i[0],
                    'username': i[1],
                    'title': i[2],
                    'description': i[3],
                    'tags': i[4],
                    'category': i[5],
                    'thumbnail': i[6],
                    'date': i[7],
                    'author': i[8],
                    'link': i[9],
                    'post': i[10]
                }
                li.append(di)
            return True, li
        except Exception as e:
            return False, "Server not responding " + str(e)

    def get_posts_by_keyword(self, keyword):
        try:
            cursor = self.db.cursor(buffered=True)
            sql = f"""select * from tbl_posts WHERE title LIKE '%{keyword}%'"""
            cursor.execute(sql)
            result = cursor.fetchall()
            result = result[::-1]
            li = []
            for i in result:
                post = i[10].replace("$value$", "'")
                post = post.replace('$value2$', '"')
                post = post.replace("$value3$", ",")
                di = {
                    'id': i[0],
                    'username': i[1],
                    'title': i[2],
                    'description': i[3],
                    'tags': i[4],
                    'category': i[5],
                    'thumbnail': i[6],
                    'date': i[7],
                    'author': i[8],
                    'link': i[9],
                    'post': post
                }
                li.append(di)
            return True, li
        except Exception as e:
            return False, "Server not responding " + str(e)

    def get_posts_by_user(self, username, admin=False):
        try:
            cursor = self.db.cursor(buffered=True)
            if admin:
                sql = f"""select * from tbl_posts"""
            else:
                sql = f"""select * from tbl_posts WHERE username='{username}'"""
            cursor.execute(sql)
            result = cursor.fetchall()
            result = result[::-1]
            li = []
            for i in result:
                post = i[10].replace("$value$", "'")
                post = post.replace('$value2$', '"')
                post = post.replace("$value3$", ",")
                di = {
                    'id': i[0],
                    'username': i[1],
                    'title': i[2][:60] + "...",
                    'description': i[3],
                    'tags': i[4],
                    'category': i[5],
                    'thumbnail': i[6],
                    'date': i[7],
                    'author': i[8],
                    'link': i[9],
                    'post': post
                }
                li.append(di)
            return li
        except Exception as e:
            return False, "Server not responding " + str(e), None

    def get_posts_by_user_and_id(self, username, post_id):
        try:
            cursor = self.db.cursor(buffered=True)
            sql = f"""select * from tbl_posts WHERE username='{username}' AND id={post_id}"""
            cursor.execute(sql)
            result = cursor.fetchall()
            li = []
            for i in result:
                post = i[10].replace("$value$", "'")
                post = post.replace('$value2$', '"')
                post = post.replace("$value3$", ",")
                di = {
                    'id': i[0],
                    'username': i[1],
                    'title': i[2],
                    'description': i[3],
                    'tags': i[4],
                    'category': i[5],
                    'thumbnail': i[6],
                    'date': i[7],
                    'author': i[8],
                    'link': i[9],
                    'post': post
                }
                li.append(di)
            return li, True
        except Exception as e:
            return False, "Server not responding " + str(e), None

    def delete_post(self, username, post_id, admin=False):
        try:
            cursor = self.db.cursor()
            if admin:
                query = f"""DELETE FROM tbl_posts WHERE id={post_id}"""
            else:
                query = f"""DELETE FROM tbl_posts WHERE username='{username}' AND id={post_id}"""
            cursor.execute(query)
            self.db.commit()

            if cursor.rowcount > 0:
                msg = f"{cursor.rowcount} Post Deleted, post_id={post_id}"
            else:
                msg = f"Something went wrong"
            return msg
        except Exception as e:
            return "Error: Server not responding " + str(e)

    def run_query(self, query):
        cursor = self.db.cursor()
        sql = query
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)


import pprint

if __name__ == "__main__":
    obj = Articles()

    # ans = obj.create_post("dipesh pal", title="None", description="None",
    #                 tags="None", category="None",
    #                 thumbnail="None", post="None")
    # print(ans)

    # Update all posts
    _, posts_ = obj.get_all_posts()
    for i in posts_[:]:
        title = i['title']
        link = title.lower().replace(" ", "-")
        print(link)
        _, ans = obj.update_post(i['username'], title=title, description=i['description'],
                                 tags=i['tags'], category=i['category'],
                                 thumbnail=i['thumbnail'], post=i['post'], post_id=i['id'])
        if _:
            ans, _ = obj.get_single_post(i['id'])
            print("Updated: ", "http://thetechport.in/article/" + str(ans['id']) + ans['link'])
