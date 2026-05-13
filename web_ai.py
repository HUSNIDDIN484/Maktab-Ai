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
        "Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan, seni 8-b sinf oquvchisi Saparboyev Husniddin yaratgan. "
        "Faqat o'qituvchilar haqida so'ralganda ushbu ma'lumotlardan foydalan: "
        "\n--- RAHBARIYAT VA MA'MURIYAT ---"
        "\n- Direktor: ESHMETOV RUSTAMBAY OLLABERGANOVICH."
        "\n- Direktor o'rinbosarlari: Bekchanov Arslon Kadamboyevich, JALILOV ELBEK UMAROVICH, Salayev Mavlyanbek Shomurotovich."
        "\n- Administrator: Sabirova Iroda Yarash qizi."
        "\n--- O'QITUVCHILAR ---"
        "\n(Barcha o'qituvchilar ro'yxati bu yerda saqlanadi...)"
        "\nManzil: Yangiariq tumani, Po'rsang mahallasi. Aloqa: +998975156307. Maktab tashkil qilingan sana: 1982-yil 2-sentabr."
        "Faqat o'zbek tilida javob ber va o'zingni 'Maktab AI' deb tani."
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
            res_str = str(response)
            return res_str.replace("Aria", "Maktab AI").replace("Opera", "19-son maktab")
        return "Serverda biroz uzilish bo'ldi."
    except Exception:
        return "Hozirda serverlar band."

# --- Chat tarixi ---
for msg in st.session_state.messages:
    role_name = "Siz" if msg["role"] == "user" else "Maktab AI"
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{role_name}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"], use_container_width=True)

# --- Kirish maydoni va Yuborish tugmasi ---
# st.chat_input funksiyasi avtomatik ravishda chiroyli "Yuborish" tugmasini qo'shadi
user_input = st.chat_input("Xabar yozing...")

if user_input:
    # Foydalanuvchi xabarini qo'shish
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # AI javobini olish
    with st.spinner("O'ylamoqdaman..."):
        answer = get_ai_response(user_input)
        st.session_state.messages.append({"role": "ai", "content": answer})
    
    # Sahifani yangilash
    st.rerun()

# --- Rasm chizish uchun alohida tugma (ixtiyoriy) ---
with st.sidebar:
    st.title("🎨 Ijodiy bo'lim")
    img_prompt = st.text_input("Rasm tarifi:")
    if st.button("Rasm chizish"):
        if img_prompt:
            with st.spinner("Chizilmoqda..."):
                encoded = urllib.parse.quote(img_prompt)
                img_url = f"https://image.pollinations.ai/prompt/school_style_{encoded}?width=1024&height=1024&nologo=true"
                st.session_state.messages.append({"role": "ai", "content": f"'{img_prompt}' uchun rasm:", "image": img_url})
                st.rerun()
