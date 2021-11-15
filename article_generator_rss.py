import json
import mysql.connector as MySQLdb
from CONSTANT import *
import xmltodict
import requests
import os
import articles_management
from newspaper import Article


def fetch_rss(url):
    res = requests.get(url)

    if res.status_code == 200:
        with open("test.xml", "w", encoding="utf8") as xml_file:
            xml_file.write(res.text)

        with open("test.xml", encoding="utf8") as xml_file:
            data_dict = xmltodict.parse(xml_file.read())
            xml_file.close()
            json_data = json.dumps(data_dict)

            with open("data.json", "w") as json_file:
                json_file.write(json_data)
                json_file.close()
    else:
        print(res.status_code)

    with open("data.json", "r") as json_file:
        data = json.load(json_file)
    os.remove("test.xml")
    os.remove("data.json")
    return data


def parse_article(url):
    article = Article(url)
    article.download()
    article.parse()
    username = article.authors[0]
    anchor_tag = f"""\n\n [Source {article.url}]({article.url})"""
    post = article.text + anchor_tag
    thumbnail = article.top_image

    article.nlp()
    tags = ','.join(article.keywords)
    return username, post, tags, thumbnail


def make_data(record):
    url = record['link']
    username, post, tags, thumbnail = parse_article(url)
    title = record['title']
    description = record['description'][:100]
    return username, title, description, tags, thumbnail, post


def log_record(link):
    db = MySQLdb.connect(user=db_user, password=db_pass,
                         host=db_host, database=db_database)
    try:
        cursor = db.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS rss_log (id INT(6) PRIMARY KEY AUTO_INCREMENT, '
            'link VARCHAR(10000) DEFAULT "None");')
        db.commit()
        sql = "insert into rss_log (link) values (%s);"
        cursor.execute(sql, [link])
        db.commit()
        db.close()
        return True, f"Log Created: {link}"
    except Exception as e:
        print(e)
        return False, None
    finally:
        db.close()
        return True, f"Log Created: {link}"


def start(url="https://gadgets.ndtv.com/rss/android/feeds", category="others", max=1):
    if not category in ['mobile', 'pc', 'others', 'ai-ml', 'tech', 'gaming']:
        return "Category not in- 'mobile', 'pc', 'others', 'ai-ml', 'tech', 'gaming'"

    if max == "all":
        max = -1

    data = fetch_rss(url)
    data = data['rss']['channel']['item'][:max]

    count = 0
    for record in data:
        try:
            username, title, description, tags, thumbnail, post = make_data(record)
            print(record['link'])
            obj = articles_management.Articles()
            status, msg = obj.create_post_by_parser(username=username, title=title, description=description,
                                                    tags=tags, category=category,
                                                    thumbnail=thumbnail, post=post)
            print(status, msg)
            if status:
                _, log_msg = log_record(record['link'])
                print(log_msg)
                count += 1
        except Exception as e:
            print(e)
    return f"{count} Article Created Successfully"


