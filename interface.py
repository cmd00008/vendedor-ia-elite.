import streamlit as st
import google.generativeai as genai
import os
import base64

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="IA Vendas Elite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS: DESIGN VISUAL ---
st.markdown("""
<style>
    /* FUNDO AZUL PROFUNDO */
    .stApp {
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }
    
    /* TEXTO BRANCO */
    h1, h2, h3, h4, h5, h6, p, span, div, li, label, .stMarkdown, button, textarea {
        color: #FFFFFF !important;
    }

    /* FOTO DE PERFIL (CÍRCULO FLUTUANTE) */
    .profile-container {
        display: flex;
        justify-content: center;
        padding-top: 30px;
        padding-bottom: 20px;
    }
    .profile-img {
        width: 150px; 
        height: 150px;
        border-radius: 50%;          /* Círculo Perfeito */
        object-fit: cover;           /* Foca no rosto */
        object-position: top center; /* Garante que o boné apareça */
        border: 4px solid #4facfe;   /* Borda Neon */
        box-shadow: 0px 0px 30px rgba(79, 172, 254, 0.7); 
        animation: float 6s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    /* ESTILO DO CHAT INPUT (Oficial) */
    .stChatInput textarea {
        background-color: #000000 !important; 
        color: #FFFFFF !important; 
        border: 2px solid #4facfe !important; 
        border-radius: 30px !important;
    }
    .stChatInput button {
        color: #4facfe !important;
    }

    /* BALÕES DO CHAT */
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
    api_key = os.environ.get("GOOGLE_API_KEY") # Prioridade Env Var
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

# Configuração do Modelo (Fix: 2.5)
# ANTIGRAVITY FIX: models/gemini-2.5-flash
model = genai.GenerativeModel('models/gemini-2.5-flash', system_instruction="Você é o CDM, IA de Vendas Elite. Responda no idioma do usuário.")

# --- 4. MEMÓRIA ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "Olá! Sou o CDM. Como posso ajudar a escalar suas vendas hoje? 🚀"}]

# --- 5. BUSCA DA FOTO (CORREÇÃO DO NOME DUPLO) ---
st.markdown('<div class="profile-container">', unsafe_allow_html=True)

# Adicionei 'perfil.jpg.png' na lista de busca!
possible_files = ["perfil.jpg.png", "perfil.jpg", "perfil.png"]
image_found = None

for file_path in possible_files:
    if os.path.exists(file_path):
        image_found = file_path
        break

if image_found:
    with open(image_found, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    # Define o tipo correto para o navegador entender
    mime_type = "image/png" if "png" in image_found else "image/jpeg"
    st.markdown(f'<img src="data:{mime_type};base64,{encoded}" class="profile-img">', unsafe_allow_html=True)
else:
    # Se não achar nada, usa o robô
    st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" class="profile-img">', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- 6. EXIBIR HISTÓRICO ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    avatar = "⚡" if msg["role"] == "model" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

# --- 7. INPUT DE CHAT (OFICIAL COM BOTÃO) ---
if prompt := st.chat_input("Digite sua pergunta aqui..."):
    # Usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # IA
    with st.chat_message("model", avatar="⚡"):
        try:
            # History cleaner
            chat_hist = [{"role": m["role"], "parts": [m["content"]]} 
                         for m in st.session_state.messages[:-1]]
            
            chat = model.start_chat(history=chat_hist)
            response = chat.send_message(prompt)
            st.markdown(response.text)
            
            # COMPLETING THE TRUNCATED LINE FROM USER REQUEST:
            st.session_state.messages.append({"role": "model", "content": response.text})
            
        except Exception as e:
            st.error(f"Erro: {e}")
