import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 1. Sahifa sozlamalari
st.set_page_config(
    page_title="19-son Maktab AI",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS Dizayn
css_style = """
<style>
    .stApp {
        background: linear-gradient(rgba(14, 17, 23, 0.7), rgba(14, 17, 23, 0.85)), 
                    url("https://images.unsplash.com/photo-1624200424564-94bc02bc9242?q=80&w=1920") no-repeat center center fixed;
        background-size: cover;
    }
    .main-container {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
        text-align: center;
    }
    .main-title { color: #ffffff; font-size: 38px; font-weight: 800; }
    .welcome-text { color: #00e5ff; font-size: 24px; font-weight: 600; }
    .emaktab-container {
        background: rgba(0, 229, 255, 0.05);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin-top: 15px;
    }
    .stChatInputContainer {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
    }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# Hafta kunlarini o'zbekchaga o'girish funksiyasi
def bugungi_hafta_kuni():
    kunlar = {
        0: "Dushanba", 1: "Seshanba", 2: "Chorshanba", 
        3: "Payshanba", 4: "Juma", 5: "Shanba", 6: "Yakshanba"
    }
    return kunlar[datetime.now().weekday()]

# 3. Session State
if "user_name" not in st.session_state: st.session_state.user_name = None
if "excel_rows" not in st.session_state: st.session_state.excel_rows = None
if "messages" not in st.session_state: st.session_state.messages = []

# 4. Foydalanuvchi interfeysi
if st.session_state.user_name is None:
    st.markdown('<div class="main-container"><div class="main-title">🏫 19-SON MAKTAB AI</div></div>', unsafe_allow_html=True)
    ism = st.text_input("Iltimos, ismingizni kiriting:", key="name_input")
    if st.button("Kirish"):
        if ism.strip():
            st.session_state.user_name = ism.strip()
            st.rerun()
else:
    st.markdown(f'<div class="main-container"><div class="main-title">🏫 19-SON MAKTAB AI</div><div class="welcome-text">Salom, {st.session_state.user_name}! 👋</div></div>', unsafe_allow_html=True)

    # e-Maktab Excel faylini yuklash
    if st.session_state.excel_rows is None:
        with st.expander("📊 REAL e-Maktab Excel faylini yuklash", expanded=True):
            uploaded_file = st.file_uploader("Excel faylni tanlang (.xlsx)", type=["xlsx"])
            
            if uploaded_file is not None:
                with st.spinner("Excel tahlil qilinmoqda..."):
                    try:
                        df = pd.read_excel(uploaded_file)
                        saqlangan_qatorlar = []
                        
                        for index, row in df.iterrows():
                            # Qatordagi ma'lumotlarni chiroyli formatda yig'amiz
                            elementlar = []
                            for k, v in row.items():
                                if pd.notna(v):
                                    v_str = str(v).strip()
                                    # Ustun nomlariga qarab chiroyli o'zbekcha nom beramiz
                                    if "Unnamed: 1" in str(k): k_name = "Fan"
                                    elif "Unnamed: 2" in str(k): k_name = "Baho"
                                    elif "Unnamed: 3" in str(k): k_name = "Vazifa"
                                    else: k_name = str(k).replace("Дневник", "Ma'lumot")
                                    
                                    elementlar.append(f"<b>{k_name}:</b> {v_str}")
                                    
                            qator_matni = " | ".join(elementlar)
                            saqlangan_qatorlar.append(qator_matni)
                        
                        st.session_state.excel_rows = saqlangan_qatorlar
                        st.success("Excel muvaffaqiyatli o'qildi!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Xatolik: {e}")
    else:
        st.sidebar.markdown(f'<div class="emaktab-container"><h4>🟢 Excel yuklangan</h4><p>O\'quvchi: {st.session_state.user_name}</p></div>', unsafe_allow_html=True)
        if st.sidebar.button("Faylni almashtirish"):
            st.session_state.excel_rows = None
            st.rerun()

    # Chat tarixi
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # Savol-javob paneli
    if prompt := st.chat_input("Savolingizni yozing..."):
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        query = prompt.lower().strip()
        response = ""
        bugun = bugungi_hafta_kuni()

        # --- YANGI KUCHAYTIRILGAN BUGUNGI DARSLAR FILTRI ---
        if st.session_state.excel_rows is not None and ("bugun" in query or "darslarim" in query or "darsni" in query):
            topilgan_darslar = []
            kun_topildi = False
            sanoq = 0
            
            for qator in st.session_state.excel_rows:
                # Agar bugungi kun nomi (masalan, Juma) topilsa, belgini True qilamiz
                if bugun.lower() in qator.lower():
                    kun_topildi = True
                    topilgan_darslar.append(qator)
                    continue
                
                # Kun topilgandan keyingi keladigan dars qatorlarini yig'amiz
                if kun_topildi:
                    # Agar keyingi satrda yangi kun boshlansa (masalan Shanba yoki Dushanba), to'xtaymiz
                    if "dushanba" in qator.lower() or "seshanba" in qator.lower() or "chorshanba" in qator.lower() or "payshanba" in qator.lower() or "juma" in qator.lower() or "shanba" in qator.lower():
                        break
                    
                    if qator.strip() and sanoq < 7: # Maksimal 7 ta darsni oladi
                        topilgan_darslar.append(qator)
                        sanoq += 1
            
            if topilgan_darslar:
                darslar_html = "<br>".join([f"• {d}" for d in topilgan_darslar])
                response = f"{st.session_state.user_name}, <b>bugun haftaning {bugun} kuni</b>. Excel faylingdan olingan bugungi darslar jadvali va vazifalar:<br><br>{darslar_html}"
            else:
                yaqin_darslar = "<br>".join([f"• {d}" for d in st.session_state.excel_rows[:6]])
                response = f"{st.session_state.user_name}, bugun haftaning {bugun} kuni. Fayldan kunni ajratishda xato bo'ldi, lekin umumiy jadval mana:<br><br>{yaqin_darslar}"

        # --- BOSHQA SAVOLLAR ---
        elif st.session_state.excel_rows is not None and ("baho" in query or "baxolar" in query or "hamma" in query or "jadval" in query):
            hamma_matn = "<br>".join([f"• {d}" for d in st.session_state.excel_rows[:15]])
            response = f"{st.session_state.user_name}, sening yuklangan faylingdagi ma'lumotlar:<br>{hamma_matn}"

        elif "direktor" in query or "eshmetov" in query:
            response = f"{st.session_state.user_name}, maktabimiz direktori — Eshmetov Rustambay Ollaberganovich."
        elif "yaratgan" in query or "muallif" in query or "husniddin" in query:
            response = f"Meni 8-B sinf o'quvchisi Saparboyev Husniddin va maktab jamoasi yaratgan."
        else:
            if st.session_state.excel_rows is None:
                response = f"e-Maktab ma'lumotlarini ko'rish uchun avval fayl yuklang."
            else:
                response = f"{st.session_state.user_name}, e-Maktab ma'lumotlaringiz yuklangan. Mendan 'bugungi darslarimni ayt' deb so'rang."

        with st.chat_message("assistant"): st.markdown(response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
