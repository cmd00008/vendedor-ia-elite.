import streamlit as st
import time
import os
import google.generativeai as genai

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA (Deve ser a primeira linha)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="IA Vendas Elite 3.0",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. DESIGN VISUAL AVANÇADO (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Importar Fontes Futuristas */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Montserrat:wght@300;400;600&display=swap');

    /* --- FUNDO E CORES GERAIS --- */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 10%, #1c1c3d 0%, #000000 90%);
        color: white;
    }

    /* --- CORREÇÃO DE TEXTO (CRÍTICO PARA MOBILE) --- */
    /* Isso garante que o texto nunca fique preto no fundo preto */
    p, div, h1, h2, h3, h4, span, label {
        color: #ffffff !important; 
        font-family: 'Montserrat', sans-serif;
    }

    /* Títulos em Neon */
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(0, 201, 255, 0.5);
    }

    /* --- ESTILO DOS BALÕES DE CHAT --- */
    
    /* Remover fundo padrão dos avatares */
    .stAvatar {
        background-color: transparent !important;
        border: 2px solid #00C9FF;
        border-radius: 50%;
    }

    /* Balão da IA (Robô) */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background: rgba(30, 30, 40, 0.9);
        border: 1px solid #00C9FF;
        border-radius: 0px 20px 20px 20px;
        box-shadow: 0 0 15px rgba(0, 201, 255, 0.1);
        padding: 15px;
    }

    /* Balão do Usuário (Você) */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, #0061ff 0%, #60efff 100%);
        border: none;
        border-radius: 20px 0px 20px 20px;
        padding: 15px;
        text-align: right; /* Alinha texto à direita */
    }

    /* Input de Texto Flutuante */
    .stChatInput {
        position: fixed;
        bottom: 20px;
        z-index: 1000;
    }
    
    .stChatInput input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 30px !important;
    }

    /* Esconder elementos desnecessários */
    #MainMenu, footer, header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. BACKEND (GEMINI AI RESTORED)
# -----------------------------------------------------------------------------
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    # Fallback to secrets if env var not set (local dev)
    if not api_key:
        api_key = st.secrets.get("GOOGLE_API_KEY")

    if api_key:
        genai.configure(api_key=api_key)
        # Usando a versão FLASH 2.5 verificada
        model = genai.GenerativeModel("models/gemini-2.5-flash")
    else:
        model = None
except Exception as e:
    model = None
    # Silencie o erro aqui se quiser apenas mostrar aviso no chat depois

# -----------------------------------------------------------------------------
# 4. CABEÇALHO PERSONALIZADO (Robô + Título + Sua Foto)
# -----------------------------------------------------------------------------

col1, col2, col3 = st.columns([1, 6, 1])

# COLUNA 1: GIF DO ROBÔ
with col1:
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbm91ZGw0bXF4eXJ5Y3l5b3J5Y3l5b3J5Y3l5b3J5Y3l5b3J5Y3l5b3J5Y3l5b3J5Y3l5b3J5Y3l5b3J5Y3l5b3J5Y3l5b3J5Y3l5b3J5Y3l5b3J5Y3l5b3J5Y3l5b3J5Y3l5b3J5Y3l5b3J5/L1R1TVThZAaKOUlrfv/giphy.gif", width=80)

# COLUNA 2: TÍTULO CENTRAL
with col2:
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>IA VENDAS ELITE <span style='font-size: 0.4em; border:1px solid #00C9FF; padding: 2px 8px; border-radius: 4px; color: #00C9FF;'>V3.0 TURBO</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #aaa !important; font-size: 0.9em;'>Sistema Neural de Conversão Ativado</p>", unsafe_allow_html=True)

# COLUNA 3: SUA FOTO
with col3:
    col3_content = st.empty()
    # Tenta achar 'minha_foto.png' ou 'minha_foto.jpg'
    foto_encontrada = False
    for ext in ["png", "jpg", "jpeg"]:
        if os.path.exists(f"minha_foto.{ext}"):
            col3_content.image(f"minha_foto.{ext}", width=80)
            foto_encontrada = True
            break
    
    if not foto_encontrada:
        col3_content.markdown("<div style='text-align:center; font-size: 50px;'>👨‍💼</div>", unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------------------------
# 5. MOTOR DO CHAT
# -----------------------------------------------------------------------------

# Mensagem Inicial
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! O sistema de **Vendas Elite** está online. 🚀\n\nAnalisei seu perfil e vejo potencial de escala. Qual produto ou serviço você quer vender hoje?"}
    ]

# Renderizar Histórico
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        avatar = "🤖" 
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
    else:
        avatar = "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# -----------------------------------------------------------------------------
# 6. INPUT E PROCESSAMENTO REAL
# -----------------------------------------------------------------------------

prompt = st.chat_input("Digite sua resposta...")

if prompt:
    # 1. Mostra o que o usuário digitou
    st.session_state.messages.append({"role": "user", "content": prompt})
