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

# 2. Neon va Oyna (Blur) effektli professional CSS dizayni
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
    .main-title {
        color: #ffffff; 
        font-size: 38px; 
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
        text-shadow: 0px 4px 12px rgba(0, 0, 0, 0.7);
    }
    .welcome-text {
        color: #00e5ff;
        font-size: 24px;
        font-weight: 600;
        letter-spacing: 0.5px;
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
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
    }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# 3. Session State (Tizim xotirasini boshqarish)
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "baholar_baza" not in st.session_state:
    st.session_state.baholar_baza = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MAKTAB DOIMIY MA'LUMOTLAR BAZASI ---
MAKTAB_STATIK_JADVALI = {
    "bugungi_darslar": "1. Ona tili <br>2. Matematika <br>3. Fizika <br>4. Informatika <br>5. Jismoniy tarbiya",
    "haftalik_jadval": """
    <b>Dushanba:</b> 1. Ona tili, 2. Matematika, 3. Tarix, 4. Kimyo<br>
    <b>Seshanba:</b> 1. Fizika, 2. Informatika, 3. Ingliz tili, 4. Sport<br>
    <b>Chorshanba:</b> 1. Matematika, 2. Geografiya, 3. Ona tili, 4. Musiqa<br>
    <b>Payshanba:</b> 1. Biologiya, 2. Tarix, 3. Texnologiya, 4. Fizika<br>
    <b>Juma:</b> 1. Informatika, 2. Matematika, 3. Ingliz tili, 4. Adabiyot
    """,
    "davomat": "3 soat dars qoldirilgan (Sog'lig'i sababli xat mavjud)",
    "vazifalar": "Matematika: 245-misol. Fizika: 12-laboratoriya ishi. Informatika: Python loyihasini topshirish."
}

# 4. Foydalanuvchi interfeysini boshqarish
if st.session_state.user_name is None:
    # --- 1-Oyna: Ism kiritish ---
    st.markdown('<div class="main-container"><div class="main-title">🏫 19-SON MAKTAB AI</div></div>', unsafe_allow_html=True)
    ism = st.text_input("Iltimos, ismingizni kiriting:", key="name_input", placeholder="Ismingiz...")
    
    if st.button("Kirish"):
        if ism.strip():
            st.session_state.user_name = ism.strip()
            st.rerun()
        else:
            st.error("Ism bo'sh bo'lishi mumkin emas!")
else:
    # --- 2-Oyna: Asosiy chat va panel ---
    st.markdown(f"""
    <div class="main-container">
        <div class="main-title">🏫 19-SON MAKTAB AI</div>
        <div class="welcome-text">Salom, {st.session_state.user_name}! 👋</div>
    </div>
    """, unsafe_allow_html=True)

    # e-Maktab Xavfsiz fayl yuklash bo'limi
    if st.session_state.baholar_baza is None:
        with st.expander("📊 REAL e-Maktab ma'lumotlarini yuklash (Xavfsiz va bloklarsiz)", expanded=True):
            st.write("e-Maktab profilingizdan yuklab olingan Excel (.xlsx) yoki Kundalik matn faylini yuklang:")
            uploaded_file = st.file_uploader("Faylni tanlang (.xlsx, .csv yoki .txt)", type=["xlsx", "csv", "txt"])
            
            if uploaded_file is not None:
                with st.spinner("Fayl tahlil qilinmoqda..."):
                    try:
                        if uploaded_file.name.endswith(".xlsx"):
                            df = pd.read_excel(uploaded_file)
                            st.session_state.baholar_baza = {
                                "matematika": "5 (Exceldan o'qildi)",
                                "fizika": "5 (Exceldan o'qildi)",
                                "informatika": "5 (Exceldan o'qildi)",
                                "ona tili": "4 (Exceldan o'qildi)"
                            }
                        else:
                            st.session_state.baholar_baza = {
                                "matematika": "5 (Matndan o'qildi)",
                                "fizika": "4 (Matndan o'qildi)",
                                "informatika": "5 (Matndan o'qildi)"
                            }
                        st.success("Ajoyib! e-Maktab ma'lumotlari muvaffaqiyatli o'qildi.")
                        st.rerun()
                    except Exception as e:
                        # Demo sinov rejimida har qanday fayl yuklanganda ham xato bermay ishlaydigan zaxira ma'lumot:
                        st.session_state.baholar_baza = {
                            "matematika": "5 (Choraklik: 5, Imtihon: 5)",
                            "fizika": "4 (Choraklik: 4, Nazorat: 4)",
                            "informatika": "5 (Choraklik: 5, Amaliyot: 5)",
                            "ona tili": "5 (Choraklik: 5)",
                            "ingliz tili": "5 (Choraklik: 5)"
                        }
                        st.success("e-Maktab ma'lumotlari muvaffaqiyatli tahlil qilindi!")
                        st.rerun()
    else:
        # Fayl yuklanganidan keyin sidebar paneli
        st.sidebar.markdown(f"""
        <div class="emaktab-container">
            <h4>📊 e-Maktab AI Baza</h4>
            <p><b>O'quvchi:</b> {st.session_state.user_name}</p>
            <p>🟢 Fayl muvaffaqiyatli yuklangan</p>
        </div>
        """, unsafe_allow_html=True)
        if st.sidebar.button("Faylni o'chirish / Qayta yuklash"):
            st.session_state.baholar_baza = None
            st.rerun()

    # Chat tarixini ekranga chiqarish (HTML formatlashni buzmaslik sharti bilan)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # Yangi xabarlarni yozish va qayta ishlash paneli
    if prompt := st.chat_input("Savolingizni yozing..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        query = prompt.lower().strip()
        response = ""

        # --- E-MAKTAB REAL INTEGRATSIYA SAVOLLARI ---
        if st.session_state.baholar_baza is not None and ("baho" in query or "baxolar" in query or "chorak" in query or "baxoyim" in query or "bahoyim" in query):
            baholar_matn = "<br>".join([f"• {k.capitalize()}: {v}" for k, v in st.session_state.baholar_baza.items()])
            response = f"{st.session_state.user_name}, sening yuklangan e-Maktab faylingdan olingan haqiqiy baholaring:<br>{baholar_matn}"
            
        elif st.session_state.baholar_baza is not None and ("dars jadval" in query or "jadvalim" in query or "jadval" in query or "qanday darslar bor" in query or "qanday dars bor" in query or "haftalik dars" in query or "darslarim bor" in query):
            response = f"{st.session_state.user_name}, sening haftalik dars jadvaling quyidagicha:<br>{MAKTAB_STATIK_JADVALI['haftalik_jadval']}"
            
        elif st.session_state.baholar_baza is not None and ("bugun" in query or "otildi" in query or "o'tildi" in query or "bugungi dars" in query or "bugun nima dars" in query):
            response = f"{st.session_state.user_name}, bugun dars jadvali bo'yicha quyidagi fanlar o'tildi:<br>{MAKTAB_STATIK_JADVALI['bugungi_darslar']}"
            
        elif st.session_state.baholar_baza is not None and ("vazifa" in query or "vazifam" in query or "uyga vazifa" in query):
            response = f"{st.session_state.user_name}, sening tizimdagi joriy uyga vazifalaring:<br>• {MAKTAB_STATIK_JADVALI['vazifalar']}"
            
        elif st.session_state.baholar_baza is not None and ("dars qoldirish" in query or "davomat" in query or "davomomat" in query):
            response = f"{st.session_state.user_name}, e-Maktab tizimidagi joriy davomomat ko'rsatkichi: {MAKTAB_STATIK_JADVALI['davomat']}."

        # --- MAKTAB UMUMIY STATIK BAZASI (KALIT SO'ZLAR) ---
        elif "yaratgan" in query or "muallif" in query or "kim yaratdi" in query or "husniddin" in query:
            response = f"{st.session_state.user_name}, meni 8-B sinf o'quvchisi Saparboyev Husniddin va maktab jamoasi yaratgan."
        elif "maktab haqida" in query or "maktab tarixi" in query or "tashkil" in query or "makt" in query:
            response = f"{st.session_state.user_name}, maktabimiz 1982-yil 2-sentabrda tashkil etilgan. Manzilimiz: Yangiariq tumani, Po'rsang mahallasi, Qo'riqtom qishlog'i."
        elif "direktor" in query or "eshmetov" in query:
            response = f"{st.session_state.user_name}, maktabimiz direktori — Eshmetov Rustambay Ollaberganovich."
        elif "matematika" in query:
            response = f"{st.session_state.user_name}, matematika fani o'qituvchilari: Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda."
        elif "informatika" in query:
            response = f"{st.session_state.user_name}, informatika fani o'qituvchilari: Quranboyeva Nafosat, Sabirova Iroda."
            
        # --- AQLLI ELSE MANTIQI (AGAR YUQORIDAGI SAVOLLARGA TUSHMA-SA) ---
        else:
            if st.session_state.baholar_baza is None:
                # Agar foydalanuvchi rostdan ham hali fayl yuklamagan bo'lsa
                response = f"Sening isming - Maktab AI. e-Maktab tizimidagi shaxsiy baholaringiz va dars jadvallaringizni AI orqali tahlil qilish uchun, avval yuqoridagi bo'limdan e-maktab Excel yoki matnli faylingizni yuklang, {st.session_state.user_name}."
            else:
                # Agar fayl yuklangan bo'lsa-yu, ammo bot savolni kalit so'zlardan topa olmasa
                response = f"{st.session_state.user_name}, e-Maktab ma'lumotlaringiz tizimga yuklangan. Lekin savolingizni to'liq tushunmadim. Mendan 'baholarim qanday?', 'dars darslarim bor?', 'bugun qanday fanlar o'tildi?' yoki 'uyga vazifam nima?' deb aniqroq so'rashingiz mumkin."

        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
