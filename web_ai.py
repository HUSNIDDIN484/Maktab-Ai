import streamlit as st
from streamlit_google_auth import Authenticate

# Sahifa sozlamalari
st.set_page_config(page_title="19-son Maktab AI", page_icon="🤖")

# Google Auth ni sozlash
auth = Authenticate(
    secret_credentials_path=None,
    cookie_name='maktab_ai_auth',
    cookie_key=st.secrets["auth"]["cookie_secret"],
    client_id=st.secrets["auth"]["client_id"],
    client_secret=st.secrets["auth"]["client_secret"],
    redirect_uri=st.secrets["auth"]["redirect_uri"],
)

# Avtomatik tekshirish
auth.check_authenticity()

# Login holatini tekshirish
if not st.session_state.get('connected'):
    st.markdown("<h1 style='text-align: center;'>19-son Maktab AI</h1>", unsafe_allow_html=True)
    st.warning("Ilovadan foydalanish uchun Google hisobingiz orqali kirishingiz shart.")
    auth.login()
    st.stop()

# --- TIZIMGA KIRILGANDA KO'RINADIGAN QISM ---
user = st.session_state.get('user_info', {})
st.sidebar.image(user.get('picture'), width=80)
st.sidebar.success(f"Salom, {user.get('name')}!")

if st.sidebar.button("Chiqish"):
    auth.logout()
    st.rerun()

# Asosiy AI qismi
st.title("🤖 Maktab AI Yordamchisi")
st.info("Siz muvaffaqiyatli tizimga kirdingiz. Endi savol berishingiz mumkin.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Qanday yordam bera olaman?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        res = "Men 19-son maktab uchun maxsus tayyorlangan AI yordamchisiman."
        st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})
