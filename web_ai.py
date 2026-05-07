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

# --- AI Funksiyasi (Barcha 65 nafar xodim yuklangan variant) ---
def get_ai_response(prompt):
    system_instructions = (
        "Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan. "
        "Faqat o'qituvchilar haqida so'ralganda ushbu ma'lumotlardan foydalan: "
        "\n--- RAHBARIYAT VA MA'MURIYAT ---"
        "\n- Direktor: ESHMETOV RUSTAMBAY OLLABERGANOVICH."
        "\n- Direktor o'rinbosarlari: Bekchanov Arslon Kadamboyevich, JALILOV ELBEK UMAROVICH, Salayev Mavlyanbek Shomurotovich."
        "\n- Administrator: Sabirova Iroda Yarash qizi."
        "\n- Boshqaruv xodimi va psixologlar: Xo'jayeva Dilorom Otanazarovna, Xudaynazarova Dilbar Yuldoshevna."
        "\n--- FAN O'QITUVCHILARI ---"
        "\n- Tarix: Allanazarova Zumrad Xo'janazarovna, MATQURBONOVA SHOHINA G‘ULOMJON QIZI, Matchanova Zebo Ozodovna, SOBIROVA GULPOSHSHA ERGASH QIZI."
        "\n- Fizika: Aminova Mehriniso Qosim qizi, Kurbonov Ollashukur Otajon o'g'li."
        "\n- Matematika: Egamova Rajabgul Azamat qizi, Iskandarova Dilnavoz Ro'zmatovna, Matkarimova Muxabbat Axmedovna, Quramboyeva O`g`iljon Xolmurod qizi, Xudaynazarova Ziyoda Xakimboy Qizi."
        "\n- Ona tili va Adabiyot: Avazova Risolat Samandarovna, Bobojonova Mushtariy Umidbek Qizi, Jumaniyozova Sadoqat Xudayzarovna, Otajonova Sharofat Shakirovna, Xudoynazarova Nafosat Sotimboyevna."
        "\n- Biologiya, Kimyo va Geografiya: Annazarova Dildora Rustamboyevna (Biologiya), Razzaqova Kumushoy Yusufbay qizi (Kimyo), Qurbanova Farida Kupalboyevna (Geografiya)."
        "\n- Ingliz tili: Eshmurodova Ra'no Ozod qizi, Farxodova Muxtaram Yarashboy Qizi, Qo'shoqova Gulasal Yo'ldoshevna, Rajabova Lobar Qadirberganovna, Raxmanova So'najon Otabekovna, Sadullayeva Durdona Nuraddin qizi."
        "\n- Rus tili: Bekmetova Shaxnoza Saparboyevna, BOBOJONOVA KOMILA SANJARBEKOVNA, Meylibayeva Aziza To'xtasin qizi, Saidova Saragul O'rinboyevna, SOBIROVA NOZIMA DILMUROD QIZI, Tillayeva Aziza Ikrom qizi, Yusupova Sanobar Axmedovna."
        "\n- Fransuz tili: Kurbonova Nigora Matyoqubovna."
        "\n- Boshlang'ich ta'lim: Bobojonova Elmira Quronboyevna, Bobojonova Maftuna Sulton qizi, Jumanazarova Nargiza Rutamovna, Kenjayeva Iroda Ramatjonovna, Normatova Iqbol Masharibovna, Nurmetova Marhabo Shakirboyevna, OTAJONOVA SARVINOZ BOBONAZAR QIZI, Quryozova Sanobar Karimovna, Ro'ziboyeva Sarvinoz Shodlik qizi, Sadiqova Farida Yaxshimurotovna, Saidmatova Muattar Ozodovna, Saparmatova Sadoqat Madiyor qizi, Xo'jaeva Shahnoza Farhodovna."
        "\n- Texnologiya va Kasbiy ta'lim: Boltayeva Zebo Hasanovna, Eshchanova Nodira Erkinovna, Matkarimova Intizor Rustamovna, Matyoqubova Xusniobod Ergashboyevna, Sobirov Ollayor Ro'zmetovich."
        "\n- San'at va Musiqa: O'razmetov O'tkir Karimboyevich (Musiqa), Xusainov Sodiqjon Bobojonovich (Musiqa), Otamuratov Rustam Odamboyevich (Tasv. san'at), SOBIROVA MALOXAT MUROD QIZI (Chizmachilik/Tasv. san'at)."
        "\n- Jismoniy tarbiya: Pirnnazarov Nurali Qo'shnazarovich, Ro`zmetova Muhtarama Ollashukur qizi, Xudaynazarov Davronbek Sotimboyevich, Yusupova Zuhraxon Urazbay Qizi."
        "\n- Boshqa: Madaminov Baxtiyor (Iqtisod), OTABOYEV XUDOYOR (Huquq), Quranboyeva Nafosat (Informatika)."
        "\n\nManzil: Yangiariq tumani, Po'rsang mahallasi. Aloqa: +998975156307. "
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
