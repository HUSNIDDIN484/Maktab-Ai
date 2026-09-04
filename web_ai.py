import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# API Kalitini xavfsiz usulda st.secrets orqali o'qiymiz
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

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
if "user_name" not in st.session_state: 
    st.session_state.user_name = None
if "user_role" not in st.session_state: 
    st.session_state.user_role = None
if "teacher_subject" not in st.session_state: 
    st.session_state.teacher_subject = None
if "excel_rows" not in st.session_state: 
    st.session_state.excel_rows = None
if "teacher_announcement" not in st.session_state: 
    st.session_state.teacher_announcement = None
if "messages" not in st.session_state: 
    st.session_state.messages = []

# Kirish oynasi
if st.session_state.user_name is None:
    st.markdown('<div class="main-container"><div class="main-title">🏫 19-SON MAKTAB AI</div></div>', unsafe_allow_html=True)
    ism = st.text_input("Iltimos, ismingizni kiriting:", placeholder="Ismingiz va familiyangiz...")
    rol = st.radio("Tizimga kirish turi:", ["O'quvchi", "O'qituvchi", "Kuzatuvchi"], index=0)
    
    fan = ""
    if rol == "O'qituvchi":
        fan = st.text_input("Dars beradigan faningizni kiriting:", placeholder="Masalan: Matematika...")
        
    if st.button("Kirish"):
        if ism.strip():
            if rol == "O'qituvchi" and not fan.strip():
                st.error("O'qituvchi fani majburiy!")
            else:
                st.session_state.user_name = ism.strip()
                st.session_state.user_role = rol
                if rol == "O'qituvchi": 
                    st.session_state.teacher_subject = fan.strip()
                st.rerun()
else:
    role_display = f"{st.session_state.user_role} ({st.session_state.teacher_subject})" if st.session_state.user_role == "O'qituvchi" else st.session_state.user_role
    st.markdown(f'<div class="main-container"><div class="main-title">🏫 19-SON MAKTAB AI</div><div class="welcome-text">Salom, {st.session_state.user_name}! 👋</div><div class="role-badge">Tizimda: {role_display}</div></div>', unsafe_allow_html=True)

    if st.sidebar.button("Tizimdan chiqish"):
        st.session_state.user_name = None
        st.session_state.user_role = None
        st.session_state.teacher_subject = None
        st.session_state.excel_rows = None
        st.session_state.teacher_announcement = None
        st.session_state.messages = []
        st.rerun()

    # O'quvchi uchun Excel yuklash paneli (To'g'rilangan universal parser)
    if st.session_state.user_role == "O'quvchi":
        if st.session_state.excel_rows is None:
            with st.expander("📊 REAL e-Maktab Excel faylini yuklash", expanded=True):
                uploaded_file = st.file_uploader("Excel faylni tanlang (.xlsx)", type=["xlsx"])
                if uploaded_file is not None:
                    df = pd.read_excel(uploaded_file)
                    saqlangan_qatorlar = []
                    
                    for index, row in df.iterrows():
                        qator_elementlari = [str(val).strip() for val in row.values if pd.notna(val)]
                        if qator_elementlari:
                            saqlangan_qatorlar.append(" | ".join(qator_elementlari))
                            
                    st.session_state.excel_rows = saqlangan_qatorlar
                    st.success("Excel muvaffaqiyatli o'qildi va saqlandi!")
                    st.rerun()
        else:
            st.info("📊 Excel faylingiz muvaffaqiyatli yuklangan. Endi darslar va baholaringiz haqida so'rashingiz mumkin.")

    # O'qituvchi paneli
    elif st.session_state.user_role == "O'qituvchi":
        with st.expander("📝 O'qituvchining tezkor boshqaruv paneli", expanded=True):
            elon_matni = st.text_area("Bugungi dars yuzasidan e'lon yoki vazifa:", value=st.session_state.teacher_announcement if st.session_state.teacher_announcement else "")
            if st.button("E'lonni saqlash"):
                st.session_state.teacher_announcement = elon_matni.strip()
                st.success("E'lon saqlandi!")

    # Chat tarixini chiqarish
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
        if maqsad_kun is None and any(k in query for k in ["bugun", "dars", "vazifa", "baho", "jadval"]): 
            maqsad_kun = bugungi_hafta_kuni()

        # 1. TAQIQLAR VA FILTRLAR
        if st.session_state.user_role == "Kuzatuvchi" and any(k in query for k in ["dars", "baho", "kundalik", "excel"]):
            response = f"Uzr, {st.session_state.user_name}. Shaxsiy e-Maktab ma'lumotlarini ko'rish uchun tizimga <b>O'quvchi</b> bo'lib kirishingiz kerak."
        elif st.session_state.user_role == "O'qituvchi" and any(k in query for k in ["mening vazifam", "e'lon", "elon"]):
            response = f"Siz qoldirgan e'lon:<br><i>\"{st.session_state.teacher_announcement}\"</i>" if st.session_state.teacher_announcement else "Hali e'lon qoldirmadingiz."
        
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
            ustozlar_bazasi = {
                "matematika": "Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda",
                "ona tili": "Avazova Risolat, Bobojonova Mushtariy, Jumaniyozova Sadoqat, Otajonova Sharofat, Xudoynazarova Nafosat",
                "ingliz": "Eshmurodova Ra'no, Farxodova Muxtaram, Qo'shoqova Gulasal, Rajabova Lobar, Raxmanova So'najon, Sadullayeva Durdona",
                "rus": "Bekmetova Shaxnoza, Bobojonova Komila, Saidova Saragul, Sobirova Nozima, Tillayeva Aziza, Yusupova Sanobar",
                "tarix": "Allanazarova Zumrad, Matqurbonova Shohina, Matchanova Zebo, Sobirova Gulposhsha",
                "fizika": "Aminova Mehriniso, Kurbonov Ollashukur, Razzaqova Kumushoy, Meylibayeva Aziza",
                "kimyo": "Aminova Mehriniso, Kurbonov Ollashukur, Razzaqova Kumushoy, Meylibayeva Aziza",
                "informatika": "Quranboyeva Nafosat, Sabirova Iroda",
                "boshlang'ich": "Bobojonova Elmira, Maftuna, Jumanazarova Nargiza, Kenjayeva Iroda, Normatova Iqbol, Nurmetova Marhabo, Otajonova Sarvinoz, Quryozova Sanobar, Ro'ziboyeva Sarvinoz, Sadiqova Farida, Saidmatova Muattar, Saparmatova Sadoqat, Xo'jayeva Shahnoza",
                "sport": "Pirnnazarov Nurali, Ro'zmetova Muhtarama, Xudaynazarov Davronbek, Yusupova Zuhraxon",
                "musiqa": "O'razmetov O'tkir, Xusainov Sodiqjon, Otamuratov Rustam, Sobirova Maloxat",
                "texnologiya": "Boltayeva Zebo, Eshchanova Nodira, Matkarimova Intizor, Matyoqubova Xusniobod, Sobirov Ollayor"
            }
            
            topilgan_fan = next((f for f in ustozlar_bazasi if f in query), None)
            
            if topilgan_fan:
                response = f"<b>19-sonli maktabning {topilgan_fan.capitalize()} fani o'qituvchilari:</b><br>{ustozlar_bazasi[topilgan_fan]}"
            else:
                response = (
                    f"{st.session_state.user_name}, 19-sonli maktab o'qituvchilarining to'liq ro'yxati:<br><br>"
                    f"• <b>Matematika:</b> {ustozlar_bazasi['matematika']}<br>"
                    f"• <b>Ona tili:</b> {ustozlar_bazasi['ona tili']}<br>"
                    f"• <b>Ingliz tili:</b> {ustozlar_bazasi['ingliz']}<br>"
                    f"• <b>Rus tili:</b> {ustozlar_bazasi['rus']}<br>"
                    f"• <b>Tarix:</b> {ustozlar_bazasi['tarix']}<br>"
                    f"• <b>Fizika/Kimyo:</b> {ustozlar_bazasi['fizika']}<br>"
                    f"• <b>Informatika:</b> {ustozlar_bazasi['informatika']}<br>"
                    f"• <b>Boshlang'ich ta'lim:</b> {ustozlar_bazasi['boshlang\'ich']}<br>"
                    f"• <b>Sport:</b> {ustozlar_bazasi['sport']}<br>"
                    f"• <b>Musiqa/San'at:</b> {ustozlar_bazasi['musiqa']}<br>"
                    f"• <b>Texnologiya:</b> {ustozlar_bazasi['texnologiya']}"
                )
        elif any(k in query for k in ["maktab", "tarix", "tashkil", "manzil", "qayerda", "qishloq", "mahalla"]):
            response = (
                f"<b>19-sonli umumta'lim maktabi haqida ma'lumot:</b><br><br>"
                f"• <b>Tashkil etilgan vaqti:</b> Maktabimiz 1982-yil 2-sentabrda tashkil etilgan.<br>"
                f"• <b>Manzilimiz:</b> Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'i, Po'rsang mahallasi."
            )
        
        # 3. EXCEL MA'LUMOTLARINI QIDIRISH (ANIQ VA AMALIY SEARCH)
        elif st.session_state.user_role == "O'quvchi" and st.session_state.excel_rows is not None:
            topilgan = []
            bugungi_sana = datetime.now().strftime("%d.%m.%Y")
            
            for qator in st.session_state.excel_rows:
                qator_lower = qator.lower()
                if bugungi_sana in qator or (maqsad_kun and maqsad_kun.lower() in qator_lower):
                    topilgan.append(qator)
            
            if topilgan:
                sarlavha = f"<b>{bugungi_sana} ({maqsad_kun or 'Bugun'})</b>"
                response = f"{sarlavha} darslaringiz va ma'lumotlaringiz:<br><br>• " + "<br>• ".join(topilgan)
            else:
                barcha_qatorlar = "<br>• ".join(st.session_state.excel_rows[:8])
                response = (
                    f"⚠️ <b>{bugungi_sana}</b> ({maqsad_kun or 'Bugun'}) uchun darslar topilmadi.<br><br>"
                    f"<b>Excel faylingizdagi dastlabki qatorlar:</b><br>• {barcha_qatorlar}"
                )

        # 4. TO'G'RIDAN-TO'G'RI API SO'ROV
        else:
            if not GEMINI_API_KEY:
                response = "⚠️ <b>Xatolik:</b> `GEMINI_API_KEY` topilmadi! Streamlit Dashboard -> Settings -> Secrets qismiga kalitni kiriting."
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
                
                modellar = ["gemini-2.0-flash", "gemini-2.5-flash"]
                muvaffaqiyatli = False
                oxirgi_xato = ""
                
                for model in modellar:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
                    try:
                        api_response = requests.post(url, headers=headers, json=payload, timeout=30)
                        res_json = api_response.json()
                        
                        if 'candidates' in res_json and res_json['candidates']:
                            response = res_json['candidates'][0]['content']['parts'][0]['text']
                            muvaffaqiyatli = True
                            break
                        elif 'error' in res_json:
                            oxirgi_xato = f"Model: {model} -> Kod: {res_json['error'].get('code')} -> Xabar: {res_json['error'].get('message')}"
                        else:
                            oxirgi_xato = f"Model: {model} -> Kutilmagan server formati."
                    except requests.exceptions.Timeout:
                        oxirgi_xato = f"Model: {model} -> Server javob berish muddati tugadi (Timeout)."
                    except Exception as e:
                        oxirgi_xato = f"Model: {model} -> Aloqa xatosi: {str(e)}"
                        continue
                
                if not muvaffaqiyatli:
                    response = f"🔴 <b>Google API Diagnostics:</b><br><code style='color:#ff1744; white-space: pre-wrap;'>{oxirgi_xato}</code>"

        # Javobni ekranga chiqarish
        with st.chat_message("assistant"): 
            st.markdown(response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
