import datetime
import json
from newspaper import Article
import requests
# import nlpcloud
from lazyme.string import color_print as cprint
import nltk

nltk.download('punkt')


def article_rewrite_step_4_optional(text):
    # # https://docs.nlpcloud.com/
    # try:
    #     client = nlpcloud.Client("finetuned-gpt-neox-20b", "264f2760ecc3d734ca19b9bde814f9a1ef64d799", True)
    #     # Returns a json object.
    #     paraphrased_text = client.paraphrasing(text)['paraphrased_text']
    #     return paraphrased_text
    # except Exception as e:
    #     print(f"Error in article_rewrite. {e}")
    #     return text
    print(f"\t\t\tRewriting (3)...")
    try:
        url = "https://imseldrith-article-rewriter.hf.space/api/predict"
        payload = {
            "data": [text]
        }
        response = requests.post(url, json=payload)
        print(response.json())
        return response.json()['data'][0]
    except Exception as e:
        return text
    # try:
    #     r = requests.post(url='https://dipesh-paraphrase-pegasus-article-rewri-ebe11dd.hf.space/api/predict/',
    #                       json={"data": [text]})
    #     return r.json()['data'][0]
    # except Exception as e:
    #     print(f"Error in article_rewrite (paraphrase-pegasus). {e}")
    #     return text


def scrape_article_step_3(url):
    print("\tScraping (2):", url)
    try:
        toi_article = Article(url, language="en")  # en for English
        toi_article.download()
        toi_article.parse()
        toi_article.nlp()
        return toi_article.text, toi_article.keywords
    except Exception as e:
        raise Exception(f"Error in scraping. {e}")


def auth_step_6(BASE_URL, NLPCLOUD_TOKEN, TECHPORT_EMAIL, TECHPORT_PASSWORD, REWRITE):
    try:
        url = f"{BASE_URL}/login/"

        payload = f'username={TECHPORT_EMAIL}&password={TECHPORT_PASSWORD}'
        headers = {
            'Authorization': 'Basic Og==',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()
    except Exception as e:
        raise Exception(f"Error in auth. {e}")


def post_news_step_5(title, thumbnail, tags, category, body, post_by_ai, source_url, BASE_URL, NLPCLOUD_TOKEN,
                     TECHPORT_EMAIL, TECHPORT_PASSWORD, REWRITE):
    print("\t\t\tPosting (4)...", title)
    try:
        res_json = auth_step_6(BASE_URL, NLPCLOUD_TOKEN, TECHPORT_EMAIL, TECHPORT_PASSWORD, REWRITE)
        access_token = res_json['access_token']
        url = f"{BASE_URL}/blog/"

        # format body after 8 full stops change line
        body_list = body.split(".")

        new_body = ""
        c = 0
        for i in body_list:
            c += 1
            if c % 8 == 0:
                new_body += i + ".\r"
            else:
                new_body += i + "."

        body = new_body

        payload = json.dumps({
            "title": f"{title}",
            "thumbnail": f"{thumbnail}",
            "tags": f"{tags}",
            "category": f"{category}",
            "body": f"{body}",
            "post_by_ai": f"{post_by_ai}",
            "source_url": f"{source_url}"
        })
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.status_code, response.json()
    except Exception as e:
        raise Exception(f"Error in post_news. {e}")


def submit_news_step_2(article, category_name, BASE_URL, NLPCLOUD_TOKEN, TECHPORT_EMAIL, TECHPORT_PASSWORD, REWRITE):
    print(f"Processing (1):", article['title'])
    try:
        title = article['title']
        thumbnail = article['urlToImage']
        category = category_name
        body, tags = scrape_article_step_3(article['url'])
        if len(body) < 200:
            print("Skipping", title)
            raise Exception(f"Skipping {title}")
        if REWRITE:
            body = article_rewrite_step_4_optional(body)
        else:
            print("\t\tSkipping Rewriting (3)...")
        post_by_ai = True
        source_url = article['url']
        status, response_json = post_news_step_5(title, thumbnail, tags, category, body, post_by_ai, source_url,
                                                 BASE_URL, NLPCLOUD_TOKEN, TECHPORT_EMAIL, TECHPORT_PASSWORD, REWRITE)
        return status, response_json
    except Exception as e:
        raise Exception(f"Error in submit_news. {e}")


# All articles mentioning Apple from yesterday, sorted by popular publishers first
def get_news_step_1(BASE_URL, NLPCLOUD_TOKEN, TECHPORT_EMAIL, TECHPORT_PASSWORD, REWRITE):
    try:
        total_posts = 0
        total_success = 0
        total_failed = 0
        date_today = datetime.datetime.now().date()
        date_yesterday = date_today - datetime.timedelta(days=1)
        ai = ["artificial intelligence", "machine learning", "deep learning"]
        mobile = ["apple", "mobile", "iphone", "samsung", "android", "oneplus",
                  "xiaomi", "oppo", "vivo", "realme"]
        computer = ["microsoft", "google", "laptop"]
        gaming = ["pubg", "fortnite", "minecraft", "valorant", "PC games", "console games", "gaming", "gamer", "gta", ]

        topics_dict = {"mobile": mobile, "gaming": gaming, "pc": computer, "ai-ml": ai}

        for category_name, category in topics_dict.items():
            for topic in category:
                print(f"{'-' * 20}{category_name} | {topic} {'-' * 20}")
                url = (f"https://newsapi.org/v2/everything?q={topic}"
                       f"&from={date_yesterday}"
                       f"&to={date_yesterday}"
                       f"&sortBy=popularity"
                       f"&apiKey={'e024295ccbd2400da561aade71bbdb61'}")

                response = requests.get(url).json()
                print('Article Fetched Successfully: ', response['status'])
                articles = response['articles']

                for article in articles:
                    try:
                        status, response_json = submit_news_step_2(article, category_name, BASE_URL, NLPCLOUD_TOKEN,
                                                                   TECHPORT_EMAIL, TECHPORT_PASSWORD, REWRITE)
                    except Exception as e:
                        cprint(f"Error in submit_news. {e}", "red")
                        status = 500
                        response_json = {"message": f"Exception in submit_news {e}"}

                    if status == 201:
                        print("\t\t\t\tSuccess (Posted):", article['title'])
                        cprint("\t\t\t\tSuccess (Posted): " + article['title'], "green")
                        total_success += 1
                    else:
                        # print(f"\t\t\t\tFailed: {article['title']} | {response_json}")
                        cprint(f"\t\t\t\tFailed: {article['title']} | {response_json}", "red")
                        total_failed += 1
                    total_posts += 1
                    cprint(
                        f"{len(articles) * len(category)} /  {total_posts} | Total: {len(articles) * len(category)} in {category_name} [Category] | Total {len(articles)} topics in {topic} [Sub-Category] | Success: {total_success} | Failed: {total_failed}",
                        "yellow")
                    print(
                        f"{category_name} [{topic}] : {'-' * 20}")

    except Exception as e:
        raise Exception(f"Error in get_news. {e}")


if __name__ == "__main__":
    get_news_step_1()
