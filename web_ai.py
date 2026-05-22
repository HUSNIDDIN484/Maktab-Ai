import streamlit as st
import pandas as pd
import io

# 1. Sahifa sozlamalari
st.set_page_config(
    page_title="19-son Maktab AI",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS Dizayn
css_style = """
<style>
    .stApp {
        background: linear-gradient(rgba(14, 17, 23, 0.7), rgba(14, 17, 23, 0.85)), 
                    url("https://images.unsplash.com/photo-1624200424564-94bc02bc9242?q=80&w=1920") no-repeat center center fixed;
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
    .emaktab-container {
        background: rgba(0, 229, 255, 0.05);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin-top: 15px;
    }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# 3. Session State
if "user_name" not in st.session_state: st.session_state.user_name = None
if "excel_matn" not in st.session_state: st.session_state.excel_matn = None
if "messages" not in st.session_state: st.session_state.messages = []

# Asosiy interfeys
if st.session_state.user_name is None:
    st.markdown('<div class="main-container"><div class="main-title">🏫 19-SON MAKTAB AI</div></div>', unsafe_allow_html=True)
    ism = st.text_input("Iltimos, ismingizni kiriting:", key="name_input")
    if st.button("Kirish"):
        if ism.strip():
            st.session_state.user_name = ism.strip()
            st.rerun()
else:
    st.markdown(f'<div class="main-container"><div class="main-title">🏫 19-SON MAKTAB AI</div><div class="welcome-text">Salom, {st.session_state.user_name}! 👋</div></div>', unsafe_allow_html=True)

    # Fayl yuklash bo'limi
    if st.session_state.excel_matn is None:
        with st.expander("📊 REAL e-Maktab Excel faylini yuklash", expanded=True):
            uploaded_file = st.file_uploader("Excel faylni tanlang (.xlsx)", type=["xlsx"])
            
            if uploaded_file is not None:
                with st.spinner("Excel tahlil qilinmoqda..."):
                    try:
                        # REAL PARSING: Excel ichidagi hamma matnni o'qiymiz
                        df = pd.read_excel(uploaded_file)
                        
                        # Excel jadvalini chiroyli matn ko'rinishiga o'giramiz
                        sarlavhalar = ", ".join([str(c) for c in df.columns])
                        namuna_satrlar = ""
                        for index, row in df.head(10).iterrows():
                            namuna_satrlar += f"<br>• " + ", ".join([f"<b>{k}:</b> {v}" for k, v in row.items() if pd.notna(v)])
                        
                        # Barcha o'qilgan ma'lumotni saqlaymiz
                        st.session_state.excel_matn = namuna_satrlar
                        st.success("Excel muvaffaqiyatli o'qildi!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Faylni o'qishda xatolik: {e}")
    else:
        st.sidebar.markdown(f'<div class="emaktab-container"><h4>🟢 Excel yuklangan</h4><p>O\'quvchi: {st.session_state.user_name}</p></div>', unsafe_allow_html=True)
        if st.sidebar.button("Faylni almashtirish"):
            st.session_state.excel_matn = None
            st.rerun()

    # Chat tarixi
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # Savol-javob paneli
    if prompt := st.chat_input("Savolingizni yozing..."):
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        query = prompt.lower().strip()
        response = ""

        # --- DINAMIK JAVOB BERISH MANTIQLARI ---
        if st.session_state.excel_matn and ("dars" in query or "baho" in query or "jadval" in query or "chorak" in query):
            response = f"{st.session_state.user_name}, sening yuklagan e-Maktab Excel fayling ichidan quyidagi real ma'lumotlar topildi:<br>{st.session_state.excel_matn}"
        
        elif "direktor" in query or "eshmetov" in query:
            response = f"{st.session_state.user_name}, maktabimiz direktori — Eshmetov Rustambay Ollaberganovich."
        elif "yaratgan" in query or "muallif" in query:
            response = f"Meni 8-B sinf o'quvchisi Saparboyev Husniddin va maktab jamoasi yaratgan."
        else:
            if st.session_state.excel_matn is None:
                response = f"e-Maktab ma'lumotlarini ko'rish uchun avval fayl yuklang."
            else:
                response = f"{st.session_state.user_name}, e-Maktab faylingiz tahlil qilingan. Mendan baholaringiz yoki darslaringiz haqida so'rang."

        with st.chat_message("assistant"): st.markdown(response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
