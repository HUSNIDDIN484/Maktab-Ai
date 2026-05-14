import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- Dizayn va Orqa Fon Rasmi ---
st.markdown("""
<style>
    .stApp {
        background-image: linear-gradient(rgba(14, 17, 23, 0.85), rgba(14, 17, 23, 0.85)), 
                          url("https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }
    .title { color: #3B8ED0; text-align: center; font-size: 34px; font-weight: bold; margin-bottom: 25px; text-shadow: 2px 2px 4px #000000; }
    .user-msg { background-color: rgba(38, 39, 48, 0.9); padding: 15px; border-radius: 15px; margin: 10px 0; border-right: 5px solid #3B8ED0; }
    .ai-msg { background-color: rgba(30, 30, 30, 0.9); padding: 15px; border-radius: 15px; border-left: 5px solid #3B8ED0; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Funksiyasi ---
def get_ai_response(prompt):
    system_instructions = (
        "Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan. "
        "Seni 8-B sinf o'quvchisi Saparboyev Husniddin va maktab jamoasi yaratgan. "
        "DIQQAT: Google haqida gapirma. Imlo xatolarisiz, rasmiy va aniq tilda javob ber. "
        "Sen matematika, fizika va boshqa fanlardan yordam beradigan bilimli yordamchisan. "
        "\n\n--- MA'MURIYAT ---"
        "\nDirektor: Eshmetov Rustambay Ollaberganovich. O'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek. Administrator: Sabirova Iroda Yarash qizi."
        "\n\n--- O'QITUVCHILAR ---"
        "\nMatematika: Egamova R, Iskandarova D, Matkarimova M, Quramboyeva O, Xudaynazarova Z."
        "\nOna tili: Avazova R, Bobojonova M, Jumaniyozova S, Otajonova Sh, Xudoynazarova N."
        "\nIngliz tili: Eshmurodova R, Farxodova M, Qo'shoqova G, Rajabova L, Raxmanova S, Sadullayeva D."
        "\nRus tili: Bekmetova Sh, Bobojonova K, Saidova S, Sobirova N, Tillayeva A, Yusupova S."
        "\nBoshlang'ich: Bobojonova E, Maftuna, Jumanazarova N, Kenjayeva I, Normatova I, Nurmetova M, Otajonova S, Quryozova S, Ro'ziboyeva S, Sadiqova F, Saidmatova M, Saparmatova S, Xo'jayeva Sh."
        "\nBoshqa: Tarix, Fizika, Kimyo, Sport, Musiqa, Texnologiya va Informatika ustozlari ro'yxati bazada mavjud."
    )
    
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": prompt}
            ],
        )
        if response:
            return str(response).replace("Google", "19-son maktab jamoasi").replace("Aria", "Maktab AI")
        return "Javob olishda xatolik."
    except Exception:
        return "Tizim hozirda band."

# --- Chat tarixi ---
for msg in st.session_state.messages:
    role_name = "Siz" if msg["role"] == "user" else "Maktab AI"
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{role_name}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"], use_container_width=True)

# --- Kirish maydoni ---
user_input = st.chat_input("Savol yozing yoki rasm uchun 'Rasm: [tarif]' deb yozing...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    input_lower = user_input.lower()
    if any(keyword in input_lower for keyword in ["rasm:", "chiz:", "rasm ber"]):
        img_desc = user_input.replace("rasm:", "").replace("chiz:", "").replace("rasm ber", "").strip()
        if not img_desc: img_desc = "maktab kutubxonasi"
            
        with st.spinner("Rasm tayyorlanmoqda..."):
            encoded = urllib.parse.quote(img_desc)
            img_url = f"https://image.pollinations.ai/prompt/school_style_{encoded}?width=1024&height=1024&nologo=true"
            st.session_state.messages.append({"role": "ai", "content": f"'{img_desc}' rasmi tayyor:", "image": img_url})
    else:
        with st.spinner("Javob tayyorlanmoqda..."):
            answer = get_ai_response(user_input)
            st.session_state.messages.append({"role": "ai", "content": answer})
    
    st.rerun()
