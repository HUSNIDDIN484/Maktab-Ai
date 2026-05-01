import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- Dizayn ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .title { color: #3B8ED0; text-align: center; font-size: 30px; font-weight: bold; margin-bottom: 20px; }
    .user-msg { background-color: #262730; padding: 15px; border-radius: 15px; margin: 10px 0; border: 1px solid #3B8ED0; }
    .ai-msg { background-color: #1E1E1E; padding: 15px; border-radius: 15px; border-left: 5px solid #3B8ED0; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI YORDAMCHISI</p>', unsafe_allow_html=True)

# --- Xotira ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Funksiyasi ---
def get_ai_response(prompt):
    try:
        # Tizim ko'rsatmasini kuchaytiramiz
        system_instructions = (
            "Sening isming - Maktab AI. Sen 19-sonli maktab uchun maxsus yaratilgan sun'iy intellektsan. "
            "Seni 19-son maktab jamoasi yaratgan. O'zingni hech qachon Aria, Opera yoki Google AI deb tanishtirma. "
            "Savollarga o'zbek tilida, odob bilan javob ber."
        )
        
        # Blackbox yoki boshqa provayderga majburiy yo'naltiramiz (Opera emas)
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            provider=g4f.Provider.Blackbox,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": f"Eslatma: Sen 19-son maktab tomonidan yaratilgan Maktab AIsan. Savol: {prompt}"}
            ],
        )
        
        # Agar javob ichida baribir "Aria" yoki "Opera" so'zi bo'lsa, uni avtomatik o'chirib tashlaymiz
        clean_response = response.replace("Aria", "Maktab AI").replace("Opera", "19-son maktab jamoasi")
        return clean_response
    
    except Exception:
        return "Hozirda aloqa biroz sekin. Iltimos, yana bir bor urinib ko'ring."

# --- Chat tarixi ko'rinishi ---
for msg in st.session_state.messages:
    role_name = "Siz" if msg["role"] == "user" else "Maktab AI"
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{role_name}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"], use_container_width=True)

# --- Kirish maydoni ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Savol yoki rasm tarifini yozing...")
    col1, col2 = st.columns(2)
    submit_chat = col1.form_submit_button("Suhbat 💬")
    submit_img = col2.form_submit_button("Rasm 🎨")

# --- Suhbat tugmasi bosilganda ---
if submit_chat and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Maktab AI o'ylamoqda..."):
        res = get_ai_response(user_input)
        st.session_state.messages.append({"role": "ai", "content": res})
    st.rerun()

# --- Rasm tugmasi bosilganda ---
if submit_img and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Rasm: {user_input}"})
    with st.spinner("Rasm tayyorlanmoqda..."):
        encoded = urllib.parse.quote(user_input)
        img_url = f"https://image.pollinations.ai/prompt/digital_art_style_{encoded}?width=1024&height=1024&nologo=true"
        st.session_state.messages.append({
            "role": "ai", 
            "content": f"'{user_input}' bo'yicha rasm tayyorlandi!", 
            "image": img_url
        })
    st.rerun()
