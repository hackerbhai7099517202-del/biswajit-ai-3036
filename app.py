import streamlit as st
import google.generativeai as genai

# Website ka Title aur Look set karna (ChatGPT/Gemini Style)
st.set_page_config(page_title="BiswaJit AI", page_icon="🤖", layout="centered")

# Dark Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #111214; color: #e3e3e3; }
    h1 { text-align: center; color: #ffffff; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🤖 BiswaJit AI</h1>", unsafe_allow_html=True)
st.center = st.caption("⚡ Sawaal aapka, Sahi Jawab BiswaJit AI ka | Powered by Advanced AI")

# API Key Secrets se uthana (Takki safe rahe aur user ko baar-baar na dalna pade)
# Agar aap local computer par chala rahe hain, to sidebar me option diya hai
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.sidebar.title("🔑 Setup")
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

# Chat History Initialize karna
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Main BiswaJit AI hoon. Aap mujhse koi bhi sawaal pooch sakte hain, main aapko bilkul sahi aur accurate jawab doonga!"}
    ]

# Chat History ko screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User jab sawaal poochega
if prompt := st.chat_input("Yahan apna sawaal likhein..."):
    
    if not api_key:
        st.error("⚠️ AI active karne ke liye API Key zaroori hai!")
    else:
        # User ka sawaal screen par dikhana
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI se jawab mangna
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            try:
                # Gemini Advance Model Configure karna
                genai.configure(api_key=api_key)
                
                # Sahi aur accurate jawab dene ke liye instructions (System Prompt)
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-pro", # Ye sabse accurate aur naya model hai
                    system_instruction="You are BiswaJit AI, a highly intelligent, accurate, and helpful AI assistant. Answer every question correctly, clearly, and truthfully based on facts. If the user asks in Hindi/Hinglish, reply in Hindi/Hinglish."
                )
                
                # Jawab generate karna
                response = model.generate_content(prompt)
                ai_reply = response.text
                
                # Screen par jawab dikhana
                response_placeholder.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
            except Exception as e:
                st.error(f"Kuch dikkat aayi, please sahi API Key check karein. Error: {str(e)}")
