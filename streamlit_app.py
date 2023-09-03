import streamlit as st
import newsapi


def main():
    secrets = st.secrets["secrets"]
    global BASE_URL, NLPCLOUD_TOKEN, TECHPORT_EMAIL, TECHPORT_PASSWORD, REWRITE
    BASE_URL = st.secrets["BASE_URL"]
    REWRITE = st.secrets["REWRITE"]
    NLPCLOUD_TOKEN = st.secrets["NLPCLOUD_TOKEN"]
    TECHPORT_EMAIL = st.secrets["TECHPORT_EMAIL"]
    TECHPORT_PASSWORD = st.secrets["TECHPORT_PASSWORD"]
    if REWRITE == "false":
        REWRITE = False

    st.title('Article Generator')
    key = st.text_input("Secret Key")

    if st.button("Generate"):
        if key != secrets:
            st.success("Invalid Key")
            print("Invalid Key")
        else:

            msg = newsapi.get_news_step_1(BASE_URL, NLPCLOUD_TOKEN, TECHPORT_EMAIL, TECHPORT_PASSWORD, REWRITE)
            st.success(msg)
            print(msg)


if __name__ == '__main__':
    main()
