import streamlit as st
import google.generativeai as genai
import os
import base64

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(
    page_title="IA Vendas Elite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS: VISUAL FUTURISTA ---
st.markdown("""
<style>
    /* FUNDO AZUL PROFUNDO */
    .stApp {
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }
    
    /* FORÇAR TEXTO BRANCO */
    h1, h2, h3, h4, h5, h6, p, span, div, li, label, .stMarkdown, input, button {
        color: #FFFFFF !important;
    }

    /* FOTO DE PERFIL (CÍRCULO FLUTUANTE) */
    .profile-container {
        display: flex;
        justify-content: center;
        padding-top: 20px;
        padding-bottom: 20px;
    }
    .profile-img {
        width: 140px; 
        height: 140px;
        border-radius: 50%;          /* Círculo Perfeito */
        object-fit: cover;           /* Foca no rosto */
        object-position: top center; /* Garante que o boné/rosto apareça */
        border: 4px solid #4facfe;   /* Borda Neon */
        box-shadow: 0px 0px 25px rgba(79, 172, 254, 0.6);
        animation: float 6s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    /* BOTÃO ENVIAR (NEON) */
    .stButton button {
        background-color: #4facfe !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 30px !important;
        font-weight: bold !important;
        width: 100%;
        text-transform: uppercase;
        box-shadow: 0px 0px 15px rgba(79, 172, 254, 0.5) !important;
    }
    .stButton button:hover {
        background-color: #00f2fe !important;
        transform: scale(1.02);
    }

    /* INPUT DE TEXTO */
    .stTextInput input {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #4facfe !important;
        border-radius: 50px !important;
        text-align: center;
        padding: 15px !important;
    }
    /* Remove margem extra do input para colar no botão */
    div[data-testid="stTextInput"] { margin-bottom: -10px; }

    /* BALÕES DO CHAT */
    div[data-testid="stChatMessage"] {
        background-color: rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONEXÃO ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ API Key não configurada.")
    st.stop()

# Configuração do Modelo
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="Você é o CDM, IA de Vendas Elite. Responda no idioma do usuário.")

# --- 4. MEMÓRIA ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "Olá! Sou o CDM. Como posso ajudar a escalar suas vendas hoje? 🚀"}]

# --- 5. LÓGICA DA FOTO (AUTOMÁTICA) ---
st.markdown('<div class="profile-container">', unsafe_allow_html=True)

# O Código procura SOZINHO pelo arquivo "perfil.jpg"
image_path = "perfil.jpg"

if os.path.exists(image_path):
    # SE ACHAR O ARQUIVO: Mostra a foto do homem
    with open(image_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    st.markdown(f'<img src="data:image/jpeg;base64,{encoded}" class="profile-img">', unsafe_allow_html=True)
else:
    # SE NÃO ACHAR: Mostra o robô (Fallback de segurança)
    st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" class="profile-img">', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- 6. FORMULÁRIO DE CHAT (INPUT + BOTÃO ENVIAR) ---
# O st.form corrige o problema de "não ter botão de enter" no celular
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Sua mensagem", placeholder="Digite sua pergunta aqui...", label_visibility="collapsed")
    submit_button = st.form_submit_button("ENVIAR 🚀")

# --- 7. PROCESSAMENTO ---
if submit_button and user_input:
    # 1. Adiciona pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. Gera resposta
    try:
        chat_hist = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages if m["role"] != "user" or m["content"] != user_input]
        chat = model.start_chat(history=chat_hist)
        response = chat.send_message(user_input)
        st.session_state.messages.append({"role": "model", "content": response.text})
        st.rerun() # Atualiza a tela para mostrar a resposta
    except Exception as e:
        st.error(f"Erro: {e}")

# --- 8. EXIBIR HISTÓRICO ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    avatar = "⚡" if msg["role"] == "model" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)
