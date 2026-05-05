import streamlit as st
from streamlit_google_auth import Authenticate
import g4f

# Sahifa sozlamalari
st.set_page_config(page_title="19-son Maktab AI", page_icon="🤖")

# Avtentifikatsiya sozlamalari
# Rasmda (image_1f7f99.png) ko'ringan xatolikni oldini olish uchun manzillarni aniq yozamiz
auth = Authenticate(
    secret_credentials_path=None,
    cookie_secret=st.secrets["auth"]["cookie_secret"],
    client_id=st.secrets["auth"]["client_id"],
    client_secret=st.secrets["auth"]["client_secret"],
    redirect_uri="https://maktab-ai.streamlit.app/oauth2callback",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration"
)

# Tizimga kirishni tekshirish
auth.check_authenticity()

if st.session_state["connected"]:
    # Sidebar qismi
    st.sidebar.image("https://raw.githubusercontent.com/husniddin484/maktab-ai/main/logo.png", width=100)
    st.sidebar.write(f"Xush kelibsiz, {st.session_state['name']}!")
    
    if st.sidebar.button("Chiqish"):
        auth.logout()

    # Asosiy interfeys
    st.title("🤖 19-son Maktab AI")
    st.info("Yangiariq tumani, 19-son maktab yordamchisi.")

    # Chat xotirasi
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Avvalgi xabarlarni chiqarish
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Foydalanuvchi savoli
    if prompt := st.chat_input("Savolingizni yozing..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI javobi (g4f orqali)
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
    st.warning("Ilovadan foydalanish uchun Google hisobingiz orqali tizimga kiring.")
    auth.login()
