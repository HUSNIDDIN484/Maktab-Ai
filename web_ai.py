import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- Dizayn va Orqa Fon (Yangilangan) ---
st.markdown("""
<style>
    /* Fon rasmi va qorong'u qatlam */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                    url("https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=2070&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* Streamlit bloklarini shaffof qilish */
    [data-testid="stHeader"], [data-testid="stAppViewBlockContainer"], [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
    }

    .title { 
        color: #ffffff; 
        text-align: center; 
        font-size: 36px; 
        font-weight: bold; 
        padding: 10px;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
    }

    .user-msg { 
        background-color: rgba(45, 45, 55, 0.85); 
        padding: 15px; border-radius: 15px; margin: 10px 0; 
        border-right: 5px solid #3B8ED0; color: white;
    }

    .ai-msg { 
        background-color: rgba(25, 25, 25, 0.85); 
        padding: 15px; border-radius: 15px; 
        border-left: 5px solid #3B8ED0; margin: 10px 0; color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Funksiyasi va Ustozlar Bazasi ---
def get_ai_response(prompt):
    system_instructions = (
        "Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan. "
        "Seni 8-B sinf o'quvchisi Saparboyev Husniddin yaratgan. "
        "DIQQAT: Google haqida gapirma. Imlo xatolarisiz, faqat rasmiy va aniq tilda javob ber. "
        
        "\n\n--- MA'MURIYAT ---"
        "\nDirektor: Eshmetov Rustambay Ollaberganovich."
        "\nO'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek."
        "\nAdministrator: Sabirova Iroda Yarash qizi."
        
        "\n\n--- O'QITUVCHILAR RO'YXATI ---"
        "\nMatematika: Egamova R, Iskandarova D, Matkarimova M, Quramboyeva O, Xudaynazarova Z."
        "\nOna tili va Adabiyot: Avazova R, Bobojonova M, Jumaniyozova S, Otajonova Sh, Xudoynazarova N."
        "\nIngliz tili: Eshmurodova R, Farxodova M, Qo'shoqova G, Rajabova L, Raxmanova S, Sadullayeva D."
        "\nRus tili: Bekmetova Sh, Bobojonova K, Saidova S, Sobirova N, Tillayeva A, Yusupova S."
        "\nBoshlang'ich sinf: Bobojonova E, Maftuna, Jumanazarova N, Kenjayeva I, Normatova I, Nurmetova M, Otajonova S, Quryozova S, Ro'ziboyeva S, Sadiqova F, Saidmatova M, Saparmatova S, Xo'jayeva Sh."
        "\nBoshqa fanlar (Fizika, Kimyo, Tarix, Biologiya, Sport, Informatika): Maktabimizning tajribali mutaxassislari dars berishadi."
    )
    
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": prompt}
            ],
        )
        return str(response).replace("Google", "Maktab jamoasi").replace("Aria", "Maktab AI")
    except Exception:
        return "Tizimda yuklama yuqori, keyinroq urinib ko'ring."

# --- Chat tarixi ---
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{"Siz" if msg["role"] == "user" else "Maktab AI"}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"])

# --- Kirish ---
user_input = st.chat_input("Savol bering (Masalan: Matematika ustozlari kim?)...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("O'ylanmoqda..."):
        if "rasm:" in user_input.lower():
            img_desc = user_input.lower().replace("rasm:", "").strip()
            encoded = urllib.parse.quote(img_desc)
            img_url = f"https://image.pollinations.ai/prompt/{encoded}"
            st.session_state.messages.append({"role": "ai", "content": f"'{img_desc}' bo'yicha rasm:", "image": img_url})
        else:
            answer = get_ai_response(user_input)
            st.session_state.messages.append({"role": "ai", "content": answer})
    
    st.rerun()
