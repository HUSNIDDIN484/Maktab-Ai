import streamlit as st

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

# 3. Session State (Tizim holatlari)
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "emaktab_logged_in" not in st.session_state:
    st.session_state.emaktab_logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- O'QUVCHINING E-MAKTAB BAZASI (Simulyatsiya ma'lumotlari) ---
# Haqiqiy integratsiyada bu ma'lumotlar fayldan yoki fondagi brauzerdan o'qib olinadi
OQUVCHI_PROFILI = {
    "ism": "Saparboyev Husniddin",
    "sinf": "8-B sinfi",
    "charek_baholar": {
        "matematika": "5 (Choraklik: 5, Nazorat: 5)",
        "fizika": "4 (Choraklik: 4, Nazorat: 4)",
        "informatika": "5 (Choraklik: 5, Amaliyot: 5)",
        "ona tili": "5 (Choraklik: 5)",
        "ingliz tili": "5 (Choraklik: 5)"
    },
    "davomomat": "3 soat dars qoldirilgan (Soliqli sababli)",
    "vazifalar": "Matematika: 245-misol. Fizika: 12-laboratoriya ishi tayyorlash. Informatika: Python loyihasini yakunlash."
}

# 4. Ilova oynalari boshqaruvi
if st.session_state.user_name is None:
    # --- 1-Oyna: Ism so'rash oynasi ---
    st.markdown('<div class="main-container"><div class="main-title">🏫 19-SON MAKTAB AI</div></div>', unsafe_allow_html=True)
    ism = st.text_input("Iltimos, ismingizni kiriting:", key="name_input", placeholder="Ismingiz...")
    
    if st.button("Kirish"):
        if ism.strip():
            st.session_state.user_name = ism.strip()
            st.rerun()
        else:
            st.error("Ism bo'sh bo'lishi mumkin emas!")

else:
    # --- 2-Oyna: Asosiy Chat va e-Maktab paneli ---
    st.markdown(f"""
    <div class="main-container">
        <div class="main-title">🏫 19-SON MAKTAB AI</div>
        <div class="welcome-text">Salom, {st.session_state.user_name}! 👋</div>
    </div>
    """, unsafe_allow_html=True)

    # Yon panel (Sidebar) yoki Chat ustida e-Maktab tizimiga kirish oynasi
    if not st.session_state.emaktab_logged_in:
        with st.expander("🔐 e-Maktab (Kundalik) tizimiga ulanish", expanded=True):
            st.write("Profil ma'lumotlaringiz va baholaringizni AI orqali tahlil qilish uchun tizimga kiring:")
            emaktab_login = st.text_input("e-Maktab Login:")
            emaktab_parol = st.text_input("e-Maktab Parol:", type="password")
            
            if st.button("e-Maktabga ulanish"):
                if emaktab_login and emaktab_parol:
                    # Bu yerda kirish muvaffaqiyatli bo'lgani simulyatsiya qilinadi
                    st.session_state.emaktab_logged_in = True
                    st.success("e-Maktab profiliga muvaffaqiyatli ulandi! Endi baholaringiz va vazifalaringiz haqida so'rashingiz mumkin.")
                    st.rerun()
                else:
                    st.error("Login va parolni to'liq kiriting!")
    else:
        st.sidebar.markdown(f"""
        <div class="emaktab-container">
            <h4>🔐 e-Maktab Profil</h4>
            <p><b>O'quvchi:</b> {OQUVCHI_PROFILI['ism']}</p>
            <p><b>Sinf:</b> {OQUVCHI_PROFILI['sinf']}</p>
            <p>🟢 Tizimga ulangan</p>
        </div>
        """, unsafe_allow_html=True)
        if st.sidebar.button("Profildan chiqish"):
            st.session_state.emaktab_logged_in = False
            st.rerun()

    # Chat tarixini chiqarish
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat yozish paneli
    if prompt := st.chat_input("Savolingizni yozing..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        query = prompt.lower().strip()
        response = ""

        # --- E-MAKTAB PROFILI BILAN BOG'LIQ SAVOLLAR ---
        if st.session_state.emaktab_logged_in and ("baho" in query or "baxolar" in query or "chorak" in query):
            baholar_matn = "<br>".join([f"• {k.capitalize()}: {v}" for k, v in OQUVCHI_PROFILI["charek_baholar"].items()])
            response = f"{st.session_state.user_name}, sening e-Maktabdagi joriy baholaring quyidagicha:<br>{baholar_matn}"
            
        elif st.session_state.emaktab_logged_in and ("vazifa" in query or "vazifam" in query or "uyga vazifa" in query):
            response = f"{st.session_state.user_name}, sening ertangi uyga vazifalaring:<br>• {OQUVCHI_PROFILI['vazifalar']}"
            
        elif st.session_state.emaktab_logged_in and ("dars qoldirish" in query or "davomat" in query or "shpargalka" in query):
            response = f"{st.session_state.user_name}, e-Maktab tizimidagi davomomat ko'rsatkichi: {OQUVCHI_PROFILI['davomomat']}."

        # --- MAKTAB UMUMIY BAZASI (Eski shartlarimiz) ---
        elif "maktab haqida" in query or "maktab tarixi" in query or "tashkil" in query or "makt" in query:
            response = f"{st.session_state.user_name}, maktabimiz 1982-yil 2-sentabrda tashkil etilgan. Manzilimiz: Yangiariq tumani, Po'rsang mahallasi."
        elif "direktor" in query:
            response = f"{st.session_state.user_name}, maktabimiz direktori — Eshmetov Rustambay Ollaberganovich."
        elif "matematika" in query:
            response = f"{st.session_state.user_name}, matematika fani o'qituvchilari: Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda."
        elif "informatika" in query:
            response = f"{st.session_state.user_name}, informatika fani o'qituvchilari: Quranboyeva Nafosat, Sabirova Iroda."
        else:
            if not st.session_state.emaktab_logged_in:
                response = f"Sening isming - Maktab AI. e-Maktab tizimidagi shaxsiy baholaringizni ko'rish uchun avval tepada joylashgan 'e-Maktab tizimiga ulanish' bo'limidan profilga kiring, {st.session_state.user_name}."
            else:
                response = f"{st.session_state.user_name}, e-Maktab profilingiz muvaffaqiyatli ulangan. Mendan 'baholarim qanday?', 'uyga vazifam nima?' yoki 'davomomatimni ko'rsat' deb so'rashingiz mumkin."

        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
