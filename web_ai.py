import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- Dizayn (CSS) ---
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
    # O'QITUVCHILAR HAQIDA BARCHA MA'LUMOTLAR:
    system_instructions = (
        "Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan. "
        "Seni 8-b sinf oquvchisi Saparboyev Husniddin yaratgan. Maktab 1982-yil 2-sentabrda ochilgan. "
        "Faqat o'qituvchilar haqida so'ralganda ushbu ro'yxatni ishlat: "
        "\n--- MA'MURIYAT ---"
        "\n- Direktor: Eshmetov Rustambay. O'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek. "
        "\n- Administrator: Sabirova Iroda Yarash qizi. Psixolog: Xo'jayeva Dilorom, Xudaynazarova Dilbar."
        "\n--- FAN O'QITUVCHILARI ---"
        "\n- Tarix: Allanazarova Zumrad, Matqurbonova Shohina, Matchanova Zebo, Sobirova Gulposhsha. "
        "\n- Matematika: Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda. "
        "\n- Fizika: Aminova Mehriniso, Kurbonov Ollashukur. "
        "\n- Kimyo: Razzaqova Kumushoy, Meylibayeva Aziza. "
        "\n- Ona tili: Avazova Risolat, Bobojonova Mushtariy, Jumaniyozova Sadoqat, Otajonova Sharofat, Xudoynazarova Nafosat. "
        "\n- Chet tili: Inglizcha (Eshmurodova Ra'no, Farxodova Muxtaram, Qo'shoqova Gulasal, Rajabova Lobar, Raxmanova So'najon, Sadullayeva Durdona), Ruscha (Bekmetova Shaxnoza, Bobojonova Komila, Saidova Saragul, Sobirova Nozima, Tillayeva Aziza, Yusupova Sanobar), Fransuzcha (Kurbonova Nigora). "
        "\n- Boshlang'ich: Bobojonova Elmira, Maftuna, Jumanazarova Nargiza, Kenjayeva Iroda, Normatova Iqbol, Nurmetova Marhabo, Otajonova Sarvinoz, Quryozova Sanobar, Ro'ziboyeva Sarvinoz, Sadiqova Farida, Saidmatova Muattar, Saparmatova Sadoqat, Xo'jaeva Shahnoza. "
        "\n- Boshqalar: Pirnnazarov Nurali (Sport), Xudaynazarov Davronbek (Sport), Yusupova Zuhraxon (Sport), Ro'zmetova Muhtarama (Sport), O'razmetov O'tkir (Musiqa), Xusainov Sodiqjon (Musiqa), Otamuratov Rustam (Rasm), Sobirova Maloxat (Rasm), Boltayeva Zebo (Texno), Eshchanova Nodira (Texno), Matkarimova Intizor (Texno), Matyoqubova Xusniobod (Texno), Sobirov Ollayor (Texno), Madaminov Baxtiyor (Iqtisod), Otaboyev Xudoyor (Huquq), Quranboyeva Nafosat (Info). "
        "\nSavollarga faqat o'zbek tilida javob ber va o'zingni 'Maktab AI' deb tanishtir."
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
    except Exception:
        return "Server hozircha band, biroz kuting."

# --- Chat tarixi ---
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{msg["role"].title()}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# --- Kirish (Yuborish tugmasi bilan) ---
user_input = st.chat_input("Savol yozing (masalan: Matematika o'qituvchilari kim?)...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Javob tayyorlanmoqda..."):
        answer = get_ai_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
