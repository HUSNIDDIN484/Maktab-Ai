import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- Dizayn va Orqa Fon ---
# Bu yerda background-image qismida talabalar va maktab binosi aks etgan sifatli rasm ishlatilgan
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url("https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .title { 
        color: #FFFFFF; 
        text-align: center; 
        font-size: 36px; 
        font-weight: bold; 
        padding: 20px;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    /* Xabarlar oynasini shaffof va o'qishga qulay qilish */
    .user-msg { 
        background-color: rgba(38, 39, 48, 0.85); 
        padding: 15px; 
        border-radius: 15px; 
        margin: 10px 0; 
        border-right: 5px solid #3B8ED0;
        color: white;
    }
    .ai-msg { 
        background-color: rgba(30, 30, 30, 0.85); 
        padding: 15px; 
        border-radius: 15px; 
        border-left: 5px solid #3B8ED0; 
        margin: 10px 0;
        color: white;
    }
    /* Kirish maydonini ham moslashtirish */
    .stChatInputContainer {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Funksiyasi ---
def get_ai_response(prompt):
    system_instructions = (
        "Sening isming - Maktab AI. Sen 19-sonli maktab yordamchisisan. "
        "Seni 8-B sinf o'quvchisi Saparboyev Husniddin yaratgan. "
        "Google haqida gapirma. Matematika, fizika va boshqa fanlardan yordam ber. "
        "Imlo xatolarisiz, rasmiy tilda javob ber."
        "\n\n--- USTOZLAR ---"
        "\nDirektor: Eshmetov Rustambay. O'rinbosarlar: Bekchanov A, Jalilov E, Salayev M."
        "\nMatematika: Egamova R, Iskandarova D, Matkarimova M, Quramboyeva O, Xudaynazarova Z."
        "\nIngliz tili: Eshmurodova R, Farxodova M, Qo'shoqova G, Rajabova L, Raxmanova S, Sadullayeva D."
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
            return res_str.replace("Google", "19-son maktab jamoasi").replace("Aria", "Maktab AI")
        return "Serverda vaqtincha uzilish bor."
    except Exception:
        return "Xatolik yuz berdi, qayta urinib ko'ring."

# --- Chat tarixi ---
for msg in st.session_state.messages:
    role_name = "Siz" if msg["role"] == "user" else "Maktab AI"
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{role_name}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"], use_container_width=True)

# --- Kirish maydoni ---
user_input = st.chat_input("Savol yozing yoki rasm uchun 'Rasm: [tarif]' deb yozing...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    input_lower = user_input.lower()
    if any(keyword in input_lower for keyword in ["rasm:", "chiz:", "rasm ber"]):
        img_desc = user_input.replace("rasm:", "").replace("chiz:", "").replace("rasm ber", "").strip()
        if not img_desc: img_desc = "talaba o'quvchi"
            
        with st.spinner("Rasm tayyorlanmoqda..."):
            encoded = urllib.parse.quote(img_desc)
            img_url = f"https://image.pollinations.ai/prompt/school_style_{encoded}?width=1024&height=1024&nologo=true"
            st.session_state.messages.append({"role": "ai", "content": f"Siz so'ragan '{img_desc}' rasmi tayyor:", "image": img_url})
    else:
        with st.spinner("Javob tayyorlanmoqda..."):
            answer = get_ai_response(user_input)
            st.session_state.messages.append({"role": "ai", "content": answer})
    
    st.rerun()
