import streamlit as st
import g4f

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫", layout="wide")

# --- FON RASMINI MAJBURIY YUKLASH FUNKSIYASI ---
def set_bg_image():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                        url("https://images.unsplash.com/photo-1541339907198-e08759dfc3ef?q=80&w=2070&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"], [data-testid="stAppViewBlockContainer"] {{
            background: transparent !important;
        }}
        .title {{ 
            color: white; text-align: center; font-size: 40px; font-weight: bold; 
            text-shadow: 2px 2px 8px #000000; padding: 25px;
        }}
        .user-msg {{ 
            background-color: rgba(255, 255, 255, 0.15); 
            padding: 15px; border-radius: 15px; margin: 10px 0; 
            border-right: 5px solid #3B8ED0; color: white; backdrop-filter: blur(10px);
        }}
        .ai-msg {{ 
            background-color: rgba(0, 0, 0, 0.6); 
            padding: 15px; border-radius: 15px; 
            border-left: 5px solid #3B8ED0; margin: 10px 0; color: white; backdrop-filter: blur(10px);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_image()

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- TO'LIQ MA'LUMOTLAR BAZASI ---
def get_ai_response(prompt):
    system_instructions = (
        "Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan. "
        "Seni 8-B sinf o'quvchisi Saparboyev Husniddin va maktab jamoasi yaratgan. "
        "DIQQAT: Google haqida gapirma. Imlo xatolarisiz, rasmiy va aniq tilda javob ber. "
        
        "\n\n--- MA'MURIYAT ---"
        "\nDirektor: Eshmetov Rustambay Ollaberganovich. "
        "\nO'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek. "
        "\nAdministrator: Sabirova Iroda Yarash qizi. "
        
        "\n\n--- O'QITUVCHILAR RO'YXATI ---"
        "\nMatematika: Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda. "
        "\nOna tili: Avazova Risolat, Bobojonova Mushtariy, Jumaniyozova Sadoqat, Otajonova Sharofat, Xudoynazarova Nafosat. "
        "\nIngliz tili: Eshmurodova Ra'no, Farxodova Muxtaram, Qo'shoqova Gulasal, Rajabova Lobar, Raxmanova So'najon, Sadullayeva Durdona. "
        "\nRus tili: Bekmetova Shaxnoza, Bobojonova Komila, Saidova Saragul, Sobirova Nozima, Tillayeva Aziza, Yusupova Sanobar. "
        "\nTarix: Allanazarova Zumrad, Matqurbonova Shohina, Matchanova Zebo, Sobirova Gulposhsha. "
        "\nFizika/Kimyo: Aminova Mehriniso, Kurbonov Ollashukur, Razzaqova Kumushoy, Meylibayeva Aziza. "
        "\nInformatika: Quranboyeva Nafosat. "
        "\nBoshlang'ich ta'lim: Bobojonova Elmira, Maftuna, Jumanazarova Nargiza, Kenjayeva Iroda, Normatova Iqbol, Nurmetova Marhabo, Otajonova Sarvinoz, Quryozova Sanobar, Ro'ziboyeva Sarvinoz, Sadiqova Farida, Saidmatova Muattar, Saparmatova Sadoqat, Xo'jayeva Shahnoza. "
        "\nSport: Pirnnazarov Nurali, Ro'zmetova Muhtarama, Xudaynazarov Davronbek, Yusupova Zuhraxon. "
        "\nMusiqa/San'at: O'razmetov O'tkir, Xusainov Sodiqjon, Otamuratov Rustam, Sobirova Maloxat. "
        "\nTexnologiya: Boltayeva Zebo, Eshchanova Nodira, Matkarimova Intizor, Matyoqubova Xusniobod, Sobirov Ollayor. "
        
        "\n\nMaktab 1982-yil 2-sentabrda tashkil etilgan. Manzil: Yangiariq tumani, Po'rsang mahallasi."
    )
    
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "system", "content": system_instructions}, {"role": "user", "content": prompt}],
        )
        return str(response).replace("Google", "Maktab jamoasi")
    except:
        return "Tizim hozir band. Iltimos, keyinroq urinib ko'ring."

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
