import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- Dizayn (Interfeys) ---
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
        "Seni 8-B sinf o'quvchisi Saparboyev Husniddin va maktab jamoasi yaratgan. "
        "MUHIM QOIDA: Google yoki boshqa tashqi kompaniyalar haqida gapirma. "
        "Faqat 19-sonli maktab va Husniddin haqida ma'lumot ber. Imlo xatolarisiz, rasmiy va aniq tilda javob ber. "
        "Ma'lumotlarni faqat so'ralganda taqdim et. "
        "\n\n--- MAKTAB MA'LUMOTLARI ---"
        "\nTashkil etilgan sana: 1982-yil 2-sentabr. "
        "\nDirektor: Eshmetov Rustambay Ollaberganovich. "
        "\nO'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek. "
        "\nAdministrator: Sabirova Iroda Yarash qizi. "
        "\nO'qituvchilar: Matematika (Egamova R, Iskandarova D, Matkarimova M, Quramboyeva O, Xudaynazarova Z), "
        "Ona tili (Avazova R, Bobojonova M, Jumaniyozova S, Otajonova Sh, Xudoynazarova N), "
        "Ingliz tili (Eshmurodova R, Farxodova M, Qo'shoqova G, Rajabova L, Raxmanova S, Sadullayeva D), "
        "Rus tili (Bekmetova Sh, Bobojonova K, Saidova S, Sobirova N, Tillayeva A, Yusupova S). "
        "Boshqa barcha fan o'qituvchilari ma'lumotlar bazasida mavjud."
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
            # Google haqidagi har qanday gapni avtomatik tozalash
            return res_str.replace("Google", "19-son maktab jamoasi").replace("Aria", "Maktab AI")
        return "Xabar yuborishda xatolik yuz berdi."
    except Exception:
        return "Hozirda serverlar band, birozdan so'ng qayta urinib ko'ring."

# --- Chat tarixi ---
for msg in st.session_state.messages:
    role_name = "Siz" if msg["role"] == "user" else "Maktab AI"
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{role_name}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"], use_container_width=True)

# --- Yagona Kirish Maydoni (Yuborish tugmasi bilan) ---
user_input = st.chat_input("Savol yozing yoki rasm uchun 'Rasm: [tarif]' deb yozing...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Rasm buyrug'ini tekshirish
    if user_input.lower().startswith("rasm:") or user_input.lower().startswith("chiz:"):
        img_desc = user_input.split(":", 1)[1].strip()
        with st.spinner("Rasm tayyorlanmoqda..."):
            encoded = urllib.parse.quote(img_desc)
            img_url = f"https://image.pollinations.ai/prompt/school_style_{encoded}?width=1024&height=1024&nologo=true"
            st.session_state.messages.append({"role": "ai", "content": f"'{img_desc}' uchun rasm tayyorlandi:", "image": img_url})
    else:
        # Savol-javob qismi
        with st.spinner("O'ylamoqdaman..."):
            answer = get_ai_response(user_input)
            st.session_state.messages.append({"role": "ai", "content": answer})
    
    st.rerun()
