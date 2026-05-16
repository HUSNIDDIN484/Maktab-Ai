import streamlit as st
import g4f

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫", layout="wide")

# --- YONSEI UNIVERSITETI RASMI (BASE64 FORMATIDA) ---
BG_IMAGE_BASE64 = (
    "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsK"
    "CwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNDhQUFBQUFBQUFBQUFBQUFBQUFBQU"
    "FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAHgAoADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAEC"
    "AwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcY"
    "GRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ip"
    "qrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAx"
    "EEBSExBhJBUQdhcRMiMoEIFEKrobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVm"
    "Z2hpanN0d3eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erF"
    "1FSubXy8vP09fb3+Pn6/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEBCEFSMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2Jyggk"
    "KFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp"
    "6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9/KKKKACiiig"
    "AiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAii"
    "igAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAi"
    "iigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigA"
    "iiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAi"
    "iigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigA"
    "iiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiig"
    "AiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiii"
    "gAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiigAiiig childhood-dream"
)

# --- Dizayn va CSS (Glassmorphism va Shaffoflik) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: url("{BG_IMAGE_BASE64}") no-repeat center center fixed;
        background-size: cover;
    }}
    .glass-container {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 15px;
        border: 1px rgba(255, 255, 255, 0.15) solid;
        padding: 25px;
        color: white;
        margin-bottom: 20px;
    }}
    h1, h2, h3, p, label {{
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    .stTextInput>div>div>input {{
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        transition: 0.3s ease !important;
    }}
    .stButton>button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
    }}
    </style>
""", unsafe_allow_exists=True, unsafe_allow_html=True)

# --- Tizim ko'rsatmalari (System Prompt) ---
SYSTEM_INSTRUCTIONS = """
Siz Xorazm viloyati Yangiariq tumani 19-son maktab jamoasi (maktab jamoasi) tomonidan maxsus yaratilgan "Maktab AI" raqamli yordamchisiz.
Hech qachon OpenAI, Google yoki boshqa tijoriy kompaniyalar nomini tilga olmang. Kelib chiqishingiz haqida so'rashsa, faqat va faqat "19-son maktab jamoasi" tomonidan ishlab chiqilganingizni ayting.

Maktab haqida ma'lumotlar:
- Maktab nomi: Xorazm viloyati Yangiariq tumani 19-son umumiy o'rta ta'lim maktabi.
- Maktab ma'muriyati va o'qituvchilar:
  * Maktab direktori: Masharipov Maqsud.
  * Matematika o'qituvchilari: Saparboyeva Dilnoza, Jumaniyazov Quvondiq.
  * Ona tili va adabiyot: Rajabova Gulbahor.
  * Tarix: Davletov Jasur.
  * Ingliz tili: Madaminova Lola.

Foydalanuvchi suhbatni boshlashdan oldin o'z ismini kiritgan. Unga har doim xushmuomalalik bilan, ismi orqali murojaat qiling va maktab hayoti yoki darslar bilan bog'liq savollariga aniq javob bering.
"""

# --- Session State rejimlarini tekshirish ---
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================================
# 1-BOSQICH: ISM SO'RASH EKRANI (CHAT BOSHLANISHIDAN OLDIN)
# =========================================================================
if not st.session_state.chat_started:
    st.markdown('<div class="glass-container" style="text-align: center; max-width: 600px; margin: 100px auto;">', unsafe_allow_html=True)
    st.title("🏫 19-son Maktab AI")
    st.write("Tizimga kirish va suhbatni boshlash uchun ismingizni kiriting:")
    
    name_input = st.text_input("Ismingiz:", placeholder="Masalan: Husniddin", key="name_field")
    
    if st.button("Chatni boshlash"):
        if name_input.strip():
            st.session_state.user_name = name_input.strip()
            st.session_state.chat_started = True
            # Dastlabki salomlashishni qo'shish
            initial_greeting = f"Assalomu alaykum, {st.session_state.user_name}! Men 19-son maktab jamoasi tomonidan yaratilgan Maktab AI yordamchisiman. Sizga qanday yordam bera olaman?"
            st.session_state.messages.append({"role": "assistant", "content": initial_greeting})
            st.rerun()
        else:
            st.error("Iltimos, davom etish uchun ismingizni kiriting!")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# 2-BOSQICH: ASOSIY CHAT INTERFEYSI
# =========================================================================
else:
    # Sarlavha qismi
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.title("🏫 19-son Maktab AI raqamli yordamchisi")
    st.write(f"Foydalanuvchi: **{st.session_state.user_name}** | Ishlab chiquvchi: **Maktab jamoasi**")
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat tarixini ko'rsatish
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Foydalanuvchidan yangi savol qabul qilish
    if prompt := st.chat_input("Savolingizni bu yerga yozing..."):
        # Tarixga qo'shish
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI javobini generatsiya qilish
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # G4F uchun xabarlar kontekstini yig'ish (Tizim ko'rsatmasini har doim tepada saqlaymiz)
            api_messages = [{"role": "system", "content": SYSTEM_INSTRUCTIONS}]
            for msg in st.session_state.messages:
                api_messages.append({"role": msg["role"], "content": msg["content"]})
            
            try:
                # G4F yordamida modelga so'rov yuborish
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4,
                    messages=api_messages,
                    stream=True,
                )
                
                for delta in response:
                    if delta:
                        full_response += delta
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                full_response = f"Kechirasiz, {st.session_state.user_name}. Tizimda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
                message_placeholder.markdown(full_response)
            
            # Javobni tarixga saqlash
            st.session_state.messages.append({"role": "assistant", "content": full_response})
