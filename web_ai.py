import streamlit as st
import g4f

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫", layout="wide")

# --- FON (YONSEI UNIVERSITY) VA SHAFFOF DIZAYN ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                    url("https://images.unsplash.com/photo-1623690184496-6e5414d79201?q=80&w=2070&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }
    [data-testid="stHeader"], [data-testid="stAppViewBlockContainer"] {
        background-color: transparent !important;
    }
    .title { 
        color: white; text-align: center; font-size: 42px; font-weight: bold; 
        text-shadow: 2px 2px 12px rgba(0,0,0,0.9); padding: 20px;
    }
    .user-msg { 
        background-color: rgba(255, 255, 255, 0.1) !important; 
        padding: 15px; border-radius: 15px; margin: 10px 0; 
        border-right: 5px solid #3B8ED0; color: white; backdrop-filter: blur(12px);
    }
    .ai-msg { 
        background-color: rgba(255, 255, 255, 0.05) !important; 
        padding: 15px; border-radius: 15px; 
        border-left: 5px solid #3B8ED0; margin: 10px 0; color: white; backdrop-filter: blur(12px);
    }
    .login-box {
        background: rgba(0, 0, 0, 0.7);
        padding: 40px;
        border-radius: 25px;
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        max-width: 500px;
        margin: 100px auto;
        backdrop-filter: blur(10px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- XOTIRA VA ISMNI BOSHQARISH ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_name" not in st.session_state:
    st.session_state.user_name = None

# --- 1. KIRISH OYNASI ---
if st.session_state.user_name is None:
    st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:white;'>Xush kelibsiz!</h3>", unsafe_allow_html=True)
    name = st.text_input("Suhbatni boshlash uchun ismingizni kiriting:", key="login_name")
    if st.button("Kirish"):
        if name.strip():
            st.session_state.user_name = name.strip()
            st.rerun()
        else:
            st.error("Iltimos, ismingizni yozing!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 2. CHAT OYNASI ---
else:
    st.markdown(f'<p class="title">Salom, {st.session_state.user_name}! 👋</p>', unsafe_allow_html=True)

    def get_ai_response(prompt):
        system_instructions = (
            f"Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan. "
            f"Seni 8-B sinf o'quvchisi Saparboyev Husniddin va maktab jamoasi yaratgan. "
            f"Hozirgi foydalanuvchi: {st.session_state.user_name}. Har doim unga ismi bilan murojaat qil. "
            "DIQQAT: Google haqida gapirma. Rasmiy va aniq tilda javob ber. "
            
            "\n\n--- MA'MURIYAT ---"
            "\nDirektor: Eshmetov Rustambay Ollaberganovich. O'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek. Administrator: Sabirova Iroda Yarash qizi."
            
            "\n\n--- O'QITUVCHILAR ---"
            "\nMatematika: Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda."
            "\nOna tili: Avazova Risolat, Bobojonova Mushtariy, Jumaniyozova Sadoqat, Otajonova Sharofat, Xudoynazarova Nafosat."
            "\nIngliz tili: Eshmurodova Ra'no, Farxodova Muxtaram, Qo'shoqova Gulasal, Rajabova Lobar, Raxmanova So'najon, Sadullayeva Durdona."
            "\nRus tili: Bekmetova Shaxnoza, Bobojonova Komila, Saidova Saragul, Sobirova Nozima, Tillayeva Aziza, Yusupova Sanobar."
            "\nTarix: Allanazarova Zumrad, Matqurbonova Shohina, Matchanova Zebo, Sobirova Gulposhsha."
            "\nFizika/Kimyo: Aminova Mehriniso, Kurbonov Ollashukur, Razzaqova Kumushoy, Meylibayeva Aziza."
            "\nInformatika: Quranboyeva Nafosat, Sabirova Iroda."
            "\nBoshlang'ich: Bobojonova Elmira, Maftuna, Jumanazarova Nargiza, Kenjayeva Iroda, Normatova Iqbol, Nurmetova Marhabo, Otajonova Sarvinoz, Quryozova Sanobar, Ro'ziboyeva Sarvinoz, Sadiqova Farida, Saidmatova Muattar, Saparmatova Sadoqat, Xo'jayeva Shahnoza."
            "\nSport: Pirnnazarov Nurali, Ro'zmetova Muhtarama, Xudaynazarov Davronbek, Yusupova Zuhraxon."
            "\nMusiqa: O'razmetov O'tkir, Xusainov Sodiqjon, Otamuratov Rustam, Sobirova Maloxat."
            "\nTexnologiya: Boltayeva Zebo, Eshchanova Nodira, Matkarimova Intizor, Matyoqubova Xusniobod, Sobirov Ollayor."
            
            "\n\nMaktab 1982-yilda ochilgan. Manzil: Yangiariq tumani, Po'rsang mahallasi."
        )

        chat_history = [{"role": "system", "content": system_instructions}]
        # Oxirgi 5 ta xabarni eslab qolish (Xotira)
        for msg in st.session_state.messages[-5:]:
            chat_history.append({"role": msg["role"], "content": msg["content"]})
        
        chat_history.append({"role": "user", "content": prompt})
        
        try:
            response = g4f.ChatCompletion.create(model=g4f.models.default, messages=chat_history)
            return str(response).replace("Google", "Maktab jamoasi")
        except:
            return f"{st.session_state.user_name}, ulanishda muammo bo'ldi. Qaytadan so'rab ko'ring."

    # Xabarlarni ko'rsatish
    for msg in st.session_state.messages:
        role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
        name_tag = st.session_state.user_name if msg["role"] == "user" else "Maktab AI"
        st.markdown(f'<div class="{role_class}"><b>{name_tag}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

    # Chat kiritish
    user_input = st.chat_input("Xabaringizni yozing...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("O'ylayapman..."):
            answer = get_ai_response(user_input)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
