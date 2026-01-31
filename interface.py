import streamlit as st
import google.generativeai as genai
import os # Added for robust auth

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Gemini 2.5 Flash Elite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS: ANIMAÇÕES E CORREÇÕES VISUAIS ---
st.markdown("""
<style>
    /* 1. FUNDO GRADIENTE ESCURO (Futurista) */
    .stApp {
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }
    
    /* Limpeza de elementos padrão */
    #MainMenu, footer, header {visibility: hidden;}
    h1, h2, h3, h4, h5, h6, p, span, div, li, label, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* 2. ANIMAÇÃO DE LEVITAÇÃO (ROBÔ) */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); } /* Sobe e desce suave */
        100% { transform: translateY(0px); }
    }
    .robot-float {
        animation: float 5s ease-in-out infinite; /* Loop infinito */
        width: 120px;
        display: block;
        margin-left: auto;
        margin-right: auto;
        filter: drop-shadow(0px 0px 20px rgba(79, 172, 254, 0.6)); /* Brilho Neon */
    }

    /* 3. SUBSTITUIR "PRESS ENTER" POR SETA PULSANTE (Mobile) */
    /* Esconde o texto pequeno */
    div[data-testid="InputInstructions"] > span {
        visibility: hidden !important;
    }
    /* Coloca a Seta Animada no lugar */
    div[data-testid="InputInstructions"]::after {
        content: "⏎"; 
        visibility: visible !important;
        display: block;
        font-size: 28px;
        color: #4facfe;
        font-weight: bold;
        margin-top: -25px;
        text-align: right;
        padding-right: 30px;
        animation: pulse-arrow 1.5s infinite;
    }
    @keyframes pulse-arrow {
        0% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.3); opacity: 1; text-shadow: 0px 0px 10px #4facfe; }
        100% { transform: scale(1); opacity: 0.5; }
    }

    /* 4. BARRA DE DIGITAÇÃO ESTILO "SEARCH" */
    .stTextInput label { display: none; }
    .stTextInput input {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #4facfe !important;
        border-radius: 50px !important;
        padding: 15px 20px !important;
        font-size: 18px !important;
        text-align: center;
        box-shadow: 0px 0px 15px rgba(79, 172, 254, 0.3);
    }
    
    /* Container do Chat */
    .chat-container {
        width: 95%;
        max-width: 800px;
        margin: auto;
        padding-bottom: 50px;
    }
    /* Balões do Chat */
    div[data-testid="stChatMessage"] {
        background-color: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- CONEXÃO SEGURA (BLINDADA) ---
try:
    api_key = os.environ.get("GOOGLE_API_KEY") # Tenta ambiente primeiro
    if not api_key:
        api_key = st.secrets["GOOGLE_API_KEY"] # Tenta secrets do Streamlit
    
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.error("⚠️ Configure a API Key nos Secrets.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ Erro de Configuração: {e}")
    st.stop()

# --- MODELO (Blindado com nome 2.5) ---
system_instruction = """
Você é o CDM, IA de Vendas Elite (v2.5).
Responda SEMPRE no idioma do usuário. Seja direto.
"""
# CORRECTED: gemini-1.5-flash -> models/gemini-2.5-flash
model = genai.GenerativeModel('models/gemini-2.5-flash', system_instruction=system_instruction)

# --- HISTÓRICO ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "Olá! Sistema Online. Como posso ajudar? 🤖"}]

# Controle do Input (para não travar loop)
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None

# --- FUNÇÃO DE LIMPEZA (CORREÇÃO DO BUG) ---
def process_input():
    # 1. Pega o texto
    if st.session_state.widget_input:
        st.session_state.last_prompt = st.session_state.widget_input
        # 2. LIMPA O CAMPO IMEDIATAMENTE
        st.session_state.widget_input = ""

# --- LAYOUT VISUAL ---

# 1. ROBÔ FLUTUANTE (HTML Puro para garantir animação)
st.markdown("""
<div style="padding: 20px;">
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" class="robot-float">
</div>
""", unsafe_allow_html=True)

# 2. INPUT DE TEXTO (Com Callback de Limpeza)
# Colocamos o input em uma coluna central para melhor visual em PC wide
col_sp1, col_inp, col_sp2 = st.columns([1, 6, 1])
with col_inp:
    st.text_input(
        "Input Oculto", 
        key="widget_input", 
        on_change=process_input, 
        placeholder="Digite aqui... ⏎"
    )

# 3. LÓGICA (Invisível)
if st.session_state.last_prompt:
    prompt = st.session_state.last_prompt
    
    # Adiciona usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Gera resposta
    try:
        # History setup
        chat_hist = []
        # Precisamos converter o histórico para o formato da API.
        # Filtramos para não enviar a mensagem atual duplicada se ela já estiver no state (embora logicamente não deveria no loop)
        for m in st.session_state.messages:
             # Exclude user's current prompt from 'history' passed to start_chat, as send_message takes it
             pass

        # Build clean history for start_chat
        valid_history = []
        for m in st.session_state.messages[:-1]: 
             valid_history.append({"role": m["role"], "parts": [m["content"]]})

        chat = model.start_chat(history=valid_history)
        response = chat.send_message(prompt)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
        # Rerun para atualizar a tela
        st.rerun()
        
    except Exception as e:
        st.error(f"Erro: {e}")
    
    # Reseta gatilho
    st.session_state.last_prompt = None

# 4. CHAT (Histórico Embaixo)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "model" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)
