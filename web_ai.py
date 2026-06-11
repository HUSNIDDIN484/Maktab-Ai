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
        st.session_state.user_name = None
        st.session_state.user_role = None
        st.session_state.teacher_subject = None
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

    # Chat tarixini chiqarish (TUZATILGAN QISM)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # Savol yuborilganda
    if prompt := st.chat_input("Savolingizni yozing..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        query = prompt.lower().strip().replace("o‘", "o'").replace("x", "h")
        response = ""
        
        # Hafta kunlarini aniqlash
        hafta_kunlari = ["dushanba", "seshanba", "chorshanba", "payshanba", "juma", "shanba", "yakshanba"]
        maqsad_kun = next((kun.capitalize() for kun in hafta_kunlari if kun in query), None)
        if maqsad_kun is None and ("bugun" in query or "darslar" in query): 
            maqsad_kun = bugungi_hafta_kuni()

        # JSON bazadan e'lonlarni tekshirish
        if any(k in query for k in ["elon", "vazifa", "topshiriq", "oqituvchi eloni"]):
            baza_eloni = elonni_bazadan_oqi()
            if baza_eloni:
                response = f"📢 <b>O'qituvchilar tomonidan qoldirilgan faol e'lon:</b><br><br>{baza_eloni}"
            else:
                response = "Hozircha bazada hech qanday faol e'lon yoki vazifa mavjud emas."

        # 1. TAQIQLAR VA FILTRLAR
        elif st.session_state.user_role == "Kuzatuvchi" and any(k in query for k in ["dars", "baho", "kundalik", "excel"]):
            response = f"Uzr, {st.session_state.user_name}. Shaxsiy e-Maktab ma'lumotlarini ko'rish uchun tizimga <b>O'quvchi</b> bo'lib kirishingiz kerak."
        
        # 2. MAKTABNING MAXSUS MA'LUMOTLAR BAZASI
        elif any(k in query for k in ["direktor", "rahbar", "ma'muryat", "mamuryat", "o'rinbosar", "orinbosar", "administrator"]):
            response = (
                f"{st.session_state.user_name}, 19-sonli maktab ma'muryati tarkibi:<br><br>"
                f"• <b>Direktor:</b> Eshmetov Rustambay Ollaberganovich.<br>"
                f"• <b>Direktor o'rinbosarlari:</b> Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek.<br>"
                f"• <b>Administrator:</b> Sabirova Iroda Yarash qizi."
            )
        elif any(k in query for k in ["yaratgan", "muallif", "husniddin", "saparboyev"]):
            response = f"Meni Xorazm viloyati, Yangiariq tumani, 19-sonli maktabning 8-B sinf o'quvchisi <b>Saparboyev Husniddin</b> yaratgan!"
        elif any(k in query for k in ["o'qituvchi", "ustoz", "fanlar", "ro'yxat", "oqituvchi"]):
            response = (
                f"{st.session_state.user_name}, 19-sonli maktab o'qituvchilarining to'liq ro'yxati:<br><br>"
                f"• <b>Matematika:</b> Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda.<br>"
                f"• <b>Ona tili:</b> Avazova Risolat, Bobojonova Mushtariy, Jumaniyozova Sadoqat, Otajonova Sharofat, Xudoynazarova Nafosat.<br>"
                f"• <b>Ingliz tili:</b> Eshmurodova Ra'no, Farxodova Muxtaram, Qo'shoqova Gulasal, Rajabova Lobar, Raxmanova So'najon, Sadullayeva Durdona.<br>"
                f"• <b>Rus tili:</b> Bekmetova Shaxnoza, Bobojonova Komila, Saidova Saragul, Sobirova Nozima, Tillayeva Aziza, Yusupova Sanobar.<br>"
                f"• <b>Tarix:</b> Allanazarova Zumrad, Matqurbonova Shohina, Matchanova Zebo, Sobirova Gulposhsha.<br>"
                f"• <b>Fizika/Kimyo:</b> Aminova Mehriniso, Kurbonov Ollashukur, Razzaqova Kumushoy, Meylibayeva Aziza.<br>"
                f"• <b>Informatika:</b> Quranboyeva Nafosat, Sabirova Iroda.<br>"
                f"• <b>Boshlang'ich ta'lim:</b> Bobojonova Elmira, Maftuna, Jumanazarova Nargiza, Kenjayeva Iroda, Normatova Iqbol, Nurmetova Marhabo, Otajonova Sarvinoz, Quryozova Sanobar, Ro'ziboyeva Sarvinoz, Sadiqova Farida, Saidmatova Muattar, Saparmatova Sadoqat, Xo'jayeva Shahnoza.<br>"
                f"• <b>Sport:</b> Pirnnazarov Nurali, Ro'zmetova Muhtarama, Xudaynazarov Davronbek, Yusupova Zuhraxon.<br>"
                f"• <b>Musiqa/San'at:</b> O'razmetov O'tkir, Xusainov Sodiqjon, Otamuratov Rustam, Sobirova Maloxat.<br>"
                f"• <b>Texnologiya:</b> Boltayeva Zebo, Eshchanova Nodira, Matkarimova Intizor, Matyoqubova Xusniobod, Sobirov Ollayor."
            )
        elif any(k in query for k in ["maktab", "tarix", "tashkil", "manzil", "qayerda", "qishloq", "mahalla"]):
            response = (
                f"<b>19-sonli umumta'lim maktabi haqida ma'lumot:</b><br><br>"
                f"• <b>Tashkil etilgan vaqti:</b> Maktabimiz 1982-yil 2-sentabrda tashkil etilgan.<br>"
                f"• <b>Manzilimiz:</b> Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'i, Po'rsang mahallasi."
            )
        
        # 3. EXCEL MA'LUMOTLARINI QIDIRISH
        elif st.session_state.user_role == "O'quvchi" and st.session_state.excel_rows is not None and maqsad_kun is not None:
            topilgan = []
            flag = False
            for qator in st.session_state.excel_rows:
                if f"ma'lumot: {maqsad_kun.lower()}" in qator.lower() or f"fan: {maqsad_kun.lower()}" in qator.lower():
                    flag = True
                    topilgan.append(qator)
                    continue
                if flag and any(f"fan: {k}" in qator.lower() for k in hafta_kunlari): 
                    break
                if flag: 
                    topilgan.append(qator)
            response = f"<b>{maqsad_kun}</b> darslari:<br>" + "<br>".join(topilgan) if topilgan else "Darslar topilmadi."

        # 4. TO'G'RIDAN-TO'G'RI API SO'ROV (YANGILANGAN VA BARQAROR)
        else:
            if not GEMINI_API_KEY:
                response = "Xatolik: GEMINI_API_KEY topilmadi. Iltimos Secrets panelini tekshiring."
            else:
                tizim_shaxsiyati = (
                    f"Sen Xorazm viloyati, Yangiariq tumani, 19-sonli maktab uchun yaratilgan 'Maktab AI' yordamchisisan. "
                    f"Seni 8-B sinf o'quvchisi Saparboyev Husniddin yaratgan. Hozir senga foydalanuvchi {st.session_state.user_name} "
                    f"savol bermoqda. Unga do'stona, aniq va faqat o'zbek tilida javob ber. Savol quyidagicha: "
                )
                
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [{"text": tizim_shaxsiyati + prompt}]
                    }]
                }
                
                # Eng oxirgi APIv1/v1beta barqaror modellari qo'yilgan
                modellar = ["gemini-1.5-flash-latest", "gemini-1.5-pro-latest", "gemini-pro"]
                muvaffaqiyatli = False
                
                for model in modellar:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
                    try:
                        api_response = requests.post(url, headers=headers, json=payload)
                        res_json = api_response.json()
                        
                        if 'candidates' in res_json and res_json['candidates']:
                            response = res_json['candidates'][0]['content']['parts'][0]['text']
                            muvaffaqiyatli = True
                            break
                    except Exception:
                        continue
                
                if not muvaffaqiyatli:
                    response = "Uzr, Google AI serverlari bilan ulanish imkoni bo'lmadi. Iltimos keyinroq qayta urining."

        # Javobni ekranga chiqarish
        with st.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
