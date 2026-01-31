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

# --- 2. CSS: DESIGN HÍBRIDO + ZOOM NO ROSTO ---
st.markdown("""
<style>
    /* FUNDO */
    .stApp {
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }
    
    p, span, div, li, label, .stMarkdown, button, textarea {
        color: #FFFFFF !important;
    }

    /* --- CONTAINER DO CABEÇALHO (FLEXBOX) --- */
    .header-container {
        display: flex;
        flex-direction: row;       /* Lado a lado */
        align-items: center;       /* Centralizado verticalmente */
        justify-content: center;   /* Centralizado na tela */
        padding-top: 20px;
        padding-bottom: 20px;
        gap: 20px;                 /* Espaço entre foto e texto */
    }

    /* --- A MÁGICA DO ZOOM (CÍRCULO MÁSCARA) --- */
    .profile-mask {
        width: 120px;              /* Tamanho PC */
        height: 120px;
        border-radius: 50%;        /* Círculo Perfeito */
        border: 3px solid #00f2fe; /* Borda Neon */
        box-shadow: 0px 0px 20px rgba(0, 242, 254, 0.5);
        overflow: hidden;          /* CORTA o que passar do círculo */
        animation: float 6s ease-in-out infinite;
        flex-shrink: 0;
        
        /* Centraliza a imagem dentro da máscara */
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* A IMAGEM DENTRO DO CÍRCULO */
    .profile-img-zoom {
        width: 100%;
        height: 100%;
        object-fit: cover;         /* Preenche tudo */
        
        /* O SEGREDO DO FOCO: */
        object-position: center 15%; /* Foca horizontalmente no meio e verticalmente no TOPO (rosto) */
        transform: scale(1.4);       /* DA UM ZOOM DE 40% PARA O ROSTO FICAR GRANDE */
    }

    /* TEXTOS */
    .brand-text {
        display: flex;
        flex-direction: column;
        text-align: left;
    }

    .neon-title {
        font-size: 32px;
        font-weight: 800;
        margin: 0;
        line-height: 1;
        text-transform: uppercase;
        color: #FFFFFF !important;
        text-shadow: 0 0 10px #00f2fe, 0 0 20px #4facfe;
    }

    .neon-subtitle {
        font-size: 16px;
        font-weight: 400;
        margin: 0;
        color: #d1d1d1 !important;
        letter-spacing: 1px;
    }

    /* --- CELULAR (AJUSTES) --- */
    @media (max-width: 600px) {
        .header-container {
            justify-content: center; /* Centraliza no mobile também */
            gap: 15px;
        }
        .profile-mask {
            width: 85px;  /* Menor no celular */
            height: 85px;
        }
        .neon-title {
            font-size: 20px; /* Texto menor para caber */
        }
        .neon-subtitle {
            font-size: 11px;
        }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }

    /* --- CHAT --- */
    .stChatInput textarea {
        background-color: #FFFFFF !important;
        color: #000000 !important;
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
# Busca imagem
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
    # APLICA A CLASSE DE ZOOM
    img_tag = f'<img src="data:{mime};base64,{encoded}" class="profile-img-zoom">'
else:
    img_tag = '<img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" class="profile-img-zoom">'

# MONTAGEM FINAL COM ESTRUTURA DE MÁSCARA
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
            chat_hist = [{"role": m["role"], "parts": [m["content"]]} 
                         for m in st.session_state.messages[:-1]]
            
            chat = model.start_chat(history=chat_hist)
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
        except Exception as e:
            st.error(f"Erro: {e}")
