import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- FON RASMI (Yonsei University) ---
st.markdown("""
<style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                          url("https://images.unsplash.com/photo-1622662914032-901e1494918e?q=80&w=2070&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    [data-testid="stHeader"], [data-testid="stAppViewBlockContainer"], .main {
        background-color: transparent !important;
    }

    .title { 
        color: white; 
        text-align: center; 
        font-size: 38px; 
        font-weight: bold; 
        text-shadow: 2px 2px 12px rgba(0,0,0,0.9);
        padding: 20px;
    }

    .user-msg { 
        background-color: rgba(50, 50, 65, 0.85) !important; 
        padding: 15px; border-radius: 15px; margin: 10px 0; 
        border-right: 5px solid #3B8ED0; color: white;
    }

    .ai-msg { 
        background-color: rgba(20, 20, 25, 0.85) !important; 
        padding: 15px; border-radius: 15px; 
        border-left: 5px solid #3B8ED0; margin: 10px 0; color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MA'MURIYAT VA USTOZLAR BAZASI ---
def get_ai_response(prompt):
    system_instructions = (
        "Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan."
        "Seni 8-B sinf o'quvchisi Saparboyev Husniddin yaratgan."
        "DIQQAT: Google yoki boshqa kompaniyalar haqida gapirma. Rasmiy, aniq va imlo xatolarisiz javob ber."
        
        "\n\n--- MA'MURIYAT ---"
        "\nDirektor: Eshmetov Rustambay Ollaberganovich."
        "\nO'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek."
        "\nAdministrator: Sabirova Iroda."
        
        "\n\n--- O'QITUVCHILAR RO'YXATI ---"
        "\nMatematika: Egamova R, Iskandarova D, Matkarimova M, Quramboyeva O, Xudaynazarova Z."
        "\nOna tili va Adabiyot: Avazova R, Bobojonova M, Jumaniyozova S, Otajonova Sh, Xudoynazarova N."
        "\nIngliz tili: Eshmurodova R, Farxodova M, Qo'shoqova G, Rajabova L, Raxmanova S, Sadullayeva D."
        "\nRus tili: Bekmetova Sh, Bobojonova K, Saidova S, Sobirova N, Tillayeva A, Yusupova S."
        "\nBoshlang'ich sinf o'qituvchilari: Bobojonova E, Jumanazarova N, Kenjayeva I, Normatova I, Nurmetova M, Otajonova S, Quryozova S, Ro'ziboyeva S, Sadiqova F, Saidmatova M, Saparmatova S, Xo'jayeva Sh."
    )
    
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "system", "content": system_instructions}, {"role": "user", "content": prompt}],
        )
        # Tizim nomini to'g'rilash
        return str(response).replace("Google", "Maktab jamoasi").replace("Aria", "Maktab AI")
    except:
        return "Hozirda tizim band, iltimos birozdan so'ng qayta urinib ko'ring."

# --- CHAT INTERFEYSI ---
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{"Siz" if msg["role"] == "user" else "Maktab AI"}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

user_input = st.chat_input("Savol yozing (Masalan: Direktorimiz kim?)...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Javob tayyorlanmoqda..."):
        answer = get_ai_response(user_input)
        st.session_state.messages.append({"role": "ai", "content": answer})
    st.rerun()
