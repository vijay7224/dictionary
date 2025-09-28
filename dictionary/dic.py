import streamlit as st
import requests
from googletrans import Translator
translator = Translator()
def login():
    st.title("🔐 Login Page")
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def get_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
        return meaning
    else:
        return " Word not found in dictionary."

def dictionary_app():
   if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

   if not st.session_state["logged_in"]:
        login()
   else:
        st.title("📚 Dictionary app")
        word=st.text_input("Ente word:")
        mpp=get_meaning(word)
        if st.button("Get Meaning"):
            st.success(f"Meaning: {mpp}")
            hin=translator.translate(mpp, src="en", dest="hi")
            st.info(f"Meaning in Hindi: {hin.text}")

if __name__ == "__main__":
    dictionary_app()
