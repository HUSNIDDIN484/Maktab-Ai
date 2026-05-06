import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- Dizayn ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .title { color: #3B8ED0; text-align: center; font-size: 32px; font-weight: bold; margin-bottom: 20px; }
    .user-msg { background-color: #262730; padding: 15px; border-radius: 15px; margin: 10px 0; border-right: 5px solid #3B8ED0; }
    .ai-msg { background-color: #1E1E1E; padding: 15px; border-radius: 15px; border-left: 5px solid #3B8ED0; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Funksiyasi (Ma'lumotlar yuklangan variant) ---
def get_ai_response(prompt):
    # MAKTAB MA'LUMOTLARI SHU YERGA JOYLANDI:
    system_instructions = (
        "Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktabning rasmiy AI yordamchisisan. "
        "Maktab haqida muhim ma'lumotlar: "
        "- Manzil: Po'rsang mahallasi, Charog'bon ko'chasi 2-uy. "
        "- Tashkil etilgan sana: 1982-yil 2-sentyabr. "
        "- Direktor: ESHMETOV RUSTAMBAY OLLABERGANOVICH. "
        "- Direktor o'rinbosarlari: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek. "
        "- Maktab kontingenti: 570 nafar o'quvchi va 65 nafar o'qituvchi. "
        "- Yuqori tashkilot: Xorazm viloyati Maktabgacha va maktab ta'limi boshqarmasi. "
        "Seni 19-son maktab jamoasi yaratgan. O'zingni Aria yoki Opera deb tanishtirma. Faqat o'zbek tilida javob ber."
    )
    
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": f"Sen Maktab AIsan. Savol: {prompt}"}
            ],
        )
        
        if response:
            res_str = str(response)
            return res_str.replace("Aria", "Maktab AI").replace("Opera", "19-son maktab")
        return "Xabar mazmuni bo'sh qaytdi."
        
    except Exception as e:
        return "Hozirda serverlar band. Iltimos, bir ozdan so'ng qayta urinib ko'ring."

# --- Chat tarixi ---
for msg in st.session_state.messages:
    role_name = "Siz" if msg["role"] == "user" else "Maktab AI"
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{role_name}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"], use_container_width=True)

# --- Kirish ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Xabar yozing...")
    col1, col2 = st.columns(2)
    submit_chat = col1.form_submit_button("Suhbat 💬")
    submit_img = col2.form_submit_button("Rasm 🎨")

if submit_chat and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("O'ylamoqdaman..."):
        answer = get_ai_response(user_input)
        st.session_state.messages.append({"role": "ai", "content": answer})
    st.rerun()

if submit_img and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Rasm: {user_input}"})
    with st.spinner("Chizilmoqda..."):
        encoded = urllib.parse.quote(user_input)
        img_url = f"https://image.pollinations.ai/prompt/school_style_{encoded}?width=1024&height=1024&nologo=true"
        st.session_state.messages.append({"role": "ai", "content": "Rasm tayyor!", "image": img_url})
    st.rerun()
