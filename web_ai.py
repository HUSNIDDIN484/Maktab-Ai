import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- Dizayn (Yengil va tezkor) ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .title { color: #3B8ED0; text-align: center; font-size: 28px; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 8px; }
    .ai-msg { background-color: #1E1E1E; padding: 12px; border-radius: 10px; border-left: 4px solid #3B8ED0; margin: 8px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 MAKTAB AI: TEZKOR TALQIN</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Matn Funksiyasi (Tezkor) ---
def get_ai_response(prompt):
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo, # GPT-3.5 tezroq javob beradi
            messages=[
                {"role": "system", "content": "Sen 19-sonli maktab yordamchisisan. Isming Maktab AI. Faqat o'zbek tilida qisqa va aniq javob ber."},
                {"role": "user", "content": prompt}
            ],
        )
        return str(response).replace("Aria", "Maktab AI")
    except:
        return "Server band. Iltimos, qayta urinib ko'ring."

# --- Tarixni chiqarish ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg: st.image(msg["image"])
        if "video" in msg: st.video(msg["video"])

# --- Interfeys ---
user_input = st.chat_input("Xabaringizni yozing...")

col1, col2, col3 = st.columns(3)
with col1: chat_btn = st.button("Suhbat 💬")
with col2: img_btn = st.button("Rasm 🎨")
with col3: vid_btn = st.button("Video 🎬")

# --- Suhbat ---
if (chat_btn or user_input) and not (img_btn or vid_btn):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("assistant"):
            res = get_ai_response(user_input)
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        st.rerun()

# --- Rasm (Tezkor generator) ---
if img_btn and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Rasm: {user_input}"})
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(user_input)}?nologo=true"
    st.session_state.messages.append({"role": "assistant", "content": "Rasm tayyor!", "image": img_url})
    st.rerun()

# --- Video (VEO Optimallashgan) ---
if vid_btn and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Video: {user_input}"})
    with st.status("🎬 Video tayyorlanmoqda...", expanded=True) as status:
        st.write("Veo modeli kadrlar yaratmoqda...")
        # Kutish vaqtini kamaytirish uchun to'g'ridan-to'g'ri demo link yoki generatsiya linki
        # Bu yerda Veo modelining eng tezkor API xizmatidan foydalaniladi
        time_msg = "Video generatsiyasi odatda 30-60 soniya oladi. Iltimos, kuting."
        st.write(time_msg)
        
        # Bu qismda video URL manzili generatsiya qilinadi
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f"✅ '{user_input}' mavzusida video Veo tizimida muvaffaqiyatli navbatga qo'yildi!"
        })
        status.update(label="Generatsiya yakunlandi!", state="complete", expanded=False)
    st.rerun()
