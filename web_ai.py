import streamlit as st
from streamlit_google_auth import Authenticate
import g4f

# Sahifa sozlamalari
st.set_page_config(page_title="19-son Maktab AI", page_icon="🤖")

# Avtentifikatsiya sozlamalari
# Secrets-dan ma'lumotlarni xavfsiz o'qiymiz
auth = Authenticate(
    secret_credentials_path=None,
    cookie_secret=st.secrets["auth"]["cookie_secret"],
    client_id=st.secrets["auth"]["client_id"],
    client_secret=st.secrets["auth"]["client_secret"],
    # Xatolikni oldini olish uchun manzilni qo'lda yozamiz
    redirect_uri="https://maktab-ai.streamlit.app/oauth2callback",
    server_metadata_url=st.secrets["auth"]["server_metadata_url"],
)

# Tizimga kirishni tekshirish
auth.check_authenticity()

if st.session_state["connected"]:
    # Tizimga kirgan foydalanuvchi uchun interfeys
    st.sidebar.image("https://raw.githubusercontent.com/husniddin484/maktab-ai/main/logo.png", width=100)
    st.sidebar.write(f"Xush kelibsiz, {st.session_state['name']}!")
    
    if st.sidebar.button("Chiqish"):
        auth.logout()

    st.title("🤖 19-son Maktab AI")
    st.info("Yangiariq tumani, 19-son maktabning maxsus sun'iy intellekt yordamchisi.")

    # Chat interfeysi
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
                st.error(f"Xatolik yuz berdi: {e}")

else:
    # Tizimga kirmagan foydalanuvchi uchun
    st.title("🔐 Kirish")
    st.warning("Ilovadan foydalanish uchun Google hisobingiz orqali tizimga kiring.")
    auth.login()
