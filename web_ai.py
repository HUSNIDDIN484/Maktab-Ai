import streamlit as st
from streamlit_google_auth import Authenticate
import g4f

# Sahifa sozlamalari
st.set_page_config(page_title="19-son Maktab AI", page_icon="🤖")

# Avtentifikatsiya (image_1e3528.png dagi xatoni tuzatish uchun)
auth = Authenticate(
    cookie_name="maktab_ai_auth",
    cookie_key=st.secrets["auth"]["cookie_secret"],
    client_id=st.secrets["auth"]["client_id"],
    client_secret=st.secrets["auth"]["client_secret"],
    redirect_uri="https://maktab-ai.streamlit.app/oauth2callback",
)

# Login holatini tekshirish
auth.check_authenticity()

if st.session_state.get("connected"):
    st.sidebar.image("https://raw.githubusercontent.com/husniddin484/maktab-ai/main/logo.png", width=100)
    st.sidebar.write(f"Foydalanuvchi: {st.session_state.get('name')}")
    
    if st.sidebar.button("Log out"):
        auth.logout()

    st.title("🤖 19-son Maktab AI")
    st.info("Xush kelibsiz! Savolingizni yozing.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Nima haqida gaplashamiz?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4,
                    messages=[{"role": "user", "content": prompt}],
                )
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Xatolik: {e}")
else:
    st.title("🔑 Kirish")
    auth.login()
