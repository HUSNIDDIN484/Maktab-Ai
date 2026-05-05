import streamlit as st
from streamlit_google_auth import Authenticate
import g4f

# Sahifa sozlamalari
st.set_page_config(page_title="19-son Maktab AI", page_icon="🤖", layout="centered")

# Avtentifikatsiya (image_1d9f02.png xatosini tuzatish uchun 2.0.0 versiya standarti)
auth = Authenticate(
    cookie_name="maktab_ai_session",
    cookie_key=st.secrets["auth"]["cookie_secret"],
    client_id=st.secrets["auth"]["client_id"],
    client_secret=st.secrets["auth"]["client_secret"],
    redirect_uri="https://maktab-ai.streamlit.app/oauth2callback"
)

# Login holatini tekshirish
auth.check_authenticity()

if st.session_state.get("connected"):
    # Sidebar: Foydalanuvchi ma'lumotlari
    st.sidebar.success(f"Tizimga kirdingiz: {st.session_state.get('name')}")
    if st.sidebar.button("Chiqish"):
        auth.logout()

    # Asosiy chat interfeysi
    st.title("🤖 19-son Maktab AI")
    st.info("Savolingizni yozing, men javob berishga tayyorman.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat tarixini ko'rsatish
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Foydalanuvchi savoli
    if prompt := st.chat_input("Masalan: O'zbekiston poytaxti qayer?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # AI javobini generatsiya qilish
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4,
                    messages=[{"role": "user", "content": prompt}],
                )
                if response:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("AI hozircha javob bera olmadi.")
            except Exception as e:
                st.error(f"Xatolik: {e}")
else:
    # Login oynasi
    st.title("🔐 Maktab AI - Kirish")
    st.write("Ilovadan foydalanish uchun Google hisobingiz orqali tizimga kirishingiz kerak.")
    auth.login()
