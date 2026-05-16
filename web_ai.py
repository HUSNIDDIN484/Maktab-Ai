import streamlit as st

# 1. Sahifa sozlamalari
st.set_page_config(
    page_title="19-son Maktab AI",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Yonsei binosi foni va oyna (Blur) dizayni
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
    .stChatInputContainer {
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
    }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# 3. Session State (Foydalanuvchi ma'lumotlari)
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []

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
    # --- 2-Oyna: Asosiy Chat interfeysi ---
    st.markdown(f"""
    <div class="main-container">
        <div class="main-title">🏫 19-SON MAKTAB AI</div>
        <div class="welcome-text">Salom, {st.session_state.user_name}! 👋</div>
    </div>
    """, unsafe_allow_html=True)

    # Oldingi chat xabarlarini chiqarish
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat yozish paneli
    if prompt := st.chat_input("Savolingizni yozing..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # --- Ma'lumotlarni qidirish va tahlil qilish tizimi ---
        query = prompt.lower()
        response = ""

        # Rahbariyat va ma'muriyat bo'yicha qidiruv
        if "direktor" in query:
            response = f"{st.session_state.user_name}, maktabimiz direktori — Eshmetov Rustambay Ollaberganovich."
        elif "o'rinbosar" in query or "zavuch" in query or "ma'naviyat" in query:
            response = f"{st.session_state.user_name}, maktab direktor o'rinbosarlari: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek."
        elif "administrator" in query or "admin" in query:
            response = f"{st.session_state.user_name}, maktab administratorimiz: Sabirova Iroda Yarash qizi."
        
        # Fan o'qituvchilari bo'yicha qidiruv
        elif "matematika" in query:
            response = f"{st.session_state.user_name}, matematika fani o'qituvchilari: Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda."
        elif "ona tili" in query or "adabiyot" in query:
            response = f"{st.session_state.user_name}, ona tili va adabiyot fani o'qituvchilari: Avazova Risolat, Bobojonova Mushtariy, Jumaniyozova Sadoqat, Otajonova Sharofat, Xudoynazarova Nafosat."
        elif "ingliz tili" in query or "ingliz" in query or "english" in query:
            response = f"{st.session_state.user_name}, ingliz tili fani o'qituvchilari: Eshmurodova Ra'no, Farxodova Muxtaram, Qo'shoqova Gulasal, Rajabova Lobar, Raxmanova So'najon, Sadullayeva Durdona."
        elif "rus tili" in query or "rus" in query:
            response = f"{st.session_state.user_name}, rus tili fani o'qituvchilari: Bekmetova Shaxnoza, Bobojonova Komila, Saidova Saragul, Sobirova Nozima, Tillayeva Aziza, Yusupova Sanobar."
        elif "tarix" in query or "huquq" in query:
            response = f"{st.session_state.user_name}, tarix fani o'qituvchilari: Allanazarova Zumrad, Matqurbonova Shohina, Matchanova Zebo, Sobirova Gulposhsha."
        elif "fizika" in query or "kimyo" in query:
            response = f"{st.session_state.user_name}, fizika va kimyo fani o'qituvchilari: Aminova Mehriniso, Kurbonov Ollashukur, Razzaqova Kumushoy, Meylibayeva Aziza."
        elif "informatika" in query:
            response = f"{st.session_state.user_name}, informatika fani o'qituvchilari: Quranboyeva Nafosat, Sabirova Iroda."
        elif "boshlang'ich" in query or "sinf o'qituvchi" in query:
            response = f"{st.session_state.user_name}, boshlang'ich ta'lim o'qituvchilari: Bobojonova Elmira, Maftuna, Jumanazarova Nargiza, Kenjayeva Iroda, Normatova Iqbol, Nurmetova Marhabo, Otajonova Sarvinoz, Quryozova Sanobar, Ro'ziboyeva Sarvinoz, Sadiqova Farida, Saidmatova Muattar, Saparmatova Sadoqat, Xo'jayeva Shahnoza."
        elif "sport" in query or "jismoniy" in query or "fizra" in query:
            response = f"{st.session_state.user_name}, sport (jismoniy tarbiya) fani o'qituvchilari: Pirnnazarov Nurali, Ro'zmetova Muhtarama, Xudaynazarov Davronbek, Yusupova Zuhraxon."
        elif "musiqa" in query or "san'at" in query or "tasviriy" in query:
            response = f"{st.session_state.user_name}, musiqa va san'at fani o'qituvchilari: O'razmetov O'tkir, Xusainov Sodiqjon, Otamuratov Rustam, Sobirova Maloxat."
        elif "texnologiya" in query or "mehnat" in query:
            response = f"{st.session_state.user_name}, texnologiya fani o'qituvchilari: Boltayeva Zebo, Eshchanova Nodira, Matkarimova Intizor, Matyoqubova Xusniobod, Sobirov Ollayor."
        
        # Maktab tarixi va manzili bo'yicha qidiruv
        elif "tashkil" in query or "tarixi" in query or "qachon" in query:
            response = f"{st.session_state.user_name}, maktabimiz 1982-yil 2-sentabrda tashkil etilgan."
        elif "manzil" in query or "qayerda" in query or "joylashgan" in query:
            response = f"{st.session_state.user_name}, maktabimiz Xorazm viloyati, Yangiariq tumani, Po'rsang mahallasida joylashgan. Shuningdek, u Qo'riqtom qishlog'idagi 19-sonli maktab hisoblanadi."
        elif "yaratgan" in query or "muallif" in query or "kim yaratdi" in query:
            response = f"{st.session_state.user_name}, meni 8-B sinf o'quvchisi Saparboyev Husniddin va maktab jamoasi yaratgan."
            
        # Standart xushmuomalalik yoki umumiy savol
        else:
            response = f"Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan. Men faqat maktabimiz tarixi, ma'muriyati va o'qituvchilari haqidagi savollaringizga rasmiy, aniq hamda to'liq javob bera olaman, {st.session_state.user_name}."

        # AI javobini chiqarish va tarixga yozish
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
