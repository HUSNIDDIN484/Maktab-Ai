import streamlit as st
from streamlit_google_auth import Authenticate
import g4f

# Sahifa sozlamalari
st.set_page_config(page_title="19-son Maktab AI", page_icon="🤖", layout="wide")

# Avtentifikatsiya sozlamalari
# image_1d9f02.png kabi o'rnatish xatolarini oldini olish uchun 2.0.0 versiya parametrlari
auth = Authenticate(
    cookie_name="maktab_ai_session",
    cookie_key=st.secrets["auth"]["cookie_secret"],
    client_id=st.secrets["auth"]["client_id"],
    client_secret=st.secrets["auth"]["client_secret"],
    redirect_uri="https://maktab-ai.streamlit.app/oauth2callback"
)

# Avtentifikatsiyani tekshirish
auth.check_authenticity()

# Asosiy interfeys
if st.session_state.get("connected"):
    # Sidebar qismi
    st.sidebar.image("https://img.icons8.com/fluency/96/user-male-circle.png", width=80)
    st.sidebar.write(f"### Xush kelibsiz!")
    st.sidebar.write(f"**{st.session_state.get('name')}**")
    st.sidebar.write(f"*{st.session_state.get('email')}*")
    
    if st.sidebar.button("Chiqish", use_container_width=True):
        auth.logout()

    # Asosiy chat oynasi
    st.title("🤖 19-son Maktab AI")
    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat tarixini chiqarish
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Foydalanuvchi kiritishi
    if prompt := st.chat_input("Savolingizni bu yerga yozing..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # g4f orqali javob olish
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4,
                    messages=[{"role": "user", "content": prompt}],
                )
                if response:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("AI javob bera olmadi. Iltimos, qaytadan urinib ko'ring.")
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {str(e)}")
else:
    # Kirish oynasi
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=100)
        st.title("Maktab AI")
        st.info("Ilovadan foydalanish uchun Google hisobingiz orqali tizimga kiring.")
        auth.login()
