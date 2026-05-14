import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫", layout="centered")

# --- Fon rasmi va Dizaynni majburiy o'rnatish ---
# Bu yerda rasm chiqishi uchun eng kuchli CSS usuli ishlatilgan
st.markdown("""
<style>
    /* Asosiy fon */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url("https://cdn.pixabay.com/photo/2016/10/11/13/43/university-1731613_1280.jpg") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* Barcha qatlamlarni shaffof qilish */
    [data-testid="stHeader"], [data-testid="stAppViewBlockContainer"], .main {
        background-color: transparent !important;
    }

    .title { 
        color: white; 
        text-align: center; 
        font-size: 38px; 
        font-weight: bold; 
        padding-top: 20px;
        text-shadow: 2px 2px 15px rgba(0,0,0,1);
    }

    /* Xabarlar dizayni */
    .user-msg { 
        background-color: rgba(60, 60, 75, 0.9) !important; 
        padding: 15px; border-radius: 15px; margin: 10px 0; 
        border-right: 5px solid #3B8ED0; color: white;
    }
    .ai-msg { 
        background-color: rgba(30, 30, 30, 0.9) !important; 
        padding: 15px; border-radius: 15px; 
        border-left: 5px solid #3B8ED0; margin: 10px 0; color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Funksiyasi va Ustozlar Ma'lumotnomasi ---
def get_ai_response(prompt):
    system_instructions = (
        "Sening isming - Maktab AI. 19-sonli maktab yordamchisisan. "
        "Seni 8-B sinf o'quvchisi Saparboyev Husniddin yaratgan. "
        "Google haqida gapirma. Imlo xatolarisiz, rasmiy javob ber."
        "\n\n--- MA'MURIYAT ---"
        "\nDirektor: Eshmetov Rustambay. O'rinbosarlar: Bekchanov A, Jalilov E, Salayev M. Admin: Sabirova I."
        "\n\n--- O'QITUVCHILAR ---"
        "\nMatematika: Egamova R, Iskandarova D, Matkarimova M, Quramboyeva O, Xudaynazarova Z."
        "\nIngliz tili: Eshmurodova R, Farxodova M, Qo'shoqova G, Rajabova L, Raxmanova S, Sadullayeva D."
        "\nOna tili: Avazova R, Bobojonova M, Jumaniyozova S, Otajonova Sh, Xudoynazarova N."
        "\nRus tili: Bekmetova Sh, Bobojonova K, Saidova S, Sobirova N, Tillayeva A, Yusupova S."
        "\nBoshlang'ich: Bobojonova E, Jumanazarova N, Kenjayeva I, Normatova I, Nurmetova M, Otajonova S, Quryozova S, Ro'ziboyeva S, Sadiqova F, Saidmatova M, Saparmatova S, Xo'jayeva Sh."
    )
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "system", "content": system_instructions}, {"role": "user", "content": prompt}],
        )
        return str(response).replace("Google", "19-son maktab jamoasi")
    except:
        return "Hozircha javob berolmayman, qayta urinib ko'ring."

# --- Chat tarixi ---
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}">{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"])

# --- Kirish ---
user_input = st.chat_input("Savol bering (Masalan: Direktor kim?)...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Javob tayyorlanmoqda..."):
        if "rasm:" in user_input.lower():
            img_desc = user_input.lower().replace("rasm:", "").strip()
            img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(img_desc)}"
            st.session_state.messages.append({"role": "ai", "content": f"'{img_desc}' rasmi:", "image": img_url})
        else:
            answer = get_ai_response(user_input)
            st.session_state.messages.append({"role": "ai", "content": answer})
    st.rerun()
