import streamlit as st
import article_generator_rss


def main():
    st.title('Article Generator')
    secrets = st.secrets["secrets"],
    key = st.text_input("Secret Key")
    category = st.selectbox('category', ('mobile', 'pc', 'others', 'ai-ml', 'tech', 'gaming'))
    max_ = st.text_input('Count', 'all')
    if max_ != 'all':
        max_ = int(max_)
    url_others = None
    if category == "others":
        url_others = st.text_input('url', 'Other RSS URl')

    if st.button("Generate"):
        # st.success(key)
        # st.success(secrets)
        # st.success(category)
        # st.success(max_)
        if key != secrets[0]:
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
            msg = article_generator_rss.start(url=url, category=category, max=max_)
            st.success(msg)
            print(msg)


if __name__ == '__main__':
    main()

