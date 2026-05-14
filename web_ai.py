import streamlit as st
import g4f

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫", layout="wide")

# --- FON VA INTERFEYS DIZAYNI ---
st.markdown("""
    <style>
    /* Asosiy fon */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                    url("https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=2132&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* Bloklarni shaffof qilish */
    [data-testid="stHeader"], [data-testid="stAppViewBlockContainer"] {
        background-color: transparent !important;
    }

    /* Sarlavha stili */
    .title { 
        color: white; text-align: center; font-size: 42px; font-weight: bold; 
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8); padding: 20px;
    }

    /* Xabarlar stili */
    .user-msg { 
        background-color: rgba(255, 255, 255, 0.1) !important; 
        padding: 15px; border-radius: 15px; margin: 10px 0; 
        border-right: 5px solid #3B8ED0; color: white; backdrop-filter: blur(8px);
    }
    .ai-msg { 
        background-color: rgba(0, 0, 0, 0.5) !important; 
        padding: 15px; border-radius: 15px; 
        border-left: 5px solid #3B8ED0; margin: 10px 0; color: white; backdrop-filter: blur(8px);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MAKTAB MA'LUMOTLAR BAZASI ---
def get_ai_response(prompt):
    # Tizim ko'rsatmalari: Google haqida gapirmaslik va imlo xatolarisiz javob berish
    system_instructions = (
       "Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan. "

"Seni 8-B sinf o'quvchisi Saparboyev Husniddin va maktab jamoasi yaratgan. "

"DIQQAT: Google haqida gapirma. Imlo xatolarisiz, rasmiy va aniq tilda javob ber. Ortiqcha gapirmasdan savolga to'liq javob ber."

"\n\n--- MA'MURIYAT ---"

"\nDirektor: Eshmetov Rustambay Ollaberganovich. O'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek. Administrator: Sabirova Iroda Yarash qizi."

"\n\n--- O'QITUVCHILAR RO'YXATI ---"

"\nMatematika: Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda."

"\nOna tili: Avazova Risolat, Bobojonova Mushtariy, Jumaniyozova Sadoqat, Otajonova Sharofat, Xudoynazarova Nafosat."

"\nIngliz tili: Eshmurodova Ra'no, Farxodova Muxtaram, Qo'shoqova Gulasal, Rajabova Lobar, Raxmanova So'najon, Sadullayeva Durdona."

"\nRus tili: Bekmetova Shaxnoza, Bobojonova Komila, Saidova Saragul, Sobirova Nozima, Tillayeva Aziza, Yusupova Sanobar."

"\nTarix: Allanazarova Zumrad, Matqurbonova Shohina, Matchanova Zebo, Sobirova Gulposhsha."

"\nFizika/Kimyo: Aminova Mehriniso, Kurbonov Ollashukur, Razzaqova Kumushoy, Meylibayeva Aziza."

"\nInformatika: Quranboyeva Nafosat,Sabirova Iroda."

"\nBoshlang'ich ta'lim: Bobojonova Elmira, Maftuna, Jumanazarova Nargiza, Kenjayeva Iroda, Normatova Iqbol, Nurmetova Marhabo, Otajonova Sarvinoz, Quryozova Sanobar, Ro'ziboyeva Sarvinoz, Sadiqova Farida, Saidmatova Muattar, Saparmatova Sadoqat, Xo'jayeva Shahnoza."

"\nSport: Pirnnazarov Nurali, Ro'zmetova Muhtarama, Xudaynazarov Davronbek, Yusupova Zuhraxon."

"\nMusiqa/San'at: O'razmetov O'tkir, Xusainov Sodiqjon, Otamuratov Rustam, Sobirova Maloxat."

"\nTexnologiya: Boltayeva Zebo, Eshchanova Nodira, Matkarimova Intizor, Matyoqubova Xusniobod, Sobirov Ollayor."

"\n\nMaktab 1982-yil 2-sentabrda tashkil etilgan. Manzil: Yangiariq tumani, Po'rsang mahallasi."

)

    
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "system", "content": system_instructions}, {"role": "user", "content": prompt}],
        )
        return str(response).replace("Google", "Maktab jamoasi")
    except:
        return "Tizim hozirda band, birozdan so'ng qayta urinib ko'ring."

# --- CHAT ---
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{"Siz" if msg["role"] == "user" else "Maktab AI"}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

user_input = st.chat_input("Savolingizni yozing...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Javob tayyorlanmoqda..."):
        answer = get_ai_response(user_input)
        st.session_state.messages.append({"role": "ai", "content": answer})
    st.rerun()
