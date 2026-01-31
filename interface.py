import streamlit as st
import time
import os
import base64
import google.generativeai as genai

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO GERAL
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="IA Vendas Elite 5.0",
    page_icon="�",
    layout="centered", # 'Centered' funciona melhor no celular que 'Wide'
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. CARREGAMENTO DA FOTO (Lógica Inteligente)
# -----------------------------------------------------------------------------
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Tenta carregar sua foto 'perfil.png'
img_tag = ""
if os.path.exists("perfil.png"):
    img_b64 = get_img_as_base64("perfil.png")
    # CSS aqui faz o recorte redondo e foca no rosto (object-position)
    img_tag = f'<img src="data:image/png;base64,{img_b64}" class="profile-pic">'
else:
    # Avatar genérico caso você esqueça de subir a foto
    img_tag = '<div style="font-size:50px;">👨‍💼</div>'

# -----------------------------------------------------------------------------
# 3. BACKEND (GEMINI AI RESTORED)
# -----------------------------------------------------------------------------
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
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

# -----------------------------------------------------------------------------
# 4. ESTILO VISUAL (CSS OTIMIZADO PARA MOBILE)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Fontes Clean */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* Fundo Escuro Moderno */
    .stApp {
        background-color: #0e1117;
        background-image: linear-gradient(180deg, #161b2e 0%, #000000 100%);
        color: white;
    }

    /* --- ESTILO DA SUA FOTO (Foco no Rosto) --- */
    .profile-pic {
        width: 110px;
        height: 110px;
        border-radius: 50%;        /* Faz ficar redondo */
        object-fit: cover;         /* Preenche sem esticar */
        object-position: center 20%; /* FOCA NO ROSTO (Sobe o foco 20%) */
        border: 3px solid #00C9FF; /* Borda Neon */
        box-shadow: 0 0 20px rgba(0, 201, 255, 0.4);
        margin-bottom: 10px;
    }

    /* Títulos */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        padding: 0;
        font-size: 2.2rem !important;
    }
    
    p {
        font-family: 'Inter', sans-serif;
        color: #b0b0b0 !important;
    }

    /* --- CHAT MOBILE FIX (Correção de Texto Invisível) --- */
    .stChatMessage {
        background-color: transparent !important;
    }

    /* Balão do Usuário */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(79, 172, 254, 0.15) !important;
        border: 1px solid rgba(79, 172, 254, 0.3);
        border-radius: 15px;
    }
    
    /* Balão da IA */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
    }

    /* Força texto branco SEMPRE */
    .stChatMessage p, .stChatMessage div {
        color: #ffffff !important;
    }

    /* Input ajustado para não quebrar no iPhone */
    .stChatInput {
        padding-bottom: 15px !important;
    }

    /* Esconder menus chatos */
    #MainMenu, footer, header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. CABEÇALHO (SEU PERFIL + ROBÔ)
# -----------------------------------------------------------------------------

col_left, col_center, col_right = st.columns([1, 2, 1])

# Coluna 1: Robô
with col_left:
    st.markdown('<div style="display:flex; justify-content:center; align-items:center; height:100%;">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712038.png", width=60) # Ícone Robô 3D
    st.markdown('</div>', unsafe_allow_html=True)

# Coluna 2: Título
with col_center:
    st.markdown("""
        <div style="text-align: center;">
            <h1>VENDAS ELITE</h1>
            <p style="font-size: 0.8rem; letter-spacing: 2px; text-transform: uppercase;">Inteligência Artificial</p>
        </div>
    """, unsafe_allow_html=True)

# Coluna 3: SUA FOTO
with col_right:
    st.markdown(f"""
        <div style="display: flex; justify-content: center;">
            {img_tag}
        </div>
    """, unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------------------------
# 6. LÓGICA DO CHAT (REAL)
# -----------------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Analisei seus dados. \n\nEstou pronto para criar a estratégia perfeita. O que vamos vender hoje?"}
    ]

# Exibir mensagens
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        with st.chat_message("assistant", avatar="🤖"):
            st.write(msg["content"])
    else:
        with st.chat_message("user", avatar="👤"):
            st.write(msg["content"])

# Input do Usuário
if prompt := st.chat_input("Digite aqui..."):
    # 1. Mostrar mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
