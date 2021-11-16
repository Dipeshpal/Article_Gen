import random
import newspaper
from datetime import datetime
import articles_management
import nltk
nltk.download('punkt')


def parse(sites):
    count = 0
    for site in sites:
        for article in site.articles:
            article.download()
            article.parse()
            article.nlp()
            tags = ""
            for i in article.keywords:
                tags += i + ","
            sync = articles_management.Articles()
            anchor_tag = f"""\n\n [Source {article.url}]({article.url})"""
            text = article.text + anchor_tag
            author_list = ["Jay", "Adonis", "Sam", "Abhinav", "Lokesh", "Junaid", "Danish"]
            username = random.choice(author_list)
            status, msg = sync.create_post_by_parser(username=username, title=article.title,
                                                     description=article.summary[:100] + "...",
                                                     tags=tags, category="others",
                                                     thumbnail=article.top_image, post=text)
            print(status, msg)
            if status:
                count += 1
            if count == 2:
                break
            # if count % 7 == 0:
            #     try:
            #         if post_count < 3:
            #             insta_bot_post.post_photo(username="techportofficial", password="@Adonis123@",
            #                                       photo_url=article.top_image, caption=article.title, tags=tags)
            #             post_count += 1
            #     except Exception as e:
            #         print(e)
    return count


def start_parsing_articles(sites=None):
    if sites is None:
        sites = ['https://beebom.com/', 'https://www.xda-developers.com/']
    msg = ""
    for site in sites:
        sync = articles_management.Articles()
        now = datetime.now()
        date_str = now.strftime("%m/%d/%Y").replace("/", "-")

        try:
            cursor = sync.db.cursor()
            sql_chk = f"select * from tbl_parsing_date where date='{date_str}' and website='{site}'"
            cursor.execute(sql_chk)
            cursor.fetchall()
            if cursor.rowcount > 0:
                print(f"{site} on {date_str} already exists")
                msg += f"{site} on {date_str} already exists\n | "
                continue
        except Exception as e:
            msg = str(e)
        cursor = sync.db.cursor()
        sql = "create table IF NOT EXISTS tbl_parsing_date (id INT(6) PRIMARY KEY AUTO_INCREMENT, " \
              "date VARCHAR(255), " \
              "fetched VARCHAR(255), " \
              "website VARCHAR(255), " \
              "count INT(255));"
        cursor.execute(sql)
        sync.db.commit()
        site_obj = newspaper.build(site, memoize_articles=False)
        count = parse([site_obj])
        if count > 0:
            fetched = True
        else:
            fetched = False

        try:
            sync = articles_management.Articles()
            cursor = sync.db.cursor()
            sql = "insert into tbl_parsing_date (date, fetched, website, count) values (%s,%s,%s,%s);"
            cursor.execute(sql, [date_str, fetched, site, count])
            sync.db.commit()
            msg += site + ": " + str(count) + "fetched \n | "
        except Exception as e:
            msg += site + ": " + str(count) + "fetched \n | " + str(e)
            print(f"Error in 'insert into tbl_parsing_date': {e}")
    return msg


def info_scrape():
    sync = articles_management.Articles()
    cursor = sync.db.cursor()
    sql = "select * from tbl_parsing_date"
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)


if __name__ == "__main__":
    # info_scrape()
    msg = start_parsing_articles()
