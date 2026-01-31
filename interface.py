import streamlit as st
import google.generativeai as genai
import os
import base64

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(
    page_title="CDM IA Vendas Elite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS: VISUAL NEON E LAYOUT LADO-A-LADO ---
st.markdown("""
<style>
    /* FUNDO AZUL PROFUNDO */
    .stApp {
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }
    
    /* FORÇAR TEXTOS GERAIS BRANCOS */
    p, span, div, li, label, .stMarkdown, button, textarea {
        color: #FFFFFF !important;
    }

    /* --- CABEÇALHO (FOTO + TEXTO NEON) --- */
    .header-container {
        display: flex;
        flex-direction: row; /* Coloca um do lado do outro */
        align-items: center; /* Alinha verticalmente no centro */
        justify-content: center; /* Centraliza o conjunto na tela */
        padding-top: 30px;
        padding-bottom: 30px;
        gap: 25px; /* Espaço entre a foto e o texto */
    }

    /* FOTO (Círculo com Zoom e Brilho) */
    .profile-img {
        width: 130px; 
        height: 130px;
        border-radius: 50%;
        object-fit: cover;
        object-position: top center;
        border: 3px solid #00f2fe; /* Borda Ciano Neon */
        box-shadow: 0px 0px 30px rgba(0, 242, 254, 0.5); /* Brilho Azul Claro */
        animation: float 6s ease-in-out infinite;
        flex-shrink: 0; /* Garante que a foto não amasse */
    }
    
    /* ÁREA DO TEXTO DA MARCA */
    .brand-text {
        display: flex;
        flex-direction: column;
    }

    /* TÍTULO PRINCIPAL (CDM IA Chatbot) - EFEITO NEON FORTE */
    .neon-title {
        font-size: 36px;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
        text-transform: uppercase;
        color: #FFFFFF !important;
        /* O Segredo do Brilho Neon: Múltiplas sombras */
        text-shadow: 
            0 0 5px #FFFFFF,
            0 0 10px #00f2fe,
            0 0 20px #00f2fe,
            0 0 40px #4facfe,
            0 0 80px #4facfe;
    }

    /* SUBTÍTULO (O futuro...) - BRILHO MAIS SUAVE */
    .neon-subtitle {
        font-size: 20px;
        font-weight: 400;
        margin: 0;
        color: #e0e0e0 !important;
        letter-spacing: 1px;
        text-shadow: 0 0 15px rgba(79, 172, 254, 0.8);
    }
    
    /* ANIMAÇÃO DE FLUTUAR */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    /* --- RESPONSIVIDADE (CELULAR) --- */
    /* No celular, coloca um embaixo do outro para não apertar */
    @media (max-width: 600px) {
        .header-container {
            flex-direction: column;
            text-align: center;
        }
        .brand-text {
            margin-top: 15px;
            align-items: center;
        }
        .neon-title { font-size: 28px; }
        .neon-subtitle { font-size: 16px; }
    }

    /* --- ESTILOS DO CHAT --- */
    .stChatInput textarea {
        background-color: #FFFFFF !important; /* Fundo BRANCO */
        color: #000000 !important;       /* Letra PRETA */
        border: 2px solid #4facfe !important;
        border-radius: 30px !important;
    }
    .stChatInput button { color: #4facfe !important; }

    div[data-testid="stChatMessage"] {
        background-color: rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONEXÃO (BLINDADA) ---
try:
    api_key = os.environ.get("GOOGLE_API_KEY") 
    if not api_key:
        api_key = st.secrets["GOOGLE_API_KEY"]
    
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.error("⚠️ API Key não configurada.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ Erro de Configuração: {e}")
    st.stop()

# ANTIGRAVITY FIX: models/gemini-2.5-flash
model = genai.GenerativeModel('models/gemini-2.5-flash', system_instruction="Você é o CDM, IA de Vendas Elite. Responda no idioma do usuário.")

# --- 4. MEMÓRIA ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "Olá! Sou o CDM. Vamos transformar suas conversas em vendas? 🚀"}]

# --- 5. CABEÇALHO (FOTO + TEXTO NEON LADO A LADO) ---

# Busca a imagem
nomes_possiveis = ["perfil.jpg", "perfil.png", "perfil.jpeg", "perfil.jpg.png"]
arquivo_encontrado = None
for nome in nomes_possiveis:
    if os.path.exists(nome):
        arquivo_encontrado = nome
        break

# Prepara a tag da imagem
if arquivo_encontrado:
    with open(arquivo_encontrado, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    mime = "image/png" if "png" in arquivo_encontrado else "image/jpeg"
    img_html = f'<img src="data:{mime};base64,{encoded}" class="profile-img">'
else:
    img_html = '<img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" class="profile-img">'

# MONTA O HTML DO CABEÇALHO COM O TEXTO BRILHANTE
st.markdown(f"""
<div class="header-container">
    {img_html}
    <div class="brand-text">
        <h1 class="neon-title">CDM IA Chatbot</h1>
        <h3 class="neon-subtitle">O futuro das suas vendas.</h3>
    </div>
</div>
""", unsafe_allow_html=True)


# --- 6. CHAT E BARRA DE DIGITAÇÃO ---
st.markdown('<div style="margin-bottom: 50px;">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    avatar = "⚡" if msg["role"] == "model" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Digite sua mensagem aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("model", avatar="⚡"):
        try:
            # FIX: safer history slicing
            chat_hist = [{"role": m["role"], "parts": [m["content"]]} 
                         for m in st.session_state.messages[:-1]]
            
            chat = model.start_chat(history=chat_hist)
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
        except Exception as e:
            st.error(f"Erro: {e}")
