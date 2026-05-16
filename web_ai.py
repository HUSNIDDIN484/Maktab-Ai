import streamlit as st

# 1. Sahifa sozlamalari (Brauzer sarlavhasi va ikonki)
st.set_page_config(
    page_title="19-son Maktab AI",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS stillari (Sintaksis xatolarini oldini olish uchun matn ko'rinishida)
# Bu yerda siz xohlagan shaffoflik va zamonaviy dizayn elementlari kiritilgan
css_style = """
<style>
    /* Umumiy fon va matn sozlamalari */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Asosiy sarlavha stili */
    .main-title {
        color: #ffffff; 
        text-align: center; 
        font-size: 38px; 
        font-weight: bold;
        padding: 20px 0;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
    }
    
    /* Salomlashish matni stili */
    .welcome-text {
        color: #ffeb3b;
        text-align: center;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 30px;
    }

    /* Qidiruv/Kiritish oynasining pastki qismda chiroyli turishi uchun (ixtiyoriy) */
    .stChatInput {
        border-radius: 10px;
    }
</style>
"""

# CSS-ni sahifaga yuklash (Faqat xavfsiz unsafe_allow_html=True parametri bilan)
st.markdown(css_style, unsafe_allow_html=True)

# 3. Session State (Foydalanuvchi ma'lumotlarini saqlash)
# Foydalanuvchi ismini eslab qolish uchun o'zgaruvchini tekshiramiz
if "username" not in st.session_state:
    st.session_state.username = None

# 4. Dasturning mantiqiy qismi (Oynalar almashinuvi)
if st.session_state.username is None:
    # --- 1-Oyna: Ism so'rash oynasi ---
    st.markdown('<div class="main-title">🏫 19-SON MAKTAB AI</div>', unsafe_allow_html=True)
    
    # Ismni kiritish inputi
    ism = st.text_input("Iltimos, ismingizni kiriting:", key="name_input", placeholder="Ismingiz...")
    
    if st.button("Kirish"):
        if ism.strip():
            st.session_state.username = ism.strip()
            st.rerun() # Sahifani yangilab, chat oynasiga o'tish
        else:
            st.error("Ism bo'sh bo'lishi mumkin emas!")

else:
    # --- 2-Oyna: Asosiy Chat interfeysi ---
    # Sarlavha
    st.markdown('<div class="main-title">🏫 19-SON MAKTAB AI</div>', unsafe_allow_html=True)
    
    # Foydalanuvchini ismi bilan qutlash
    st.markdown(f'<div class="welcome-text">Salom, {st.session_state.username}! 👋</div>', unsafe_allow_html=True)

    # Chat xabarlari tarixi uchun konteyner (agar kerak bo'lsa)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Oldingi xabarlarni ekranga chiqarish
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Savol yozish paneli (Pastki qismda chiqadi)
    if prompt := st.chat_input("Savolingizni yozing..."):
        # Foydalanuvchi savolini ekranga chiqarish
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Bu yerga sun'iy intellekt javob berish mantiqini (Maktab AI modelini) ulashingiz mumkin
        response = f"Rahmat {st.session_state.username}, savolingiz qabul qilindi. Tez orada javob beraman!"
        
        # AI javobini ekranga chiqarish
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
