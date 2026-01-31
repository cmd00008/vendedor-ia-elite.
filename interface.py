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

# --- 2. CSS: ZOOM NO ROSTO + CHAT 3D METÁLICO ---
st.markdown("""
<style>
    /* FUNDO */
    .stApp {
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }
    
    /* Força cor branca para textos gerais que não são do chat */
    .header-container p, .header-container span, .header-container div, 
    label, button, textarea {
        color: #FFFFFF !important;
    }

    /* --- CABEÇALHO --- */
    .header-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        padding-top: 20px;
        padding-bottom: 20px;
        gap: 20px;
    }

    /* MÁSCARA DO CÍRCULO */
    .profile-mask {
        width: 120px; height: 120px;
        border-radius: 50%;
        border: 3px solid #00f2fe;
        box-shadow: 0px 0px 25px rgba(0, 242, 254, 0.6);
        overflow: hidden;
        animation: float 6s ease-in-out infinite;
        flex-shrink: 0;
        display: flex; align-items: center; justify-content: center;
    }

    /* FOTO COM ZOOM EXTREMO NO ROSTO */
    .profile-img-zoom {
        width: 100%; height: 100%;
        object-fit: cover;
        /* Ajuste fino: move para baixo (25%) para centralizar o rosto */
        object-position: center 25%; 
        /* Zoom forte (3x) para preencher o círculo só com o rosto */
        transform: scale(3.0); 
    }

    /* TEXTOS DO CABEÇALHO */
    .brand-text { display: flex; flex-direction: column; text-align: left; }
    .neon-title {
        font-size: 32px; font-weight: 800; line-height: 1; text-transform: uppercase;
        color: #FFFFFF !important;
        text-shadow: 0 0 10px #00f2fe, 0 0 20px #4facfe;
    }
    .neon-subtitle { font-size: 16px; font-weight: 400; color: #d1d1d1 !important; letter-spacing: 1px; }

    /* --- CELULAR --- */
    @media (max-width: 600px) {
        .header-container { justify-content: center; gap: 15px; }
        .profile-mask { width: 85px; height: 85px; }
        .neon-title { font-size: 20px; }
        .neon-subtitle { font-size: 11px; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }

    /* --- CHAT INPUT --- */
    .stChatInput textarea {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #4facfe !important;
        border-radius: 30px !important;
    }
    .stChatInput button { color: #4facfe !important; }

    /* --- NOVOS BALÕES DE CHAT (OVAL 3D, TRANSPARENTE, METÁLICO) --- */
    div[data-testid="stChatMessage"] {
        /* Forma Oval e Transparência */
        background-color: rgba(20, 30, 40, 0.4) !important; /* Azul escuro bem transparente */
        border-radius: 50px !important; /* Borda bem redonda (oval) */
        border: 1px solid rgba(255, 255, 255, 0.15); /* Borda sutil */
        
        /* Efeito 3D Flutuante */
        box-shadow: 
            0 8px 20px rgba(0,0,0,0.3), /* Sombra projetada para baixo */
            inset 0 1px 2px rgba(255,255,255,0.2); /* Brilho interno na borda superior */
        
        /* Efeito Vidro Fosco */
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        
        margin-bottom: 15px;
        padding: 15px 25px !important; /* Mais espaço interno */
    }

    /* --- TEXTO METÁLICO BRILHANTE DENTRO DOS BALÕES --- */
    div[data-testid="stChatMessage"] .stMarkdown p {
        /* Gradiente Metálico (Prata/Cromo) */
        background: linear-gradient(to bottom, #ffffff, #e0e0e0, #b0b0b0, #ffffff);
        background-size: 200% auto;
        
        /* Aplica o gradiente no texto */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: transparent;
        
        /* Sombra para dar profundidade 3D nas letras */
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        font-weight: 600; /* Um pouco mais negrito para destacar o efeito */
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONEXÃO (BLINDADA) ---
try:
    api_key = os.environ.get("GOOGLE_API_KEY") # Prioridade Env Var
    if not api_key:
        api_key = st.secrets["GOOGLE_API_KEY"]
    
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.error("⚠️ API Key ausente.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ Erro de Configuração: {e}")
    st.stop()

# ANTIGRAVITY FIX: models/gemini-2.5-flash
model = genai.GenerativeModel('models/gemini-2.5-flash', system_instruction="Você é o CDM, IA de Vendas Elite. Responda no idioma do usuário.")

# --- 4. MEMÓRIA ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "Olá! Sou o CDM. Como posso ajudar a escalar suas vendas hoje? 🚀"}]

# --- 5. CABEÇALHO ---
nomes = ["perfil.jpg", "perfil.png", "perfil.jpeg", "perfil.jpg.png"]
arquivo = None
for n in nomes:
    if os.path.exists(n):
        arquivo = n
        break

if arquivo:
    with open(arquivo, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    mime = "image/png" if "png" in arquivo else "image/jpeg"
    img_tag = f'<img src="data:{mime};base64,{encoded}" class="profile-img-zoom">'
else:
    img_tag = '<img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" class="profile-img-zoom">'

st.markdown(f"""
<div class="header-container">
    <div class="profile-mask">
        {img_tag}
    </div>
    <div class="brand-text">
        <div class="neon-title">CDM IA CHATBOT</div>
        <div class="neon-subtitle">O futuro das suas vendas.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 6. CHAT ---
st.markdown('<div style="margin-bottom: 60px;">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    avatar = "⚡" if msg["role"] == "model" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("model", avatar="⚡"):
        try:
            # FIX: Safer history slicing
            chat_hist = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
            chat = model.start_chat(history=chat_hist)
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
        except Exception as e:
            st.error(f"Erro: {e}")
