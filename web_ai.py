import streamlit as st
import g4f
import urllib.parse
import os

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- Dizayn ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .title { color: #3B8ED0; text-align: center; font-size: 32px; font-weight: bold; margin-bottom: 10px; }
    .user-msg { background-color: #262730; padding: 15px; border-radius: 15px; margin: 10px 0; border-right: 5px solid #3B8ED0; }
    .ai-msg { background-color: #1E1E1E; padding: 15px; border-radius: 15px; border-left: 5px solid #3B8ED0; margin: 10px 0; }
    .logo-container { display: flex; justify-content: center; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- Logotip va Sarlavha ---
logo_path = "image_68543b.jpg"
if os.path.exists(logo_path):
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(logo_path, width=150)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

# --- Xotira tizimini tekshirish ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Funksiyasi (Xotira bilan ishlaydigan variant) ---
def get_ai_response(user_input):
    system_instructions = (
        "Sening isming - Maktab AI. Sen 19-sonli maktab yordamchisisan. "
        "Seni 19-son maktab jamoasi yaratgan. O'zingni Aria yoki Opera deb tanishtirma. "
        "Faqat o'zbek tilida javob ber. Avvalgi suhbat mazmunini eslab qol va shunga qarab javob qaytar."
    )
    
    # AIga yuboriladigan xabarlar paketi (Tizim ko'rsatmasi + Suhbat tarixi + Yangi savol)
    full_history = [{"role": "system", "content": system_instructions}]
    
    # Xotiradagi oxirgi 10 ta xabarni AIga yuboramiz (xotira juda kattalashib ketmasligi uchun)
    for msg in st.session_state.messages[-10:]:
        # Faqat matnli xabarlarni xotiraga qo'shamiz (rasmlarsiz)
        if "content" in msg and msg["content"]:
            # Rolni to'g'irlaymiz: 'ai' -> 'assistant'
            role = "assistant" if msg["role"] == "ai" else "user"
            full_history.append({"role": role, "content": msg["content"]})
    
    # Yangi savolni qo'shamiz
    full_history.append({"role": "user", "content": user_input})

    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=full_history,
        )
        
        if response:
            res_str = str(response)
            # Aria filtrini qo'llaymiz
            return res_str.replace("Aria", "Maktab AI").replace("Opera", "19-son maktab jamoasi")
        return "Xabar mazmuni bo'sh qaytdi."
        
    except Exception:
        return "Hozirda serverlar band. Iltimos, bir ozdan so'ng qayta urinib ko'ring."

# --- Chat tarixini ekranga chiqarish ---
for msg in st.session_state.messages:
    role_name = "Siz" if msg["role"] == "user" else "Maktab AI"
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{role_name}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"], use_container_width=True)

# --- Kirish maydoni ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Xabar yozing...")
    col1, col2 = st.columns(2)
    submit_chat = col1.form_submit_button("Suhbat 💬")
    submit_img = col2.form_submit_button("Rasm 🎨")

# --- Suhbat tugmasi ---
if submit_chat and user_input:
    # 1. Foydalanuvchi xabarini xotiraga qo'shish
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("Maktab AI o'ylamoqda..."):
        # 2. AIga butun xotira bilan so'rov yuborish
        answer = get_ai_response(user_input)
        # 3. AI javobini xotiraga qo'shish
        st.session_state.messages.append({"role": "ai", "content": answer})
    st.rerun()

# --- Rasm tugmasi ---
if submit_img and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Rasm chizish: {user_input}"})
    with st.spinner("Chizilmoqda..."):
        encoded = urllib.parse.quote(user_input)
        img_url = f"https://image.pollinations.ai/prompt/school_style_{encoded}?width=1024&height=1024&nologo=true"
        st.session_state.messages.append({"role": "ai", "content": f"'{user_input}' uchun rasm tayyor!", "image": img_url})
    st.rerun()
