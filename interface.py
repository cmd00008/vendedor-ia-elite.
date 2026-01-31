import streamlit as st
import time
import os
import google.generativeai as genai

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="IA Vendas Elite | Sistema Neural",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. DESIGN SYSTEM (CSS "Neural" - Visual Futurista & Correção Mobile)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* FONTE IMPORTADA (Rajdhani para títulos técnicos, Inter para leitura) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Rajdhani:wght@500;700&display=swap');

    /* CONFIGURAÇÃO GERAL */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }

    /* FUNDO PRINCIPAL (Background Imersivo) */
    .stApp {
        background-color: #050511;
        background-image: 
            radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
        background-attachment: fixed;
    }

    /* TÍTULOS */
    h1, h2, h3 {
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* O BLOCO CENTRAL DE CHAT (Vidro Escuro) */
    .block-container {
        background: rgba(10, 10, 20, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem !important;
        margin-top: 40px;
        box-shadow: 0 0 40px rgba(0, 0, 0, 0.5);
    }

    /* CABEÇALHO PERSONALIZADO */
    .header-style {
        text-align: center;
        padding-bottom: 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    
    .neon-text {
        background: linear-gradient(to right, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        text-shadow: 0 0 20px rgba(0, 114, 255, 0.3);
    }

    /* --- CORREÇÃO DE CHAT (CRÍTICO PARA MOBILE) --- */
    
    /* Mensagem da IA */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(0, 0, 0, 0.4);
        border: 1px solid #0072ff;
        border-radius: 4px 20px 20px 20px;
        box-shadow: 0 0 15px rgba(0, 114, 255, 0.1);
    }

    /* Mensagem do Usuário */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, #2b32b2 0%, #1488cc 100%);
        border: none;
        color: white !important;
        border-radius: 20px 4px 20px 20px;
        text-align: right;
    }

    .stChatMessage p {
        color: #ffffff !important;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* Avatar */
    .stChatMessage .stAvatar {
        background-color: transparent !important;
    }

    /* INPUT */
    .stChatInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    
    /* ESCONDER ELEMENTOS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. BACKEND (GEMINI AI RESTORED)
# -----------------------------------------------------------------------------
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except:
        pass

model = None
if api_key:
    genai.configure(api_key=api_key)
    try:
        # Usando a versão FLASH 2.5 como verificado anteriormente
        model = genai.GenerativeModel("models/gemini-2.5-flash")
    except Exception as e:
        st.error(f"Erro ao conectar no modelo: {e}")

# -----------------------------------------------------------------------------
# 4. INTERFACE VISUAL
# -----------------------------------------------------------------------------

# Cabeçalho
st.markdown("""
    <div class="header-style">
        <h3 style="color: #64748b; font-size: 0.9rem; margin-bottom: -10px;">SISTEMA DE VENDAS INTELIGENTE</h3>
        <h1 class="neon-text">ELITE SALES AI <span style="font-size:1rem; color: #fff; vertical-align: super;">V2.5</span></h1>
        <p style="color: #94a3b8; font-size: 0.9rem;"><i>"Transformando conversas em conversão."</i></p>
    </div>
""", unsafe_allow_html=True)

# Inicializar histórico
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá. Sou sua IA de Vendas Elite. Analisei seu perfil e identifiquei uma oportunidade de crescimento. \n\n**Qual é o maior obstáculo impedindo suas vendas de dobrarem hoje?**"}
    ]

# Exibir histórico
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        avatar_icon = "💎"
    else:
        avatar_icon = "👤"

    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# -----------------------------------------------------------------------------
# 5. CÉREBRO DA IA + EFEITO DIGITAÇÃO
# -----------------------------------------------------------------------------

prompt = st.chat_input("Digite sua resposta aqui...")

if prompt:
    # 1. Mensagem Usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
