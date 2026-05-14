import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- MAJBURIY GRAFIKA VA FON ---
# !important operatori orqali Streamlit'ning qora temasi bloklanadi
st.markdown("""
<style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                          url("https://images.unsplash.com/photo-1546410531-bb4caa6b424d?q=80&w=2071&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* Barcha konteynerlarni shaffof qilish */
    [data-testid="stHeader"], [data-testid="stAppViewBlockContainer"], .main {
        background-color: transparent !important;
    }

    .title { 
        color: white; 
        text-align: center; 
        font-size: 40px; 
        font-weight: bold; 
        text-shadow: 2px 2px 10px #000000;
        padding: 20px;
    }

    .user-msg { 
        background-color: rgba(50, 50, 60, 0.9) !important; 
        padding: 15px; border-radius: 15px; margin: 10px 0; 
        border-right: 5px solid #3B8ED0; color: white;
    }

    .ai-msg { 
        background-color: rgba(20, 20, 25, 0.9) !important; 
        padding: 15px; border-radius: 15px; 
        border-left: 5px solid #3B8ED0; margin: 10px 0; color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- USTOZLAR VA MA'MURIYAT ---
def get_ai_response(prompt):
    system_instructions = (
        "Sening isming - Maktab AI. 19-sonli maktab yordamchisisan. "
        "Saparboyev Husniddin (8-B sinf) seni yaratgan. "
        "DIQQAT: Google yoki boshqa kompaniyalar haqida gapirma. "
        "Javoblar rasmiy va imlo xatolarisiz bo'lsin."
        "\n\n--- MA'MURIYAT ---"
        "\nDirektor: Eshmetov Rustambay Ollaberganovich."
        "\nO'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek."
        "\nAdministrator: Sabirova Iroda."
        "\n\n--- O'QITUVCHILAR ---"
        "\nMatematika: Egamova R, Iskandarova D, Matkarimova M, Quramboyeva O, Xudaynazarova Z."
        "\nOna tili: Avazova R, Bobojonova M, Jumaniyozova S, Otajonova Sh, Xudoynazarova N."
        "\nIngliz tili: Eshmurodova R, Farxodova M, Qo'shoqova G, Rajabova L, Raxmanova S, Sadullayeva D."
        "\nRus tili: Bekmetova Sh, Bobojonova K, Saidova S, Sobirova N, Tillayeva A, Yusupova S."
        "\nBoshlang'ich sinf: Bobojonova E, Jumanazarova N, Kenjayeva I, Normatova I, Nurmetova M, Otajonova S, Quryozova S, Ro'ziboyeva S, Sadiqova F, Saidmatova M, Saparmatova S, Xo'jayeva Sh."
    )
    
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "system", "content": system_instructions}, {"role": "user", "content": prompt}],
        )
        return str(response).replace("Google", "Maktab jamoasi")
    except:
        return "Tizimda yuklama yuqori, qayta urinib ko'ring."

# --- CHAT ---
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{"Siz" if msg["role"] == "user" else "Maktab AI"}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"])

user_input = st.chat_input("Savol bering (Masalan: Matematika ustozlari kim?)...")

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
