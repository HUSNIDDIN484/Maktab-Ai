import streamlit as st
import g4f

# Sarlavha
st.title("🤖 Maktab AI")

# Xabarlar xotirasi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tarixni ko'rsatish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Savol kiritish
if prompt := st.chat_input("Savolingizni yozing..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # AI javobi
    with st.chat_message("assistant"):
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=[{"role": "user", "content": prompt}],
            )
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error("Ulanishda xato bo'ldi, qaytadan urinib ko'ring.")
