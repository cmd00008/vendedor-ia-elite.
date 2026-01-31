import streamlit as st
import google.generativeai as genai
import os
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Gemini 2.5 Flash Elite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS: ANIMAÇÃO DE LEVITAÇÃO E CORREÇÃO VISUAL ---
st.markdown("""
<style>
    /* 1. FUNDO GRADIENTE FUTURISTA */
    .stApp {
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }
    
    /* Limpeza da Interface */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Texto Branco Global */
    h1, h2, h3, h4, h5, h6, p, span, div, li, label, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* 2. ANIMAÇÃO DE LEVITAÇÃO (FLUTUAR) */
    @keyframes float {
        0% { transform: translatey(0px); }
        50% { transform: translatey(-20px); } /* Sobe 20px */
        100% { transform: translatey(0px); }
    }
    
    .robot-float {
        animation: float 6s ease-in-out infinite; /* Animação infinita suave */
        width: 120px;
        margin-bottom: 20px;
        filter: drop-shadow(0px 0px 15px rgba(79, 172, 254, 0.6)); /* Brilho neon */
    }

    /* 3. CONTAINER DO TOPO (Robô + Input) */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 30px;
        margin-bottom: 20px;
        padding: 20px;
    }

    /* 4. ESTILO DA BARRA DE DIGITAÇÃO (Igual Search Bar) */
    .stTextInput label { display: none; }
    
    .stTextInput input {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #4facfe !important;
        border-radius: 50px !important;
        padding: 15px 25px !important;
        font-size: 18px !important;
        box-shadow: 0px 0px 15px rgba(79, 172, 254, 0.3);
        text-align: center;
    }
    
    /* Responsividade da Barra */
    div[data-testid="stTextInput"] {
        width: 90%;
        max-width: 600px;
        margin: auto;
    }

    /* 5. ÁREA DO CHAT (Abaixo) */
    .chat-container {
        width: 90%;
        max-width: 800px;
        margin: auto;
        padding-bottom: 50px;
    }
    
    div[data-testid="stChatMessage"] {
        background-color: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
    }

</style>
""", unsafe_allow_html=True)

# --- CONEXÃO COM A IA (BLINDADA) ---
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

# --- MODELO (GEMINI 2.5) ---
system_instruction = """
Você é o CDM, IA de Vendas Elite (v2.5).
Responda sempre no idioma do usuário. Seja direto e futurista.
"""
# Usando o modelo funcional 2.5
model = genai.GenerativeModel('models/gemini-2.5-flash', system_instruction=system_instruction)

# --- INICIALIZAÇÃO DE VARIÁVEIS ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "model", "content": "Olá! Sistema Online. Como posso ajudar? 🤖"})

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None

# --- FUNÇÃO MÁGICA PARA CORRIGIR O INPUT (CALLBACK) ---
def process_input():
    # Pega o texto digitado
    user_text = st.session_state.widget_input
    if user_text:
        # Salva na memória temporária para processar
        st.session_state.last_prompt = user_text
        # LIMPA O CAMPO VISUALMENTE IMEDIATAMENTE (Resolve o bug)
        st.session_state.widget_input = ""

# --- LAYOUT VISUAL ---

# 1. IMAGEM FLUTUANTE (HTML Puro para aplicar a animação CSS)
st.markdown("""
<div class="header-container">
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" class="robot-float">
</div>
""", unsafe_allow_html=True)

# 2. INPUT CENTRAL COM CALLBACK
st.text_input("Pergunta", key="widget_input", on_change=process_input)

# 3. EXIBIÇÃO DO CHAT
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    avatar_icon = "🤖" if message["role"] == "model" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])
st.markdown('</div>', unsafe_allow_html=True)

# 4. PROCESSAMENTO PÓS-CALLBACK
if st.session_state.last_prompt:
    prompt = st.session_state.last_prompt
    # Limpa o last_prompt para não repetir no próximo rerun
    st.session_state.last_prompt = None 
    
    # Adiciona msg usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Processa resposta
    try:
        chat_history = [
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ]
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(prompt)
        
        st.session_state.messages.append({"role": "model", "content": response.text})
        
        # Rerun para atualizar a tela com a nova resposta
        st.rerun()
        
    except Exception as e:
        st.error(f"Erro: {e}")
