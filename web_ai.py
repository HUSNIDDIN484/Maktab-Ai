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
        "Seni 8-B sinf o'quvchisi Saparboyev Husniddin yaratgan. Maktab 1982-yil 2-sentabrda tashkil etilgan. "
        "MUHIM: Quyidagi ma'lumotlarni FAQAT foydalanuvchi maktab xodimlari yoki maktab haqida so'ragandagina ko'rsat. "
        "Boshqa paytda faqat berilgan savolga aniq javob ber. Imlo xatolarisiz, rasmiy tilda gapir."
        "\n\n--- MA'MURIYAT ---"
        "\nDirektor: Eshmetov Rustambay Ollaberganovich. O'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek. Administrator: Sabirova Iroda Yarash qizi."
        "\n\n--- O'QITUVCHILAR ---"
        "\nMatematika: Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda."
        "\nOna tili: Avazova Risolat, Bobojonova Mushtariy, Jumaniyozova Sadoqat, Otajonova Sharofat, Xudoynazarova Nafosat."
        "\nTarix: Allanazarova Zumrad, Matqurbonova Shohina, Matchanova Zebo, Sobirova Gulposhsha."
        "\nFizika/Kimyo: Aminova Mehriniso, Kurbonov Ollashukur, Razzaqova Kumushoy, Meylibayeva Aziza."
        "\nIngliz tili: Eshmurodova Ra'no, Farxodova Muxtaram, Qo'shoqova Gulasal, Rajabova Lobar, Raxmanova So'najon, Sadullayeva Durdona."
        "\nRus tili: Bekmetova Shaxnoza, Bobojonova Komila, Saidova Saragul, Sobirova Nozima, Tillayeva Aziza, Yusupova Sanobar."
        "\nBoshlang'ich ta'lim: Bobojonova Elmira, Maftuna, Jumanazarova Nargiza, Kenjayeva Iroda, Normatova Iqbol, Nurmetova Marhabo, Otajonova Sarvinoz, Quryozova Sanobar, Ro'ziboyeva Sarvinoz, Sadiqova Farida, Saidmatova Muattar, Saparmatova Sadoqat, Xo'jayeva Shahnoza."
        "\nSport/San'at: Pirnnazarov Nurali, Ro'zmetova Muhtarama, Xudaynazarov Davronbek, Yusupova Zuhraxon. Musiqa: O'razmetov O'tkir, Xusainov Sodiqjon. Tasviriy san'at: Otamuratov Rustam, Sobirova Maloxat."
        "\nTexnologiya: Boltayeva Zebo, Eshchanova Nodira, Matkarimova Intizor, Matyoqubova Xusniobod, Sobirov Ollayor. Informatika: Quranboyeva Nafosat."
        "\n\nManzil: Yangiariq tumani, Po'rsang mahallasi. Aloqa: +998975156307."
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
        return "Serverda texnik uzilish yuz berdi."
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
user_input = st.chat_input("Xabar yozing...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Javob tayyorlanmoqda..."):
        answer = get_ai_response(user_input)
        st.session_state.messages.append({"role": "ai", "content": answer})
    st.rerun()

# --- Yon panel (Rasm chizish) ---
with st.sidebar:
    st.title("🎨 Ijodiy bo'lim")
    img_prompt = st.text_input("Rasm tarifi:")
    if st.button("Rasm chizish"):
        if img_prompt:
            with st.spinner("Rasm tayyorlanmoqda..."):
                encoded = urllib.parse.quote(img_prompt)
                img_url = f"https://image.pollinations.ai/prompt/school_{encoded}?width=1024&height=1024&nologo=true"
                st.session_state.messages.append({"role": "ai", "content": f"'{img_prompt}' uchun rasm:", "image": img_url})
                st.rerun()
