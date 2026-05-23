import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 1. Sahifa sozlamalari
st.set_page_config(
    page_title="19-son Maktab AI",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Yangilangan Maktab Kutubxonasi fonli CSS dizayni
css_style = """
<style>
    .stApp {
        background: linear-gradient(rgba(14, 17, 23, 0.75), rgba(14, 17, 23, 0.85)), 
                    url("https://images.unsplash.com/photo-1521587760476-6c12a4b040da?q=80&w=1920") no-repeat center center fixed;
        background-size: cover;
    }
    .main-container {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
        text-align: center;
    }
    .main-title { color: #ffffff; font-size: 38px; font-weight: 800; }
    .welcome-text { color: #00e5ff; font-size: 24px; font-weight: 600; }
    .role-badge {
        background: rgba(255, 255, 255, 0.1);
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        color: #e0e0e0;
        display: inline-block;
        margin-top: 5px;
    }
    .emaktab-container {
        background: rgba(0, 229, 255, 0.05);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin-top: 15px;
    }
    .stChatInputContainer {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
    }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# Hafta kunlarini o'zbekchaga o'girish funksiyasi
def bugungi_hafta_kuni():
    kunlar = {
        0: "Dushanba", 1: "Seshanba", 2: "Chorshanba", 
        3: "Payshanba", 4: "Juma", 5: "Shanba", 6: "Yakshanba"
    }
    return kunlar[datetime.now().weekday()]

# 3. Session State (Tizim xotirasi)
if "user_name" not in st.session_state: st.session_state.user_name = None
if "user_role" not in st.session_state: st.session_state.user_role = None
if "excel_rows" not in st.session_state: st.session_state.excel_rows = None
if "messages" not in st.session_state: st.session_state.messages = []

# 4. Kirish oynasi
if st.session_state.user_name is None:
    st.markdown('<div class="main-container"><div class="main-title">🏫 19-SON MAKTAB AI</div></div>', unsafe_allow_html=True)
    
    ism = st.text_input("Iltimos, ismingizni kiriting:", key="name_input", placeholder="Ismingiz...")
    rol = st.radio("Tizimga kirish turi:", ["O'quvchi", "Kuzatuvchi"], index=0)
    
    if st.button("Kirish"):
        if ism.strip():
            st.session_state.user_name = ism.strip()
            st.session_state.user_role = rol
            st.rerun()
        else:
            st.error("Ism bo'sh bo'lishi mumkin emas!")
else:
    # Asosiy oyna sarlavhasi
    st.markdown(
        f'<div class="main-container">'
        f'<div class="main-title">🏫 19-SON MAKTAB AI</div>'
        f'<div class="welcome-text">Salom, {st.session_state.user_name}! 👋</div>'
        f'<div class="role-badge">Tizimda: {st.session_state.user_role}</div>'
        f'</div>', 
        unsafe_allow_html=True
    )

    # 5. O'quvchi roli uchun Excel yuklash bo'limi
    if st.session_state.user_role == "O'quvchi":
        if st.session_state.excel_rows is None:
            with st.expander("📊 REAL e-Maktab Excel faylini yuklash", expanded=True):
                uploaded_file = st.file_uploader("Excel faylni tanlang (.xlsx)", type=["xlsx"])
                
                if uploaded_file is not None:
                    with st.spinner("Excel tahlil qilinmoqda..."):
                        try:
                            df = pd.read_excel(uploaded_file)
                            saqlangan_qatorlar = []
                            
                            for index, row in df.iterrows():
                                elementlar = []
                                for k, v in row.items():
                                    if pd.notna(v):
                                        v_str = str(v).strip()
                                        if "Unnamed: 1" in str(k): k_name = "Fan"
                                        elif "Unnamed: 2" in str(k): k_name = "Baho"
                                        elif "Unnamed: 3" in str(k): k_name = "Vazifa"
                                        else: k_name = str(k).replace("Дневник", "Ma'lumot")
                                        
                                        elementlar.append(f"<b>{k_name}:</b> {v_str}")
                                        
                                qator_matni = " | ".join(elementlar)
                                saqlangan_qatorlar.append(qator_matni)
                            
                            st.session_state.excel_rows = saqlangan_qatorlar
                            st.success("Excel muvaffaqiyatli o'qildi!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Xatolik: {e}")
    else:
        st.sidebar.markdown(f'<div class="emaktab-container"><h4>🟢 Kuzatuv rejimi</h4><p>Foydalanuvchi: {st.session_state.user_name}</p></div>', unsafe_allow_html=True)

    # Chat tarixini ko'rsatish
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # Savol-javob paneli
    if prompt := st.chat_input("Savolingizni yozing..."):
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Kiruvchi so'rovni tozalash va harflarni normallashtirish
        query = prompt.lower().strip().replace("‘", "'").replace("`", "'").replace("o‘", "o'")
        response = ""
        
        # O'quvchi uchun haftalik kunlarni aniqlash mantiqi
        maqsad_kun = None
        hafta_kunlari = ["dushanba", "seshanba", "chorshanba", "payshanba", "juma", "shanba", "yakshanba"]
        
        for kun in hafta_kunlari:
            if kun in query:
                maqsad_kun = kun.capitalize()
                break
        
        if maqsad_kun is None and ("bugun" in query or "darslarim" in query or "darsni" in query):
            maqsad_kun = bugungi_hafta_kuni()

        # --- JAVOB BERISH TIPI ---
        
        # 1. O'quvchi roli uchun e-Maktab ma'lumotlari filtrlanishi
        if st.session_state.user_role == "O'quvchi" and st.session_state.excel_rows is not None and maqsad_kun is not None:
            topilgan_darslar = []
            kun_topildi = False
            
            for qator in st.session_state.excel_rows:
                if f"fan: {maqsad_kun.lower()}" in qator.lower() or f"<b>fan:</b> {maqsad_kun.lower()}" in qator.lower():
                    kun_topildi = True
                    topilgan_darslar.append(qator)
                    continue
                
                if kun_topildi:
                    boshqa_kun_bormi = False
                    for k in hafta_kunlari:
                        if k != maqsad_kun.lower() and (f"fan: {k}" in qator.lower() or f"<b>fan:</b> {k}" in qator.lower()):
                            boshqa_kun_bormi = True
                            break
                    if boshqa_kun_b
