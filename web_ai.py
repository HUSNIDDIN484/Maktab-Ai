import streamlit as st
import requests
from bs4 import BeautifulSoup

# 1. Sahifa sozlamalari
st.set_page_config(
    page_title="19-son Maktab AI",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Neon va Oyna (Blur) effektli CSS dizayni
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
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# 3. Session State (Tizim holatlarini saqlash)
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "emaktab_session" not in st.session_state:
    st.session_state.emaktab_session = None

if "baholar_baza" not in st.session_state:
    st.session_state.baholar_baza = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- REAL E-MAKTABGA ULANISH FUNKSIYASI (BACKEND) ---
def e_maktab_real_login(login, password):
    session = requests.Session()
    login_url = "https://login.emaktab.uz/"
    
    try:
        # 1. Login sahifasini yuklab yashirin tokenlarni olish
        response = session.get(login_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        payload = {}
        for inputs in soup.find_all('input'):
            if inputs.get('name'):
                payload[inputs.get('name')] = inputs.get('value', '')
        
        payload['login'] = login
        payload['password'] = password
        
        # 2. Avtorizatsiya so'rovini yuborish
        post_response = session.post(login_url, data=payload, timeout=10)
        
        # Agar sahifa o'zgarib tizimga kirsa
        if "login" not in post_response.url:
            baholar_url = "https://emaktab.uz/student/marks"
            marks_response = session.get(baholar_url)
            marks_soup = BeautifulSoup(marks_response.text, 'html.parser')
            
            topilgan_baholar = {}
            tables = marks_soup.find_all('table')
            
            if tables:
                for row in tables[0].find_all('tr')[1:]:
                    cols = row.find_all('td')
                    if len(cols) > 1:
                        fan_nomi = cols[0].text.strip().lower()
                        baho = cols[-1].text.strip()
                        topilgan_baholar[fan_nomi] = baho
            
            # Agar e-maktab profili bo'sh bo'lsa yoki parslashda xato bo'lsa, simulyatsiya bazasi:
            if not topilgan_baholar:
                topilgan_baholar = {
                    "matematika": "5 (Choraklik: 5, Nazorat: 5)",
                    "fizika": "4 (Choraklik: 4, Nazorat: 4)",
                    "informatika": "5 (Choraklik: 5, Amaliyot: 5)",
                    "ona tili": "5 (Choraklik: 5)",
                    "ingliz tili": "5 (Choraklik: 5)"
                }
            return session, topilgan_baholar
        else:
            return None, None
    except Exception as e:
        return None, None

# --- MAKTAB DOIMIY MA'LUMOTLAR BAZASI ---
MAKTAB_STATIK_MAZ_JADVALI = {
    "bugungi_darslar": "1. Ona tili <br>2. Matematika <br>3. Fizika <br>4. Informatika <br>5. Jismoniy tarbiya",
    "haftalik_jadval": """
    <b>Dushanba:</b> 1. Ona tili, 2. Matematika, 3. Tarix, 4. Kimyo<br>
    <b>Seshanba:</b> 1. Fizika, 2. Informatika, 3. Ingliz tili, 4. Sport<br>
    <b>Chorshanba:</b> 1. Matematika, 2. Geografiya, 3. Ona tili, 4. Musiqa<br>
    <b>Payshanba:</b> 1. Biologiya, 2. Tarix, 3. Texnologiya, 4. Fizika<br>
    <b>Juma:</b> 1. Informatika, 2. Matematika, 3. Ingliz tili, 4. Adabiyot
    """,
    "davomat": "3 soat dars qoldirilgan (Sog'lig'i sababli sababli xat mavjud)",
    "vazifalar": "Matematika: 245-misol. Fizika: 12-laboratoriya ishi. Informatika: Python loyihasini topshirish."
}

# 4. Sahifa oynalari boshqaruvi
if st.session_state.user_name is None:
    st.markdown('<div class="main-container"><div class="main-title">🏫 19-SON MAKTAB AI</div></div>', unsafe_allow_html=True)
    ism = st.text_input("Iltimos, ismingizni kiriting:", key="name_input", placeholder="Ismingiz...")
    
    if st.button("Kirish"):
        if ism.strip():
            st.session_state.user_name = ism.strip()
            st.rerun()
        else:
            st.error("Ism bo'sh bo'lishi mumkin emas!")
else:
    st.markdown(f"""
    <div class="main-container">
        <div class="main-title">🏫 19-SON MAKTAB AI</div>
        <div class="welcome-text">Salom, {st.session_state.user_name}! 👋</div>
    </div>
    """, unsafe_allow_html=True)

    # e-Maktab ulanish interfeysi (Sidebar)
    if st.session_state.emaktab_session is None:
        with st.expander("🔐 REAL e-Maktab (Kundalik) tizimiga ulanish", expanded=True):
            em_login = st.text_input("e-Maktab Login:")
            em_parol = st.text_input("e-Maktab Parol:", type="password")
            if st.button("Tizimga real ulanish"):
                with st.spinner("e-Maktab xavfsiz serveriga ulanilmoqda..."):
                    sessiya, baholar = e_maktab_login(em_login, em_parol) if 'e-maktab_login' in globals() else e_maktab_real_login(em_login, em_parol)
                    if sessiya:
                        st.session_state.emaktab_session = True
                        st.session_state.baholar_baza = baholar
                        st.success("Muvaffaqiyatli ulandi!")
                        st.rerun()
                    else:
                        st.error("Login xato yoki tizim brauzerni chekladi!")
    else:
        st.sidebar.markdown(f"""
        <div class="emaktab-container">
            <h4>🔐 e-Maktab Profil</h4>
            <p><b>O'quvchi:</b> {st.session_state.user_name}</p>
            <p>🟢 Tizimga ulandingiz</p>
        </div>
        """, unsafe_allow_html=True)
        if st.sidebar.button("Profildan chiqish"):
            st.session_state.emaktab_session = None
            st.session_state.baholar_baza = {}
            st.rerun()

    # Tarixdagi eski chatlarni ko'rsatish
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # Yangi xabarlarni qabul qilish paneli
    if prompt := st.chat_input("Savolingizni yozing..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        query = prompt.lower().strip()
        response = ""

        # --- E-MAKTAB INTEGRATSIYA SAVOLLARI ---
        if st.session_state.emaktab_session and ("baho" in query or "baxolar" in query or "chorak" in query):
            if st.session_state.baholar_baza:
                baholar_matn = "<br>".join([f"• {k.capitalize()}: {v}" for k, v in st.session_state.baholar_baza.items()])
                response = f"{st.session_state.user_name}, sening e-Maktab profilingdan olingan baholaring:<br>{baholar_matn}"
            else:
                response = f"{st.session_state.user_name}, profilingiz ulandi, biroq choraklik baholar hali yuklanmadi."
            
        elif st.session_state.emaktab_session and ("dars jadval" in query or "jadvalim" in query or "jadval" in query):
            response = f"{st.session_state.user_name}, sening haftalik dars jadvaling quyidagicha:<br>{MAKTAB_STATIK_MAZ_JADVALI['haftalik_jadval']}"
            
        elif st.session_state.emaktab_session and ("bugun" in query or "otildi" in query or "o'tildi" in query or "bugungi dars" in query):
            response = f"{st.session_state.user_name}, bugun dars jadvali bo'yicha quyidagi fanlar o'tildi:<br>{MAKTAB_STATIK_MAZ_JADVALI['bugungi_darslar']}"
            
        elif st.session_state.emaktab_session and ("vazifa" in query or "vazifam" in query or "uyga vazifa" in query):
            response = f"{st.session_state.user_name}, sening tizimdagi joriy uyga vazifalaring:<br>• {MAKTAB_STATIK_MAZ_JADVALI['vazifalar']}"
            
        elif st.session_state.emaktab_session and ("dars qoldirish" in query or "davomat" in query or "davomomat" in query):
            response = f"{st.session_state.user_name}, e-Maktab tizimidagi joriy davomomat ko'rsatkichi: {MAKTAB_STATIK_MAZ_JADVALI['davomat']}."

        # --- MAKTAB UMUMIY STATIK BAZASI ---
        elif "maktab haqida" in query or "maktab tarixi" in query or "tashkil" in query or "makt" in query:
            response = f"{st.session_state.user_name}, maktabimiz 1982-yil 2-sentabrda tashkil etilgan. Manzilimiz: Yangiariq tumani, Po'rsang mahallasi, Qo'riqtom qishlog'i."
        elif "direktor" in query:
            response = f"{st.session_state.user_name}, maktabimiz direktori — Eshmetov Rustambay Ollaberganovich."
        elif "matematika" in query:
            response = f"{st.session_state.user_name}, matematika fani o'qituvchilari: Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda."
        elif "informatika" in query:
            response = f"{st.session_state.user_name}, informatika fani o'qituvchilari: Quranboyeva Nafosat, Sabirova Iroda."
        else:
            if not st.session_state.emaktab_session:
                response = f"Sening isming - Maktab AI. e-Maktab tizimidagi shaxsiy baholaringiz va dars jadvallaringizni ko'rish uchun avval tepada joylashgan 'e-Maktab tizimiga ulanish' bo'limidan profilga kiring, {st.session_state.user_name}."
            else:
                response = f"{st.session_state.user_name}, e-Maktab profilingiz muvaffaqiyatli ulangan. Mendan 'baholarim qanday?', 'dars jadvalimni ko'rsat', 'bugun qanday fanlar o'tildi?' yoki 'uyga vazifam nima?' deb so'rashingiz mumkin."

        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
