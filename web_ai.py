import streamlit as st
from streamlit_google_auth import Authenticate

# 1. Sahifa sozlamalari (Buni eng tepada yozish shart)
st.set_page_config(page_title="19-son Maktab AI", page_icon="🤖")

# 2. Google Auth sozlamalarini secrets.toml dan yuklash
auth = Authenticate(
    secret_credentials_path=None, 
    cookie_name='maktab_ai_auth',
    cookie_key=st.secrets["auth"]["cookie_secret"],
    client_id=st.secrets["auth"]["client_id"],
    client_secret=st.secrets["auth"]["client_secret"],
    redirect_uri=st.secrets["auth"]["redirect_uri"],
)

# 3. Foydalanuvchi holatini tekshirish
auth.check_authenticity()

# 4. Agar foydalanuvchi kirmagan bo'lsa
if not st.session_state.get('connected'):
    st.markdown("<h1 style='text-align: center;'>19-son Maktab AI</h1>", unsafe_allow_html=True)
    st.info("Tizimdan foydalanish uchun Google hisobingiz orqali kiring.")
    
    # Login tugmasi
    auth.login()
    st.stop()  # Pastdagi AI kodlarini ishga tushirishni to'xtatadi

# --- BU YERDAN KEYIN FAQAT TIZIMGA KIRGANLAR UCHUN ---

# Sidebar - Foydalanuvchi ma'lumotlari va Chiqish tugmasi
user_info = st.session_state.get('user_info', {})
st.sidebar.image(user_info.get('picture'), width=100)
st.sidebar.write(f"Siz kirdingiz: **{user_info.get('name')}**")

if st.sidebar.button("Tizimdan chiqish"):
    auth.logout()
    st.rerun()

# --- SIZNING ASOSIY AI KODINGIZ ---
st.title("🤖 Maktab AI Yordamchisi")

# Masalan, Chat qismi:
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Savolingizni yozing..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = "Assalomu alaykum! Men 19-son maktab AI yordamchisiman. Hozircha login tizimini test qilyapmiz."
        st.markdown(response)
