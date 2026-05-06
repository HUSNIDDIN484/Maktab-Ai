import streamlit as st
import g4f
import urllib.parse
import asyncio
import nest_asyncio

# Streamlit-da asinxron loop xatolarini (Oh no!) tuzatish
nest_asyncio.apply()

# --- Sahifa sozlamalari ---
st.set_page_config(
    page_title="19-son Maktab AI",
    page_icon="🏫",
    initial_sidebar_state="collapsed"
)

# --- Maxsus Dizayn (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .title { color: #3B8ED0; text-align: center; font-size: 32px; font-weight: bold; margin-bottom: 20px; text-shadow: 2px 2px 4px #000; }
    .user-msg { background-color: #262730; padding: 15px; border-radius: 15px; margin: 10px 0; border-right: 5px solid #3B8ED0; }
    .ai-msg { background-color: #1E1E1E; padding: 15px; border-radius: 15px; border-left: 5px solid #3B8ED0; margin: 10px 0; }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

# --- Xotira (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Javob Funksiyasi ---
async def fetch_ai_response(prompt):
    # MAKTABNING BARCHA MA'LUMOTLARI SHU YERDA
    system_instructions = (
        "Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, 19-sonli maktabning rasmiy AI yordamchisisan. "
        "Maktab ma'lumotlarini har doim eslab qol va so'ralganda aniq javob ber: "
        "\n1. Direktor: ESHMETOV RUSTAMBAY OLLABERGANOVICH."
        "\n2. Administrator (ma'muriyat): SABIROVA IRODA YARASH QIZI."
        "\n3. Direktor o'rinbosarlari: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek."
        "\n4. Aloqa uchun asosiy telefon: +998975156307."
        "\n5. Maktab manzili: Yangiariq tumani, Qo'riqtom qishlog'i, Po'rsang mahallasi, Charog'bon ko'chasi 2-uy."
        "\n6. Kontingent: 570 o'quvchi va 65 o'qituvchi."
        "\n7. Tashkil etilgan sana: 1982-yil 2-sentyabr."
        "\n\nQoidalar: "
        "- O'zingni Aria yoki Opera deb tanishtirma, faqat 'Maktab AI' deb tanishtir."
        "- Tillarni aralashtirma, faqat toza O'zbek tilida javob ber."
        "- Ma'lumotlarni aniq va chiroyli formatda taqdim et."
    )

    try:
        # Eng barqaror provayderlar
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": prompt}
            ],
        )
        if response:
            res_str = str(response)
            # Keraksiz nomlarni almashtirish
            return res_str.replace("Aria", "Maktab AI").replace("Opera", "19-son maktab")
    except:
        return "Hozirda serverlarda yuklama yuqori. Iltimos, bir ozdan so'ng qayta urinib ko'ring."

# --- Chat tarixini ko'rsatish ---
for msg in st.session_state.messages:
    role_name = "Siz" if msg["role"] == "user" else "Maktab AI"
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{role_name}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"], use_container_width=True)

# --- Kirish maydoni ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Savol yozing yoki rasm tarifini bering...")
    col1, col2 = st.columns(2)
    submit_chat = col1.form_submit_button("Suhbat 💬")
    submit_img = col2.form_submit_button("Rasm 🎨")

# --- Suhbat logikasi ---
if submit_chat and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Maktab AI o'ylamoqda..."):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        answer = new_loop.run_until_complete(fetch_ai_response(user_input))
        st.session_state.messages.append({"role": "ai", "content": answer})
    st.rerun()

# --- Rasm logikasi ---
if submit_img and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Rasm tarifi: {user_input}"})
    with st.spinner("Rasm tayyorlanmoqda..."):
        encoded_prompt = urllib.parse.quote(user_input)
        img_url = f"https://image.pollinations.ai/prompt/school_art_{encoded_prompt}?width=1024&height=1024&nologo=true"
        st.session_state.messages.append({
            "role": "ai", 
            "content": f"'{user_input}' asosida rasm tayyorlandi:", 
            "image": img_url
        })
    st.rerun()
