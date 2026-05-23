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

# 2. Maktab Kutubxonasi va Sinf xonasi fonli CSS dizayni
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
        
        # To'g'ri yozilgan hafta kunlari ro'yxati
        hafta_kunlari = ["dushanba", "seshanba", "chorshanba", "payshanba", "juma", "shanba", "yakshanba"]
        
        # O'quvchi uchun haftalik kunlarni aniqlash mantiqi
        maqsad_kun = None
        for kun in hafta_kunlari:
            if kun in query:
                maqsad_kun = kun.capitalize()
                break
        
        if maqsad_kun is None and ("bugun" in query or "darslarim" in query or "darsni" in query):
            maqsad_kun = bugungi_hafta_kuni()

        # --- JAVOB BERISH MANTIQI ---
        
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
                    if boshqa_kun_bormi:
                        break
                    if qator.strip():
                        topilgan_darslar.append(qator)
            
            if topilgan_darslar:
                darslar_html = "<br>".join([f"• {d}" for d in topilgan_darslar])
                response = f"{st.session_state.user_name}, siz so'ragan <b>{maqsad_kun}</b> kunidagi darslar jadvali:<br><br>{darslar_html}"
            else:
                response = f"{st.session_state.user_name}, afsuski Excel faylingizdan <b>{maqsad_kun}</b> kuniga doir darslar topilmadi."

        elif st.session_state.user_role == "O'quvchi" and st.session_state.excel_rows is not None and ("baho" in query or "baxolar" in query or "hamma" in query or "jadval" in query):
            hamma_matn = "<br>".join([f"• {d}" for d in st.session_state.excel_rows[:15]])
            response = f"{st.session_state.user_name}, sizning kundalik ma'lumotlaringiz:<br>{hamma_matn}"

        # 2. Kuzatuvchi shaxsiy darslarni so'raganda taqiq qo'yish
        elif st.session_state.user_role == "Kuzatuvchi" and ("dars" in query or "baho" in query or "kundalik" in query or "excel" in query):
            response = f"Uzr, {st.session_state.user_name}. Siz tizimga <b>Kuzatuvchi</b> bo'lib kirgansiz. Shaxsiy e-Maktab dars jadvali va baholarni ko'rish uchun tizimga <b>O'quvchi</b> bo'lib qayta kirishingiz kerak."

        # 3. RASMIY INTEGRATSIYA QILINGAN BAZA
        elif any(k in query for k in ["direktor", "rahbar", "ma'muryat", "mamuryat", "o'rinbosar", "orinbosar", "administrator"]):
            response = (
                f"{st.session_state.user_name}, 19-sonli maktab ma'muryati tarkibi:<br><br>"
                f"• <b>Direktor:</b> Eshmetov Rustambay Ollaberganovich.<br>"
                f"• <b>Direktor o'rinbosarlari:</b> Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek.<br>"
                f"• <b>Administrator:</b> Sabirova Iroda Yarash qizi."
            )
            
        elif any(k in query for k in ["yaratgan", "muallif", "husniddin", "saparboyev"]):
            response = (
                f"Sening isming - Maktab AI. Men Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisiman. "
                f"Meni 8-B sinf o'quvchisi <b>Saparboyev Husniddin</b> va maktab jamoasi yaratgan, {st.session_state.user_name}."
            )
            
        elif any(k in query for k in ["o'qituvchi", "oqituvchi", "ustoz", "kim o'tadi", "fanlar", "ro'yxat", "royxat", "malumotlari"]):
            response = (
                f"{st.session_state.user_name}, Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab o'qituvchilarining to'liq ro'yxati:<br><br>"
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
                f"{st.session_state.user_name}, 19-sonli maktabimiz 1982-yil 2-sentabrda tashkil etilgan. "
                f"Manzilimiz: Yangiariq tumani, Qo'riqtom qishlog'i, Po'rsang mahallasi."
            )
            
        else:
            if st.session_state.user_role == "O'quvchi" and st.session_state.excel_rows is None:
                response = f"{st.session_state.user_name}, shaxsiy e-Maktab ko'rsatkichlaringizni tahlil qilish uchun avval yuqoridan Excel faylingizni yuklang."
            else:
                response = f"{st.session_state.user_name}, men bilan maktab rahbariyati, o'qituvchilar va maktab tarixi haqida batafsil suhbatlashishingiz mumkin. Savolingizni beravering!"

        with st.chat_message("assistant"): st.markdown(response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
