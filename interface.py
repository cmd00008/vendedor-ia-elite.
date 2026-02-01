import streamlit as st
import google.generativeai as genai
import os
import base64

# --- 1. SEUS LINKS ---
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

# --- 2. CSS (A CORREÇÃO FINAL: CENTRALIZADO E COLADO) ---
st.markdown("""
<style>
    /* FUNDO */
    .stApp {
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }
    
    p, span, div, li, label, .stMarkdown, button, textarea, h1, h2, h3 {
        color: #FFFFFF !important;
    }

    /* --- LAYOUT MOBILE: O BLINDADO --- */
    @media (max-width: 640px) {
        
        /* 1. O CONTAINER: Centraliza tudo na tela para NÃO CORTAR a foto */
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
            justify-content: center !important; /* ISSO SALVA A FOTO DE SER CORTADA */
            gap: 0px !important; /* SEM ESPAÇO NENHUM */
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* 2. COLUNA DA FOTO */
        div[data-testid="column"]:nth-of-type(1) {
            flex: 0 0 auto !important; /* Tamanho exato da foto */
            width: auto !important;
            display: flex !important;
            justify-content: flex-end !important; /* Encosta na direita (no texto) */
            align-items: center !important;
            padding: 0 !important;
        }
        
        /* 3. COLUNA DO TEXTO */
        div[data-testid="column"]:nth-of-type(2) {
            flex: 0 0 auto !important; /* Tamanho exato do texto */
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: flex-start !important;
            padding-left: 5px !important; /* Apenas 5px para não sobrepor visualmente */
        }

        /* 4. TAMANHO DA FOTO (Controlado) */
        .profile-mask { 
            width: 95px !important; 
            height: 95px !important; 
            margin: 0 !important; /* Remove margens extras */
        }

        /* 5. TEXTO (Ajustado) */
        .neon-title {
            font-size: 18px !important; 
            text-align: left !important;
            line-height: 1.1 !important;
            margin-bottom: 2px !important;
            margin-top: 0 !important;
            white-space: nowrap !important;
        }
        
        .neon-subtitle {
            font-size: 11px !important; 
            text-align: left !important; 
            margin-bottom: 5px !important;
            white-space: nowrap !important;
        }
        
        /* Ícones */
        .social-bar {
            justify-content: flex-start !important;
            gap: 8px !important;
            margin-bottom: 5px !important;
        }
        
        .social-icon { width: 20px !important; height: 20px !important; }
        
        /* Botão */
        div.stButton > button {
            margin-left: -2px !important;
            padding: 0px !important;
            transform: scale(0.9);
            transform-origin: left center;
        }
    }

    /* --- ESTILOS GERAIS (PC) --- */
    .profile-mask {
        width: 140px; height: 140px;
        border-radius: 50%;
        border: 3px solid #00f2fe;
        box-shadow: 0px 0px 25px rgba(0, 242, 254, 0.6);
        overflow: hidden; 
        animation: float 6s ease-in-out infinite;
        flex-shrink: 0;
        display: flex; align-items: center; justify-content: center;
    }

    .profile-img-zoom {
        width: 100%; height: 100%;
        object-fit: cover;
        object-position: center 15%; 
        transform: scale(1.8); 
        transform-origin: center 20%;
    }

    .neon-title {
        font-size: 36px; font-weight: 800; line-height: 1; text-transform: uppercase;
        color: #FFFFFF !important;
        text-shadow: 0 0 10px #00f2fe, 0 0 20px #4facfe;
        margin-bottom: 5px;
        margin-top: 0;
    }
    .neon-subtitle { 
        font-size: 18px; font-weight: 400; color: #d1d1d1 !important; 
        letter-spacing: 1px; margin-bottom: 15px;
    }

    .social-bar {
        display: flex; justify-content: flex-start; gap: 15px; margin-bottom: 15px;
    }
    .social-icon {
        width: 30px; height: 30px;
        transition: transform 0.3s ease;
        filter: drop-shadow(0 0 5px rgba(255,255,255,0.2));
    }
    .social-icon:hover { transform: scale(1.2); }

    div.stButton > button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
        display: inline-flex;
        align-items: center;
        justify-content: flex-start;
        transition: transform 0.3s ease;
        margin-top: -5px;
    }
    div.stButton > button:hover { transform: scale(1.05); }

    div.stButton > button::before {
        content: "";
        display: inline-block;
        width: 28px; height: 28px;
        background-image: url('https://cdn-icons-png.flaticon.com/512/3616/3616190.png'); 
        background-size: contain; 
        background-repeat: no-repeat;
        background-position: center;
        margin-right: 8px;
        filter: drop-shadow(0 0 5px rgba(0, 255, 0, 0.4)); 
    }

    div.stButton > button p {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-size: 13px !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        margin: 0 !important;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(191, 149, 63, 0.5);
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }

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

if "show_card" not in st.session_state:
    st.session_state.show_card = False

def toggle_card():
    st.session_state.show_card = not st.session_state.show_card

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

# --- 6. CABEÇALHO ---
st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)

# Colunas Automáticas (A Mágica acontece aqui com o CSS de 1 para 1)
col_foto, col_texto = st.columns([1, 1]) 

with col_foto:
    st.markdown(f"""
    <div style="display:flex; justify-content:center;">
        <div class="profile-mask">
            {img_tag_header}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_texto:
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; justify-content:center; height:100%;">
        <div class="neon-title">CDM IA CHATBOT</div>
        <div class="neon-subtitle">O futuro das suas vendas.</div>
        <div class="social-bar">
            <a href="{LINK_FACEBOOK}" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/5968/5968764.png" class="social-icon" title="Facebook">
            </a>
            <a href="{LINK_INSTAGRAM}" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/3955/3955024.png" class="social-icon" title="Instagram">
            </a>
            <a href="{LINK_YOUTUBE}" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/3670/3670147.png" class="social-icon" title="YouTube">
            </a>
            <a href="{LINK_TIKTOK}" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/3046/3046121.png" class="social-icon" title="TikTok">
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("DIGITAL CARD"):
        toggle_card()
        st.rerun()

# --- 7. MOSTRA O CARTÃO ---
if st.session_state.show_card:
    cartao_visita = "perfil.jpg.jpg"
    if os.path.exists(cartao_visita):
        st.markdown('<div style="animation: float 0.5s ease-out; margin-top: 15px; margin-bottom: 20px;">', unsafe_allow_html=True)
        st.image(cartao_visita, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="margin-bottom: 40px;"></div>', unsafe_allow_html=True)

# --- 8. CHAT ---
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
