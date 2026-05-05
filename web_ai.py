import streamlit as st
from streamlit_google_auth import Authenticate
import g4f

# Sahifa sozlamalari
st.set_page_config(page_title="19-son Maktab AI", page_icon="🤖")

# Avtentifikatsiya sozlamalari (1.1.8 versiyasi uchun moslangan)
auth = Authenticate(
    secret_credentials_path=None, # Loglarda ko'ringan xatolikni oldini olish uchun
    cookie_name="maktab_ai_auth",
    cookie_key=st.secrets["auth"]["cookie_secret"],
    client_id=st.secrets["auth"]["client_id"],
    client_secret=st.secrets["auth"]["client_secret"],
    redirect_uri="https://maktab-ai.streamlit.app/oauth2callback",
)

# Login holatini tekshirish
auth.check_authenticity()

if st.session_state.get("connected"):
    # Tizimga kirgan foydalanuvchi qismi
    st.sidebar.image("https://raw.githubusercontent.com/husniddin484/maktab-ai/main/logo.png", width=100)
    st.sidebar.write(f"Xush kelibsiz, {st.session_state.get('name')}!")
    
    if st.sidebar.button("Chiqish"):
        auth.logout()

    st.title("🤖 19-son Maktab AI")
    st.info("Yangiariq tumani, 19-son maktab yordamchisi.")

    # Chat xotirasi
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Savolingizni yozing..."):
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
    # Kirish oynasi
    st.title("🔐 Kirish")
    st.warning("Ilovadan foydalanish uchun Google orqali kiring.")
    auth.login()
