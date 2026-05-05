import streamlit as st
import g4f

# Sahifa sozlamalari
st.set_page_config(page_title="19-son Maktab AI", page_icon="🤖")

st.title("🤖 19-son Maktab AI")
st.write("Xush kelibsiz! Savolingizni pastga yozishingiz mumkin.")

# Chat tarixini saqlash uchun xotira
if "messages" not in st.session_state:
    st.session_state.messages = []

# Avvalgi yozishmalarni ekranga chiqarish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Foydalanuvchi xabarini qabul qilish
if prompt := st.chat_input("Qanday yordam bera olaman?"):
    # Foydalanuvchi xabarini xotiraga qo'shish
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI javobini generatsiya qilish
    with st.chat_message("assistant"):
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=[{"role": "user", "content": prompt}],
            )
            if response:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.error("AI hozircha javob bera olmadi, iltimos qaytadan urinib ko'ring.")
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {e}")
