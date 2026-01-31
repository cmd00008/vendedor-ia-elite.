import streamlit as st
import google.generativeai as genai
import os
import base64
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="IA Vendas Elite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS: DESIGN FUTURISTA E FOTO REDONDA ---
st.markdown("""
<style>
    /* FUNDO GRADIENTE ESCURO */
    .stApp {
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }
    
    /* LIMPEZA GERAL */
    #MainMenu, footer, header {visibility: hidden;}
    h1, h2, h3, h4, h5, h6, p, span, div, li, label, .stMarkdown, input {
        color: #FFFFFF !important;
    }

    /* --- ESTILO DA FOTO REDONDA (PERFIL) --- */
    .profile-container {
        display: flex;
        justify-content: center;
        padding-top: 30px;
        padding-bottom: 20px;
    }
    
    .profile-img {
        width: 140px;          
        height: 140px;         
        border-radius: 50%;    /* Transforma quadrado em círculo */
        object-fit: cover;     /* Garante foco no rosto sem esticar */
        object-position: top center; /* Prioriza a parte de cima (rosto/boné) */
        border: 4px solid #4facfe;   /* Borda Neon */
        box-shadow: 0px 0px 25px rgba(79, 172, 254, 0.6);
        
        /* Animação de Flutuar */
        animation: float 6s ease-in-out infinite;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    /* --- BARRA DE DIGITAÇÃO --- */
    div[data-testid="InputInstructions"] { display: none; }
    .stTextInput label { display: none; }
    
    .stTextInput input {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #4facfe !important;
        border-radius: 50px !important;
        padding: 15px 25px !important;
        font-size: 18px !important;
        text-align: center;
        box-shadow: 0px 0px 15px rgba(79, 172, 254, 0.3);
    }
    
    /* Ajuste de largura responsivo */
    div[data-testid="stTextInput"] {
        width: 90%;
        max-width: 600px;
        margin: 0 auto;
    }

    /* --- CHAT --- */
    .chat-container {
        width: 95%;
        max-width: 800px;
        margin: auto;
        padding-bottom: 50px;
    }
    div[data-testid="stChatMessage"] {
        background-color: rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONEXÃO COM A IA (BLINDADA) ---
try:
    api_key = os.environ.get("GOOGLE_API_KEY") 
    if not api_key:
        api_key = st.secrets["GOOGLE_API_KEY"]
    
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.error("⚠️ Configure a API Key.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ Erro de Configuração: {e}")
    st.stop()

# Configuração do Cérebro (Prompt)
system_instruction = """
Você é o CDM, uma IA de Vendas de Elite.
Personalidade: Profissional, experiente (como um vendedor sênior), direto e persuasivo.
REGRA DE IDIOMA: Responda SEMPRE no idioma que o usuário falar.
"""
# ANTIGRAVITY FIX: models/gemini-2.5-flash
model = genai.GenerativeModel('models/gemini-2.5-flash', system_instruction=system_instruction)

# --- 4. MEMÓRIA ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "Olá! Sou o CDM. Estou pronto para escalar suas vendas."}]

# --- 5. LÓGICA DE EXIBIÇÃO DA FOTO (MANUAL) ---
# Tenta com jpg primeiro, mas permitimos png por robustez
image_file = "perfil.jpg"
if not os.path.exists(image_file) and os.path.exists("perfil.png"):
    image_file = "perfil.png"

html_code = ""

if os.path.exists(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        
    mime = "image/png" if image_file.endswith(".png") else "image/jpeg"
    html_code = f"""
    <div class="profile-container">
        <img src="data:{mime};base64,{encoded}" class="profile-img">
    </div>
    """
else:
    # Se você ainda não subiu a foto, mostra o robô como reserva
    html_code = """
    <div class="profile-container">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" class="profile-img">
    </div>
    """

st.markdown(html_code, unsafe_allow_html=True)

# --- 6. INPUT E PROCESSAMENTO (COM CORREÇÃO DE LOOP) ---
prompt = st.text_input("Input", key="user_input", placeholder="Digite sua pergunta aqui... ⏎")

if prompt:
    # Adiciona a pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Gera a resposta
    try:
        # History clean
        valid_history = [{"role": m["role"], "parts": [m["content"]]} 
                         for m in st.session_state.messages[:-1]]
        
        chat = model.start_chat(history=valid_history)
        response = chat.send_message(prompt)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
        # O TRUQUE: Limpa o input PROPRIAMENTE antes do rerun
        st.session_state["user_input"] = ""
        st.rerun() 
        
    except Exception as e:
        st.error(f"Erro: {e}")

# --- 7. EXIBIR CHAT ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    # Avatar: Raio para o Modelo, Boneco para o Usuário
    avatar = "⚡" if msg["role"] == "model" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)
