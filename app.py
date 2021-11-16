import streamlit as st
import article_generator_rss
import nltk

nltk.download('punkt')


def main():
    db_user = st.secrets["db_user"]
    db_pass = st.secrets["db_pass"]
    db_host = st.secrets["db_host"]
    db_database = st.secrets["db_database"]
    secrets = st.secrets["secrets"]

    st.title('Article Generator')
    key = st.text_input("Secret Key")
    category = st.selectbox('category', ('mobile', 'pc', 'others', 'ai-ml', 'tech', 'gaming'))
    max_ = st.text_input('Count', 5)
    if max_ != 'all':
        max_ = int(max_)
    url_others = None
    if category == "others":
        url_others = st.text_input('url', 'Other RSS URl')

    if st.button("Generate"):
        if key != secrets:
            st.success("Invalid Key")
            print("Invalid Key")
        else:
            dict_of_url = {
                "mobile": "https://gadgets.ndtv.com/rss/android/feeds",
                "pc": "https://gadgets.ndtv.com/rss/laptops/feeds",
                "gaming": "https://gadgets.ndtv.com/rss/games/feeds",
                "tech": "https://gadgets.ndtv.com/rss/how-to/feeds",
                "ai-ml": "https://www.techrepublic.com/rssfeeds/topic/artificial-intelligence/",
                "others": url_others,
            }
            url = dict_of_url[category]
            msg = article_generator_rss.start(url=url, category=category, max=max_,
                                              db_user=db_user, db_pass=db_pass, db_host=db_host,
                                              db_database=db_database)
            st.success(msg)
            print(msg)


if __name__ == '__main__':
    main()
