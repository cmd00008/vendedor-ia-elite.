import streamlit as st
import google.generativeai as genai
import os
import base64

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(
    page_title="IA Vendas Elite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS: CORREÇÃO VISUAL E FOTO PERFEITA ---
st.markdown("""
<style>
    /* FUNDO AZUL PROFUNDO */
    .stApp {
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }
    
    /* TEXTOS BRANCOS */
    h1, h2, h3, h4, h5, h6, p, span, div, li, label, .stMarkdown, button, textarea {
        color: #FFFFFF !important;
    }

    /* --- O SEGREDO DA FOTO PERFEITA --- */
    .profile-container {
        display: flex;
        justify-content: center;
        padding-top: 30px;
        padding-bottom: 20px;
    }
    
    .profile-img {
        width: 150px; 
        height: 150px;
        border-radius: 50%;          /* Faz o círculo */
        
        /* AQUI ESTÁ A CORREÇÃO: */
        object-fit: cover;           /* Dá zoom para preencher o círculo (sem borda cinza) */
        object-position: top center; /* Foca no rosto/boné, corta o peito se precisar */
        
        border: 4px solid #4facfe;   /* Borda Azul Neon */
        box-shadow: 0px 0px 30px rgba(79, 172, 254, 0.7); /* Brilho forte */
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    /* ESTILO DA BARRA DE CHAT (OFICIAL) */
    .stChatInput textarea {
        background-color: #1e1e1e !important; /* Fundo Escuro */
        color: #FFFFFF !important; /* Letra Branca */
        border: 2px solid #4facfe !important; /* Borda Azul */
        border-radius: 30px !important;
    }
    
    /* Ícone de Enviar */
    .stChatInput button {
        color: #4facfe !important;
    }

    /* BALÕES */
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

# Configuração do Modelo (ANTIGRAVITY FIX: models/gemini-2.5-flash)
model = genai.GenerativeModel('models/gemini-2.5-flash', system_instruction="Você é o CDM, IA de Vendas Elite. Responda no idioma do usuário.")

# --- 4. MEMÓRIA ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "Olá! Sou o CDM. Estou pronto para escalar suas vendas! 🚀"}]

# --- 5. BUSCA INTELIGENTE DA FOTO (Resolve o problema do nome) ---
st.markdown('<div class="profile-container">', unsafe_allow_html=True)

# Lista de tentativas: o código vai tentar todos esses nomes até achar sua foto
nomes_possiveis = [
    "perfil.jpg", 
    "perfil.png", 
    "perfil.jpeg", 
    "perfil.jpg.png", # Caso tenha renomeado errado
    "perfil.png.jpg"
]

arquivo_encontrado = None

# O Loop Caçador de Arquivos
for nome in nomes_possiveis:
    if os.path.exists(nome):
        arquivo_encontrado = nome
        break # Achou! Para de procurar.

if arquivo_encontrado:
    # Se achou, carrega e exibe
    with open(arquivo_encontrado, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    
    # Define o tipo (truque técnico para navegador)
    mime = "image/png" if "png" in arquivo_encontrado else "image/jpeg"
    
    st.markdown(f'<img src="data:{mime};base64,{encoded}" class="profile-img">', unsafe_allow_html=True)
else:
    # Se não achou NADA, mostra o robô (pra não ficar buraco na tela)
    st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" class="profile-img">', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- 6. EXIBIR O CHAT ---
# Mostra o histórico
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    avatar = "⚡" if msg["role"] == "model" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

# --- 7. A BARRA DE CHAT OFICIAL (Resolve o problema do Enter) ---
# st.chat_input cria aquela barra fixa embaixo igual WhatsApp
if prompt := st.chat_input("Digite sua mensagem aqui..."):
    # 1. Mostra msg do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. IA Responde
    with st.chat_message("model", avatar="⚡"):
        try:
            # HISTORY FIX: avoid duplicate prompt in history
            chat_hist = [{"role": m["role"], "parts": [m["content"]]} 
                         for m in st.session_state.messages[:-1]]
            
            chat = model.start_chat(history=chat_hist)
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
        except Exception as e:
            st.error(f"Erro: {e}")
