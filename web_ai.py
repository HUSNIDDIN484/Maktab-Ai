import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import json
import os

# API Kalitini xavfsiz usulda st.secrets orqali o'qiymiz
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
BAZA_FAYLI = "elonlar_baza.json"

# --- BAZA BILAN ISHLASH FUNKSIYALARI ---
def elonni_bazaga_yoz(elon_matni):
    """E'lonni hamma ko'rishi uchun JSON faylga doimiy saqlaydi"""
    malumot = {"elon": elon_matni, "vaqt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    with open(BAZA_FAYLI, "w", encoding="utf-8") as f:
        json.dump(malumot, f, ensure_ascii=False, indent=4)

def elonni_bazadan_oqi():
    """Fayldan e'lonni o'qib oladi, agar fayl bo'lmasa None qaytaradi"""
    if os.path.exists(BAZA_FAYLI):
        try:
            with open(BAZA_FAYLI, "r", encoding="utf-8") as f:
                malumot = json.load(f)
                return malumot.get("elon", None)
        except Exception:
            return None
    return None
# ----------------------------------------

# Sahifa sozlamalari
st.set_page_config(
    page_title="19-son Maktab AI",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Fonli dizayn uchun CSS
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
    .stChatInputContainer {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
    }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

def bugungi_hafta_kuni():
    kunlar = {0: "Dushanba", 1: "Seshanba", 2: "Chorshanba", 3: "Payshanba", 4: "Juma", 5: "Shanba", 6: "Yakshanba"}
    return kunlar[datetime.now().weekday()]

# Tizim xotirasi (Session State)
if "user_name" not in st.session_state: st.session_state.user_name = None
if "user_role" not in st.session_state: st.session_state.user_role = None
if "teacher_subject" not in st.session_state: st.session_state.teacher_subject = None
if "excel_rows" not in st.session_state: st.session_state.excel_rows = None
if "messages" not in st.session_state: st.session_state.messages = []

# Kirish oynasi
if st.session_state.user_name is None:
    st.markdown('<div class="main-container"><div class="main-title">🏫 19-SON MAKTAB AI</div></div>', unsafe_allow_html=True)
    ism = st.text_input("Iltimos, ismingizni kiriting:", placeholder="Ismingiz va familiyangiz...")
    rol = st.radio("Tizimga kirish turi:", ["O'quvchi", "O'qituvchi", "Kuzatuvchi"], index=0)
    
    fan = ""
    if rol == "O'qituvchi":
        fan = st.text_input("Dars beradigan fandingizni kiriting:", placeholder="Masalan: Matematika...")
        
    if st.button("Kirish"):
        if ism.strip():
            if rol == "O'qituvchi" and not fan.strip():
                st.error("O'qituvchi fandi majburiy!")
            else:
                st.session_state.user_name = ism.strip()
                st.session_state.user_role = rol
                if rol == "O'qituvchi": st.session_state.teacher_subject = fan.strip()
                st.rerun()
else:
    role_display = f"{st.session_state.user_role} ({st.session_state.teacher_subject})" if st.session_state.user_role == "O'qituvchi" else st.session_state.user_role
    st.markdown(f'<div class="main-container"><div class="main-title">🏫 19-SON MAKTAB AI</div><div class="welcome-text">Salom, {st.session_state.user_name}! 👋</div><div class="role-badge">Tizimda: {role_display}</div></div>', unsafe_allow_html=True)

    if st.sidebar.button("Tizimdan chiqish"):
        st.session_state.user_name = None; st.session_state.user_role = None; st.session_state.teacher_subject = None
        st.session_state.messages = []
        st.rerun()

    # O'quvchi uchun Excel yuklash paneli
    if st.session_state.user_role == "O'quvchi":
        if st.session_state.excel_rows is None:
            with st.expander("📊 REAL e-Maktab Excel faylini yuklash", expanded=True):
                uploaded_file = st.file_uploader("Excel faylni tanlang (.xlsx)", type=["xlsx"])
                if uploaded_file is not None:
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
                        saqlangan_qatorlar.append(" | ".join(elementlar))
                    st.session_state.excel_rows = saqlangan_qatorlar
                    st.success("Excel o'qildi!")
                    st.rerun()
    
    # O'qituvchi paneli
    elif st.session_state.user_role == "O'qituvchi":
        with st.expander("📝 O'qituvchining tezkor boshqaruv paneli", expanded=True):
            joriy_elon = elonni_bazadan_oqi()
            elon_matni = st.text_area("Bugungi dars yuzasidan e'lon yoki vazifa:", value=joriy_elon if joriy_elon else "")
            if st.button("E'lonni saqlash"):
                yangi_elon_formati = f"<b>{st.session_state.user_name} ({st.session_state.teacher_subject}):</b> {elon_matni.strip()}"
                elonni_bazaga_yoz(yangi_elon_formati)
                st.success("E'lon hammaga ko'rinadigan qilib bazaga saqlandi!")

    # Chat tarixini chiqarish
    for message in st.session_state.messages:
        with st.chat_message(message
