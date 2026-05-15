import streamlit as st
import g4f

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫", layout="wide")

# --- KUCHAYTIRILGAN CSS (Qora fonni yo'qotish kafolati bilan) ---
st.markdown("""
    <style>
    /* 1. Asosiy fonni majburan o'zgartirish */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                    url("https://images.unsplash.com/photo-1623690184496-6e5414d79201?q=80&w=2070&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* 2. Standart barcha qora/oq qatlamlarni shaffof qilish */
    [data-testid="stHeader"], 
    [data-testid="stAppViewBlockContainer"], 
    .main, 
    .stChatMessage, 
    [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
        background: transparent !important;
    }

    /* 3. Sarlavha va matnlar */
    .title { 
        color: white !important; 
        text-align: center; 
        font-size: 45px; 
        font-weight: bold; 
        text-shadow: 4px 4px 20px rgba(0,0,0,1); 
        padding: 30px;
    }

    /* 4. Xabarlar dizayni (Shaffof va blurli) */
    .user-msg { 
        background-color: rgba(255, 255, 255, 0.1) !important; 
        padding: 15px; border-radius: 18px; margin: 10px 0; 
        border-right: 6px solid #3B8ED0; color: white !important; 
        backdrop-filter: blur(15px);
    }
    .ai-msg { 
        background-color: rgba(255, 255, 255, 0.03) !important; 
        padding: 15px; border-radius: 18px; 
        border-left: 6px solid #3B8ED0; margin: 10px 0; 
        color: white !important; 
        backdrop-filter: blur(15px);
    }

    /* 5. Kirish oynasi */
    .login-box {
        background: rgba(0, 0, 0, 0.75) !important;
        padding: 45px; border-radius: 30px; 
        border: 1px solid rgba(255,255,255,0.3);
        text-align: center; max-width: 500px; 
        margin: 100px auto; backdrop-filter: blur(20px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- XOTIRA VA ISM ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# --- 1. KIRISH QISMI ---
if st.session_state.user_name is None:
    st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h2 style='color:white;'>Xush kelibsiz!</h2>", unsafe_allow_html=True)
    name = st.text_input("Suhbatni boshlash uchun ismingizni kiriting:", key="login_field")
    if st.button("Kirish"):
        if name.strip():
            st.session_state.user_name = name.strip()
            st.rerun()
        else:
            st.warning("Iltimos, ismingizni yozing!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 2. CHAT QISMI ---
else:
    st.markdown(f'<p class="title">Salom, {st.session_state.user_name}!</p>', unsafe_allow_html=True)

    def get_ai_response(prompt):
        system_instructions = (
            f"Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan. "
            f"Seni 8-B sinf o'quvchisi Saparboyev Husniddin va maktab jamoasi yaratgan. "
            f"Foydalanuvchi: {st.session_state.user_name}. Har doim unga ismi bilan murojaat qil. "
            "Google haqida gapirma. Rasmiy, samimiy va aniq tilda javob ber."
            "\n\n--- MA'MURIYAT ---"
            "\nDirektor: Eshmetov Rustambay Ollaberganovich. O'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek. Administrator: Sabirova Iroda Yarash qizi."
            "\n\n--- O'QITUVCHILAR RO'YXATI ---"
            "\nMatematika: Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda."
            "\nOna tili: Avazova Risolat, Bobojonova Mushtariy, Jumaniyozova Sadoqat, Otajonova Sharofat, Xudoynazarova Nafosat."
            "\nIngliz tili: Eshmurodova Ra'no, Farxodova Muxtaram, Qo'shoqova Gulasal, Rajabova Lobar, Raxmanova So'najon, Sadullayeva Durdona."
            "\nRus tili: Bekmetova Shaxnoza, Bobojonova Komila, Saidova Saragul, Sobirova Nozima, Tillayeva Aziza, Yusupova Sanobar."
            "\nTarix: Allanazarova Zumrad, Matqurbonova Shohina, Matchanova Zebo, Sobirova Gulposhsha."
            "\nFizika/Kimyo: Aminova Mehriniso, Kurbonov Ollashukur, Razzaqova Kumushoy, Meylibayeva Aziza."
            "\nInformatika: Quranboyeva Nafosat, Sabirova Iroda."
            "\nBoshlang'ich ta'lim: Bobojonova Elmira, Maftuna, Jumanazarova Nargiza, Kenjayeva Iroda, Normatova Iqbol, Nurmetova Marhabo, Otajonova Sarvinoz, Quryozova Sanobar, Ro'ziboyeva Sarvinoz, Sadiqova Farida, Saidmatova Muattar, Saparmatova Sadoqat, Xo'jayeva Shahnoza."
            "\nSport: Pirnnazarov Nurali, Ro'zmetova Muhtarama, Xudaynazarov Davronbek, Yusupova Zuhraxon."
            "\nMusiqa/San'at: O'razmetov O'tkir, Xusainov Sodiqjon, Otamuratov Rustam, Sobirova Maloxat."
            "\nTexnologiya: Boltayeva Zebo, Eshchanova Nodira, Matkarimova Intizor, Matyoqubova Xusniobod, Sobirov Ollayor."
            "\n\nMaktab 1982-yilda tashkil etilgan. Manzil: Yangiariq tumani, Po'rsang mahallasi."
        )

        chat_context = [{"role": "system", "content": system_instructions}]
        for msg in st.session_state.messages[-5:]:
            chat_context.append({"role": msg["role"], "content": msg["content"]})
        chat_context.append({"role": "user", "content": prompt})
        
        try:
            response = g4f.ChatCompletion.create(model=g4f.models.default, messages=chat_context)
            return str(response).replace("Google", "Maktab jamoasi")
        except:
            return f"Kechirasiz {st.session_state.user_name}, aloqada uzilish bo'ldi."

    # Chat ko'rinishi
    for msg in st.session_state.messages:
        role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
        sender = st.session_state.user_name if msg["role"] == "user" else "Maktab AI"
        st.markdown(f'<div class="{role_class}"><b>{sender}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

    # Input
    user_input = st.chat_input("Savolingizni bu yerga yozing...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Javob yozilmoqda..."):
            answer = get_ai_response(user_input)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
