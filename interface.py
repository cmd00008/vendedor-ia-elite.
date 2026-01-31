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

# --- 2. CSS (ESTRUTURA ELITE: ESQUERDA - CENTRO - DIREITA) ---
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

    /* --- ÁREA CENTRAL (FOTO + TEXTO) --- */
    .center-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    /* MÁSCARA DA FOTO (NO PC ELA É MAIOR) */
    .profile-mask {
        width: 150px; height: 150px;
        border-radius: 50%;
        border: 4px solid #00f2fe;
        box-shadow: 0px 0px 40px rgba(0, 242, 254, 0.6);
        overflow: hidden; 
        animation: float 6s ease-in-out infinite;
        flex-shrink: 0;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 15px; /* Espaço para o texto */
    }

    .profile-img-zoom {
        width: 100%; height: 100%;
        object-fit: cover;
        object-position: center 15%; 
        transform: scale(1.8); 
        transform-origin: center 20%;
    }

    /* TÍTULO (NO PC É GIGANTE) */
    .neon-title {
        font-size: 40px; 
        font-weight: 900; 
        line-height: 1.2; 
        text-transform: uppercase;
        color: #FFFFFF !important;
        text-shadow: 0 0 15px #00f2fe, 0 0 30px #4facfe;
        margin: 0;
    }
    .neon-subtitle { 
        font-size: 18px; 
        font-weight: 400; 
        color: #e0e0e0 !important; 
        letter-spacing: 3px; /* Letras espaçadas estilo cinema */
        margin-top: 5px;
    }

    /* --- ÁREA DA DIREITA (REDES SOCIAIS) --- */
    .social-bar-right {
        display: flex; 
        justify-content: flex-end; /* Alinha tudo para a DIREITA */
        gap: 20px;
        align-items: center;
        height: 100%; /* Para centralizar verticalmente com o botão */
        padding-top: 15px; /* Ajuste fino de altura */
    }
    .social-icon {
        width: 35px; height: 35px;
        transition: transform 0.3s ease;
        filter: drop-shadow(0 0 5px rgba(255,255,255,0.3));
    }
    .social-icon:hover { transform: scale(1.3); }

    /* --- ÁREA DA ESQUERDA (BOTÃO DIGITAL CARD) --- */
    
    /* Força o botão a ficar na esquerda */
    div.stButton {
        display: flex;
        justify-content: flex-start;
        padding-top: 10px; /* Alinha com os ícones */
    }

    div.stButton > button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
        display: inline-flex;
        align-items: center;
        transition: transform 0.3s ease;
    }
    
    div.stButton > button:hover { transform: scale(1.05); }

    div.stButton > button::before {
        content: "";
        display: inline-block;
        width: 32px; height: 32px;
        background-image: url('https://cdn-icons-png.flaticon.com/512/5585/5585856.png'); 
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        margin-right: 12px;
        filter: drop-shadow(0 0 8px rgba(255, 50, 50, 0.8)); 
    }

    div.stButton > button p {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        margin: 0 !important;
        letter-spacing: 1px;
        text-shadow: 0 0 15px rgba(191, 149, 63, 0.4);
    }

    /* --- CELULAR (AJUSTE AUTOMÁTICO) --- */
    @media (max-width: 800px) {
        .social-bar-right { justify-content: center; margin-top: 15px; } /* Centraliza ícones */
        div.stButton { justify-content: center; margin-top: 15px; } /* Centraliza botão */
        .neon-title { font-size: 26px; }
        .neon-subtitle { font-size: 12px; letter-spacing: 1px; }
        .profile-mask { width: 120px; height: 120px; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }

    /* CHAT */
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

# --- 4. MEMÓRIA & ESTADO ---
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

# --- 6. CABEÇALHO ESTRUTURADO (PC ELITE) ---
st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)

# CRIA 3 COLUNAS BALANCEADAS: [ESQUERDA] [CENTRO MAIOR] [DIREITA]
# No celular, elas vão empilhar automaticamente.
col_left, col_center, col_right = st.columns([1, 1.5, 1])

# --- COLUNA DA ESQUERDA: BOTÃO DIGITAL CARD ---
with col_left:
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True) # Espaçador
    if st.button("DIGITAL CARD"):
        toggle_card()
        st.rerun()

# --- COLUNA DO CENTRO: FOTO + TÍTULO ---
with col_center:
    st.markdown(f"""
    <div class="center-content">
        <div class="profile-mask">
            {img_tag_header}
        </div>
        <div class="neon-title">CDM IA CHATBOT</div>
        <div class="neon-subtitle">O futuro das suas vendas.</div>
    </div>
    """, unsafe_allow_html=True)

# --- COLUNA DA DIREITA: ÍCONES SOCIAIS ---
with col_right:
    # Usamos uma div especial para alinhar à direita
    st.markdown(f"""
    <div class="social-bar-right">
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
    """, unsafe_allow_html=True)

# --- 7. MOSTRA O CARTÃO (Centralizado) ---
if st.session_state.show_card:
    cartao_visita = "perfil.jpg.jpg"
    if os.path.exists(cartao_visita):
        # Cria colunas para centralizar a imagem do cartão
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown('<div style="animation: float 0.5s ease-out; margin-top: 20px; margin-bottom: 20px;">', unsafe_allow_html=True)
            st.image(cartao_visita, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="margin-bottom: 50px;"></div>', unsafe_allow_html=True)

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
