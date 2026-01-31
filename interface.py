import streamlit as st
import google.generativeai as genai
import os
import base64

# --- 1. CONFIGURAÇÃO E LINKS ---
LINK_FACEBOOK = "https://www.facebook.com/share/1BivFdqW66/"
LINK_INSTAGRAM = "https://www.instagram.com/tocadocdm?igsh=MTdkYng5OGszNGI3Zw=="
LINK_YOUTUBE = "https://youtube.com/@cdm_236?si=2cvU0sn9cgEssDpW"
LINK_TIKTOK = "https://www.tiktok.com/@cdm_236?_r=1&_t=ZP-93XYGtjM0r8"

st.set_page_config(
    page_title="CDM IA Vendas Elite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS: ALINHAMENTO DE ÍCONES SOB O TEXTO ---
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

    /* --- CABEÇALHO GERAL --- */
    .header-container {
        display: flex;
        flex-direction: row;       /* Lado a Lado */
        align-items: center;       /* Centralizado Verticalmente */
        justify-content: center;   /* Centralizado na Tela */
        padding-top: 20px;
        padding-bottom: 20px;
        gap: 20px;
    }

    /* MÁSCARA DA FOTO */
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

    /* FOTO COM ZOOM 1.8 */
    .profile-img-zoom {
        width: 100%; height: 100%;
        object-fit: cover;
        object-position: center 15%; 
        transform: scale(1.8); 
        transform-origin: center 20%;
    }

    /* --- COLUNA DE TEXTO (ONDE OS ÍCONES VÃO FICAR) --- */
    .brand-text { 
        display: flex; 
        flex-direction: column; 
        text-align: left;         /* Tudo alinhado à esquerda */
        justify-content: center;
    }
    
    .neon-title {
        font-size: 32px; font-weight: 800; line-height: 1; text-transform: uppercase;
        color: #FFFFFF !important;
        text-shadow: 0 0 10px #00f2fe, 0 0 20px #4facfe;
        margin-bottom: 5px;
    }
    
    .neon-subtitle { 
        font-size: 16px; 
        font-weight: 400; 
        color: #d1d1d1 !important; 
        letter-spacing: 1px; 
        margin-bottom: 12px; /* Espaço entre subtítulo e ícones */
    }

    /* --- BARRA DE REDES SOCIAIS (AGORA ALINHADA A ESQUERDA) --- */
    .social-bar {
        display: flex;
        justify-content: flex-start; /* Alinha no começo (esquerda) junto com o texto */
        gap: 15px; /* Espaço entre os ícones */
    }
    
    .social-icon {
        width: 28px; /* Tamanho delicado para caber bem */
        height: 28px;
        transition: transform 0.3s ease, filter 0.3s ease;
        filter: drop-shadow(0 0 5px rgba(255,255,255,0.2));
    }
    
    .social-icon:hover { transform: scale(1.2); }
    .icon-fb:hover { filter: drop-shadow(0 0 10px #1877F2); }
    .icon-insta:hover { filter: drop-shadow(0 0 10px #E4405F); }
    .icon-yt:hover { filter: drop-shadow(0 0 10px #FF0000); }
    .icon-tiktok:hover { filter: drop-shadow(0 0 10px #00F2EA); }

    /* CELULAR */
    @media (max-width: 600px) {
        .header-container { gap: 15px; }
        .profile-mask { width: 90px; height: 90px; }
        .neon-title { font-size: 20px; }
        .neon-subtitle { font-size: 11px; }
        .social-icon { width: 24px; height: 24px; }
        .social-bar { gap: 10px; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
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
        background-color: rgba(20, 30, 40, 0.5) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        margin-bottom: 10px;
    }
    
    .stChatMessageAvatar img {
        border-radius: 50% !important;
        background-color: #ffffff;
        padding: 2px;
    }
    
    div[data-testid="stChatMessage"] .stMarkdown p {
        background: linear-gradient(to bottom, #ffffff, #dcdcdc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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

# --- 5. IMAGENS ---
nomes = ["perfil.jpg", "perfil.png", "perfil.jpeg", "perfil.jpg.png"]
arquivo_usuario = None
for n in nomes:
    if os.path.exists(n):
        arquivo_usuario = n
        break

if arquivo_usuario:
    with open(arquivo_usuario, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    mime = "image/png" if "png" in arquivo_usuario else "image/jpeg"
    img_tag_header = f'<img src="data:{mime};base64,{encoded}" class="profile-img-zoom">'
else:
    img_tag_header = '<img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" class="profile-img-zoom">'

user_avatar_chat = "https://cdn-icons-png.flaticon.com/512/9408/9408175.png" 
bot_avatar_chat = "https://cdn-icons-png.flaticon.com/512/4712/4712139.png"

# --- 6. EXIBIR CABEÇALHO COM ÍCONES INTEGRADOS ---
st.markdown(f"""
<div class="header-container">
    <div class="profile-mask">
        {img_tag_header}
    </div>
    <div class="brand-text">
        <div class="neon-title">CDM IA CHATBOT</div>
        <div class="neon-subtitle">O futuro das suas vendas.</div>
        
        <div class="social-bar">
            <a href="{LINK_FACEBOOK}" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/5968/5968764.png" class="social-icon icon-fb" title="Facebook">
            </a>
            <a href="{LINK_INSTAGRAM}" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/3955/3955024.png" class="social-icon icon-insta" title="Instagram">
            </a>
            <a href="{LINK_YOUTUBE}" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/3670/3670147.png" class="social-icon icon-yt" title="YouTube">
            </a>
            <a href="{LINK_TIKTOK}" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/3046/3046121.png" class="social-icon icon-tiktok" title="TikTok">
            </a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 7. CHAT ---
st.markdown('<div style="margin-bottom: 60px;">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    icon = user_avatar_chat if msg["role"] == "user" else bot_avatar_chat
    with st.chat_message(msg["role"], avatar=icon):
        st.markdown(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=user_avatar_chat):
        st.markdown(prompt)

    with st.chat_message("model", avatar=bot_avatar_chat):
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
