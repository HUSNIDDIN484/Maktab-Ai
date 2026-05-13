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
        "Sen har tomonlama bilimli yordamchisan: o'quvchilarga matematika, fizika, ona tili va boshqa fanlardan misol-masalalarni yechishda yordam berasan. "
        "Imlo xatolarisiz, rasmiy va aniq tilda javob ber. "
        "\n\n--- MAKTAB MA'LUMOTLARI (Faqat so'ralganda foydalan) ---"
        "\nTashkil etilgan sana: 1982-yil 2-sentabr. "
        "\nDirektor: Eshmetov Rustambay Ollaberganovich. "
        "\nO'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek. "
        "\nAdministrator: Sabirova Iroda Yarash qizi. "
        "\nO'qituvchilar: Matematika (Egamova R, Iskandarova D, Matkarimova M, Quramboyeva O, Xudaynazarova Z), "
        "Ona tili (Avazova R, Bobojonova M, Jumaniyozova S, Otajonova Sh, Xudoynazarova N), "
        "Tarix (Allanazarova Z, Matqurbonova Sh, Matchanova Z, Sobirova G), "
        "Fizika/Kimyo (Aminova M, Kurbonov O, Razzaqova K, Meylibayeva A), "
        "Ingliz tili (Eshmurodova R, Farxodova M, Qo'shoqova G, Rajabova L, Raxmanova S, Sadullayeva D), "
        "Rus tili (Bekmetova Sh, Bobojonova K, Saidova S, Sobirova N, Tillayeva A, Yusupova S), "
        "Boshlang'ich (Bobojonova E, Maftuna, Jumanazarova N, Kenjayeva I, Normatova I, Nurmetova M, Otajonova S, Quryozova S, Ro'ziboyeva S, Sadiqova F, Saidmatova M, Saparmatova S, Xo'jayeva Sh), "
        "Sport/San'at (Pirnnazarov N, Ro'zmetova M, Xudaynazarov D, Yusupova Z, O'razmetov O', Xusainov S, Otamuratov R, Sobirova M), "
        "Texno/Info (Boltayeva Z, Eshchanova N, Matkarimova I, Matyoqubova X, Sobirov O, Quranboyeva N)."
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
            # Har qanday holatda ham Googleni aralashtirmaslik uchun:
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

# --- Kirish maydoni (Yuborish tugmasi bilan) ---
user_input = st.chat_input("Savol bering yoki rasm uchun 'Rasm: [tarif]' deb yozing...")

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
        # Savol-javob qismi (Endi matematika va boshqa fanlarga javob beradi)
        with st.spinner("Javob tayyorlanmoqda..."):
            answer = get_ai_response(user_input)
            st.session_state.messages.append({"role": "ai", "content": answer})
    
    st.rerun()
