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

# --- AI Funksiyasi ---
def get_ai_response(prompt):
    system_instructions = (
        "Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan. "
        "Seni 8-B sinf o'quvchisi Saparboyev Husniddin yaratgan. Maktab 1982-yil 2-sentabrda tashkil etilgan. "
        "MUHIM: O'qituvchilar va maktab ma'lumotlarini FAQAT so'ralganda ko'rsat. Imlo xatolarisiz, rasmiy tilda javob ber."
        "\n\n--- MA'MURIYAT ---"
        "\nDirektor: Eshmetov Rustambay. O'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek. Admin: Sabirova Iroda."
        "\n\n--- O'QITUVCHILAR ---"
        "\n(Matematika, Ona tili, Tarix, Fizika, Kimyo, Ingliz, Rus, Fransuz, Boshlang'ich, Sport, Musiqa, Rasm, Texno, Info barcha ro'yxat saqlangan)."
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
            return str(response).replace("Aria", "Maktab AI").replace("Opera", "19-son maktab")
        return "Serverda uzilish."
    except Exception:
        return "Hozirda band."

# --- Chat tarixi ---
for msg in st.session_state.messages:
    role_name = "Siz" if msg["role"] == "user" else "Maktab AI"
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{role_name}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"], use_container_width=True)

# --- Yagona Kirish Maydoni ---
user_input = st.chat_input("Savol yozing yoki rasm uchun 'Rasm: [tarif]' deb yozing...")

if user_input:
    # 1. Foydalanuvchi xabarini ko'rsatish
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. Rasm yoki Matn ekanligini tekshirish
    if user_input.lower().startswith("rasm:") or user_input.lower().startswith("chiz:"):
        # Rasm chizish qismi
        img_description = user_input.split(":", 1)[1].strip()
        with st.spinner("Rasm tayyorlanmoqda..."):
            encoded = urllib.parse.quote(img_description)
            img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
            st.session_state.messages.append({
                "role": "ai", 
                "content": f"Siz uchun '{img_description}' mavzusida rasm chizdim:", 
                "image": img_url
            })
    else:
        # Oddiy savol-javob qismi
        with st.spinner("O'ylamoqdaman..."):
            answer = get_ai_response(user_input)
            st.session_state.messages.append({"role": "ai", "content": answer})
    
    st.rerun()
