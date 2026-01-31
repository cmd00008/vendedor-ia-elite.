import streamlit as st
import google.generativeai as genai
import time
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Gemini 2.5 Flash Elite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS FUTURISTA E RESPONSIVO ---
st.markdown("""
<style>
    /* 1. FUNDO GRADIENTE AZUL (Baseado na imagem) */
    .stApp {
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364); /* Gradiente Azul Profundo */
        background-attachment: fixed;
    }
    
    /* Ocultar elementos padrão do Streamlit para limpar o visual */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Forçar texto branco globalmente */
    h1, h2, h3, h4, h5, h6, p, span, div, li, label, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* ============================================================
       ÁREA SUPERIOR FLUTUANTE (Robô + Input)
    ============================================================ */
    /* Container que agrupa o robô e o input */
    .floating-header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 40px; /* Espaço do topo */
        margin-bottom: 30px; /* Espaço para o chat abaixo */
    }

    /* Ícone do Robô Central */
    .robot-icon-img {
        width: 100px; /* Tamanho bom para mobile e PC */
        margin-bottom: 20px;
        filter: drop-shadow(0px 0px 10px rgba(79, 172, 254, 0.7)); /* Brilho azul */
    }

    /* Estilização da Barra de Pesquisa "How can I help you?" */
    /* Esconde o label padrão */
    .stTextInput label { display: none; }
    
    /* A caixa de input em si */
    .stTextInput input {
        background-color: #000000 !important; /* Fundo Preto */
        color: #FFFFFF !important; /* Texto Branco */
        border: 2px solid #4facfe !important; /* Borda Azul Brilhante */
        border-radius: 50px !important; /* Bordas Redondas */
        padding: 15px 25px !important; /* Espaçamento interno */
        font-size: 18px !important; /* Texto maior */
        box-shadow: 0px 0px 20px rgba(79, 172, 254, 0.5); /* Sombra Azul */
        text-align: center; /* Texto centralizado */
    }
    /* Placeholder (Texto de ajuda) */
    ::placeholder {
        color: #a0a0a0 !important;
        font-style: italic;
    }
    
    /* Responsividade do Input: Mais largo no PC, mais estreito no Mobile */
    div[data-testid="stTextInput"] {
        width: 90%; /* Mobile: ocupa quase tudo */
        max-width: 600px; /* PC: limita a largura para não ficar gigante */
        margin: auto;
    }

    /* ============================================================
       ÁREA DO CHAT (Estável Abaixo)
    ============================================================ */
    /* Container para as mensagens */
    .chat-history-container {
        width: 90%;
        max-width: 800px;
        margin: auto; /* Centraliza no PC */
        padding-bottom: 50px;
    }
    
    /* Balões de Chat Transparentes/Vidro */
    div[data-testid="stChatMessage"] {
        background-color: rgba(0, 0, 0, 0.4); /* Fundo preto transparente */
        border: 1px solid rgba(79, 172, 254, 0.2); /* Borda azul sutil */
        border-radius: 15px;
        margin-bottom: 10px;
    }
    
    /* Avatar do usuário e modelo */
    .stChatMessageAvatar {
        border: 2px solid #4facfe;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# BACKEND (RESTORED by Antigravity)
# -----------------------------------------------------------------------------

# 1. VISUAL DO CABEÇALHO (HTML)
st.markdown("""
<div class="floating-header-container">
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" class="robot-icon-img">
</div>
""", unsafe_allow_html=True)

# 2. CONEXÃO BLINDADA
try:
    api_key = os.environ.get("GOOGLE_API_KEY") 
    if not api_key:
        api_key = st.secrets["GOOGLE_API_KEY"]
    
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.error("⚠️ API Key não encontrada.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ Erro de Configuração: {e}")
    st.stop()

# 3. CÉREBRO DA IA (Gemini 2.5)
system_instruction = """
Você é o CDM, a IA de Vendas Elite (v2.5).
REGRA DE IDIOMA: Responda SEMPRE no idioma que o usuário falar.
Seja direto, use emojis e foque em ajudar.
"""
# Usando o modelo funcional 2.5
model = genai.GenerativeModel('models/gemini-2.5-flash', system_instruction=system_instruction)

# 4. LÓGICA DO CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "model", "content": "Olá! Sistema Online. Como posso ajudar? 🤖"})

# 5. INPUT FLUTUANTE (Centralizado)
# O input fica logo abaixo do robô visualmente (devido ao CSS)
prompt = st.text_input("How can I help you?", placeholder="How can I help you?...", key="main_input")

# 6. EXIBIÇÃO DO CHAT (Abaixo do Input)
st.markdown('<div class="chat-history-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    avatar_icon = "🤖" if message["role"] == "model" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])
st.markdown('</div>', unsafe_allow_html=True)

# 7. PROCESSAMENTO
if prompt:
    # Adiciona msg usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Prepara histórico
        chat_history = [
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ]
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(prompt)
        
        st.session_state.messages.append({"role": "model", "content": response.text})
        
        # Recarregar para atualizar a tela e 'limpar' o input (fluxo pseudo-chat)
        st.rerun()
        
    except Exception as e:
        st.error(f"Erro: {e}")
