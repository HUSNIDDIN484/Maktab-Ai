import streamlit as st
import g4f

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- MAJBURIY CSS (Fon rasm va shaffoflik uchun) ---
st.markdown(
<style>
    /* Asosiy fonni Yonsei universiteti rasmiga almashtirish */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                    url("https://images.unsplash.com/photo-1622662914032-901e1494918e?q=80&w=2070&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* Streamlit standart elementlarini shaffof qilish */
    [data-testid="stHeader"], [data-testid="stAppViewBlockContainer"], .main {
        background-color: transparent !important;
    }

    .title { 
        color: white; text-align: center; font-size: 38px; font-weight: bold; 
        text-shadow: 3px 3px 15px black; padding: 20px;
    }

    /* Xabarlar dizayni */
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
, unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MA'LUMOTLAR BAZASI ---
def get_ai_response(prompt):
    system_instructions = (
        "Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan. "
        "Seni 8-B sinf o'quvchisi Saparboyev Husniddin va maktab jamoasi yaratgan. "
        "DIQQAT: Google haqida gapirma. Imlo xatolarisiz, rasmiy va aniq tilda javob ber. Ortiqcha gapirmasdan savolga to'liq javob ber."
        
        "\n\n--- MA'MURIYAT ---"
        "\nDirektor: Eshmetov Rustambay Ollaberganovich. "
        "\nO'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek. "
        "\nAdministrator: Sabirova Iroda Yarash qizi."
        
        "\n\n--- O'QITUVCHILAR RO'YXATI ---"
        "\nMatematika: Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda."
        "\nOna tili: Avazova Risolat, Bobojonova Mushtariy, Jumaniyozova Sadoqat, Otajonova Sharofat, Xudoynazarova Nafosat."
        "\nIngliz tili: Eshmurodova Ra'no, Farxodova Muxtaram, Qo'shoqova Gulasal, Rajabova Lobar, Raxmanova So'najon, Sadullayeva Durdona."
        "\nRus tili: Bekmetova Shaxnoza, Bobojonova Komila, Saidova Saragul, Sobirova Nozima, Tillayeva Aziza, Yusupova Sanobar."
        "\nTarix: Allanazarova Zumrad, Matqurbonova Shohina, Matchanova Zebo, Sobirova Gulposhsha."
        "\nFizika/Kimyo: Aminova Mehriniso, Kurbonov Ollashukur, Razzaqova Kumushoy, Meylibayeva Aziza."
        "\nInformatika: Quranboyeva Nafosat."
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
        # Google so'zini avtomatik almashtirish
        return str(response).replace("Google", "Maktab jamoasi")
    except:
        return "Tizimda xatolik yuz berdi. Iltimos, birozdan so'ng qayta urinib ko'ring."

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
