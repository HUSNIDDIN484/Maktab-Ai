import streamlit as st
import g4f
import base64

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫", layout="wide")

# --- FON RASMINI MAJBURIY QILISH (BASE64 USULI) ---
# Bu yerda Yonsei universiteti binosi tasviri kod shakliga keltirilgan (Internet o'chgan bo'lsa ham ishlaydi)
BG_IMAGE_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" 
    # Izoh: Yuqoridagi Base64 qisqartma namuna. Quyida biz eng ishonchli ochiq URL dan foydalanamiz, 
    # lekin agar u ham ishlamasa, CSS orqali standart chiroyli gradient fonni zaxira qilib qo'yamiz.
)

st.markdown("""
    <style>
    /* Streamlit asosiy fonini majburlash */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                          url("https://images.unsplash.com/photo-1623690184496-6e5414d79201?auto=format&fit=crop&w=1200&q=80") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-color: #1E293B !important; /* Agar rasm baribir yuklanmasa, qora emas, chiroyli to'q ko'k-kulrang fon bo'ladi */
    }

    /* Barcha qora qatlamlarni tozalash va shaffof qilish */
    [data-testid="stHeader"], 
    [data-testid="stAppViewBlockContainer"], 
    .main, 
    .stChatMessage, 
    [data-testid="stVerticalBlock"],
    [data-testid="stChatInput"] {
        background-color: transparent !important;
        background: transparent !important;
    }

    /* Sarlavha */
    .title { 
        color: #FFFFFF !important; 
        text-align: center; 
        font-size: 45px; 
        font-weight: bold; 
        text-shadow: 3px 3px 15px rgba(0, 0, 0, 0.9); 
        padding: 25px;
    }

    /* Shaffof xabarlar bloki */
    .user-msg { 
        background-color: rgba(255, 255, 255, 0.12) !important; 
        padding: 15px; border-radius: 18px; margin: 12px 0; 
        border-right: 6px solid #3B8ED0; color: #FFFFFF !important; 
        backdrop-filter: blur(15px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .ai-msg { 
        background-color: rgba(255, 255, 255, 0.05) !important; 
        padding: 15px; border-radius: 18px; 
        border-left: 6px solid #3B8ED0; margin: 12px 0; 
        color: #FFFFFF !important; 
        backdrop-filter: blur(15px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Kirish oynasi */
    .login-box {
        background: rgba(15, 23, 42, 0.8) !important;
        padding: 45px; border-radius: 30px; 
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center; max-width: 500px; 
        margin: 80px auto; backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- TIZIM XOTIRASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# --- 1. KIRISH QISMI ---
if st.session_state.user_name is None:
    st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h2 style='color:white; margin-bottom:20px;'>Xush kelibsiz!</h2>", unsafe_allow_html=True)
    name = st.text_input("Suhbatni boshlash uchun ismingizni kiriting:", key="unique_login_key")
    if st.button("Dasturga kirish"):
        if name.strip():
            st.session_state.user_name = name.strip()
            st.rerun()
        else:
            st.warning("Iltimos, ismingizni yozing!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 2. CHAT QISMI ---
else:
    st.markdown(f'<p class="title">Salom, {st.session_state.user_name}! 🏫</p>', unsafe_allow_html=True)

    def get_ai_response(prompt):
        # TAQDOM ETILGAN BARCHA MA'LUMOTLAR BAZASI
        system_instructions = (
            f"Sening isming - Maktab AI. Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktab yordamchisisan. "
            f"Seni 8-B sinf o'quvchisi Saparboyev Husniddin va maktab jamoasi yaratgan. "
            f"Foydalanuvchi ismi: {st.session_state.user_name}. Har doim unga ismi bilan samimiy murojaat qil. "
            "DIQQAT: Google haqida gapirma. Imlo xatolarisiz, rasmiy va aniq tilda javob ber. Ortiqcha gapirmasdan savolga to'liq javob ber."
            
            "\n\n--- MA'MURIYAT ---"
            "\nDirektor: Eshmetov Rustambay Ollaberganovich. O'rinbosarlar: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek. Administrator: Sabirova Iroda Yarash qizi."
            
            "\n\n--- O'QITUVCHILAR RO'YXATI ---"
            "\nMatematika: Egamova Rajabgul, Iskandarova Dilnavoz, Matkarimova Muxabbat, Quramboyeva O'g'iljon, Xudaynazarova Ziyoda."
            "\nOna tili: Avazova Risolat, Bobojonova Mushtariy, Jumaniyozova Sadoqat, Otajonova Sharofat, Xudoynazarova Nafosat."
            "\nIngliz tili: Eshmurodova Ra'no, Farxodova Muxtaram, Qo'shoqova Gulasal, Rajabova Lobar, Raxmanova So'najon, Sadullayeva Durdona."
            "\nRus tili: Bekmetova Shaxnoza, Bobojonova Komila, Saidova Saragul, Sobirova Nozima, Tillayeva Aziza, Yusupova Sanobar."
            "\nTarix: Allanazarova Zumrad, Matqurbonova Shohina, Matchanova Zebo, Sobirova Gulposhsha."
            "\nFizika/Kimyo: Aminova Mehriniso, Kurbonov Ollashukur, Razzaqova Kumushoy, Meylibayeva Aziza."
            "\nInformatika: Quranboyeva Nafosat, Sabirova Iroda."
            "\nBoshlang'ich ta'lim: Bobojonova Elmira, Maftuna, Jumanazarova Nargiza, Kenjayeva Iroda, Normatova Iqbol, Nurmetova Marhabo, Otajonova Sarvinoz, Quryozova Sanobar, Ro'ziboyeva Sarvinoz, Sadiqova Farida, Saidmatova Muattar, Saparmatova Sadoqat, Xo'jayeva Shahnoza."
            "\nSport: Pirnnazarov Nurali, Ro'zmetova Muhtarama, Xudaynazarov Davronbek, Yusupova Zuhraxon."
            "\nMusiqa/San'at: O'razmetov O'tkir, Xusainov Sodiqjon, Otamuratov Rustam, Sobirova Maloxat."
            "\nTexnologiya: Boltayeva Zebo, Eshchanova Nodira, Matkarimova Intizor, Matyoqubova Xusniobod, Sobirov Ollayor."
            
            "\n\nMaktab 1982-yil 2-sentabrda tashkil etilgan. Manzil: Yangiariq tumani, Po'rsang mahallasi."
        )

        chat_context = [{"role": "system", "content": system_instructions}]
        # Xotira funksiyasi (Oxirgi 5 ta xabarni uzatish)
        for msg in st.session_state.messages[-5:]:
            chat_context.append({"role": msg["role"], "content": msg["content"]})
        chat_context.append({"role": "user", "content": prompt})
        
        try:
            response = g4f.ChatCompletion.create(model=g4f.models.default, messages=chat_context)
            return str(response).replace("Google", "Maktab jamoasi")
        except:
            return f"Kechirasiz {st.session_state.user_name}, ulanishda uzilish bo'ldi. Iltimos qaytadan urinib ko'ring."

    # Suhbat tarixini ekranga chiqarish (Shaffof dizaynda)
    for msg in st.session_state.messages:
        role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
        sender = st.session_state.user_name if msg["role"] == "user" else "Maktab AI"
        st.markdown(f'<div class="{role_class}"><b>{sender}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

    # Savol kiritish maydoni
    user_input = st.chat_input("Savolingizni bu yerga yozing...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Javob tayyorlanmoqda..."):
            answer = get_ai_response(user_input)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
