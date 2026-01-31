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

# --- 2. CSS: CORREÇÃO DE CORES E VISUAL ---
st.markdown("""
<style>
    /* FUNDO AZUL PROFUNDO */
    .stApp {
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }
    
    /* TEXTOS GERAIS (Títulos, mensagens antigas) - BRANCO */
    h1, h2, h3, h4, h5, h6, p, span, div, li, label, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* --- CORREÇÃO DA BARRA DE DIGITAÇÃO (BRANCA COM LETRA PRETA) --- */
    .stChatInput textarea {
        background-color: #FFFFFF !important; /* Fundo BRANCO */
        color: #000000 !important;       /* Letra PRETA */
        caret-color: #000000 !important; /* Cursor piscando PRETO */
        border: 2px solid #4facfe !important; /* Borda Azul */
        border-radius: 30px !important;
    }
    
    /* Cor do texto de ajuda (Placeholder) dentro da barra branca */
    .stChatInput textarea::placeholder {
        color: #555555 !important; /* Cinza escuro para ler fácil */
    }

    /* Ícone de Enviar (Setinha) */
    .stChatInput button {
        color: #4facfe !important;
    }

    /* --- BALÕES DO CHAT --- */
    div[data-testid="stChatMessage"] {
        background-color: rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        margin-bottom: 10px;
    }
    
    /* ANIMAÇÃO DE FLUTUAR A FOTO */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
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

# ANTIGRAVITY FIX: models/gemini-2.5-flash
model = genai.GenerativeModel('models/gemini-2.5-flash', system_instruction="Você é o CDM, IA de Vendas Elite. Responda no idioma do usuário.")

# --- 4. MEMÓRIA ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "Olá! Sou o CDM. Vamos bater as metas de hoje? 🚀"}]

# --- 5. FOTO DE PERFIL (CORREÇÃO DO ZOOM) ---
st.markdown('<div style="display: flex; justify-content: center; padding: 30px 0;">', unsafe_allow_html=True)

# Procura o arquivo
nomes_possiveis = ["perfil.jpg", "perfil.png", "perfil.jpeg", "perfil.jpg.png"]
arquivo_encontrado = None

for nome in nomes_possiveis:
    if os.path.exists(nome):
        arquivo_encontrado = nome
        break

# HTML DA IMAGEM (Com estilo INLINE para garantir o corte redondo)
if arquivo_encontrado:
    with open(arquivo_encontrado, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    
    mime = "image/png" if "png" in arquivo_encontrado else "image/jpeg"
    
    # O SEGREDO ESTÁ AQUI: object-fit: cover FORÇADO
    st.markdown(f"""
    <img src="data:{mime};base64,{encoded}" 
         style="
            width: 150px; 
            height: 150px; 
            border-radius: 50%; 
            object-fit: cover; 
            object-position: top center; 
            border: 4px solid #4facfe; 
            box-shadow: 0px 0px 30px rgba(79, 172, 254, 0.7);
            animation: float 6s ease-in-out infinite;
         ">
    """, unsafe_allow_html=True)
else:
    # Robô (Reserva)
    st.markdown("""
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" 
         style="width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 4px solid #4facfe; animation: float 6s ease-in-out infinite;">
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- 6. EXIBIR O CHAT ---
st.markdown('<div style="margin-bottom: 50px;">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    avatar = "⚡" if msg["role"] == "model" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

# --- 7. BARRA DE DIGITAÇÃO (AGORA BRANCA) ---
if prompt := st.chat_input("Digite sua mensagem aqui..."):
    # 1. Mostra msg do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. IA Responde
    with st.chat_message("model", avatar="⚡"):
        try:
            # FIX: Use safe history slicing to include all BUT the last (just added) message
            # This is safer than filtering by content which might accidentally remove duplicates
            chat_hist = [{"role": m["role"], "parts": [m["content"]]} 
                         for m in st.session_state.messages[:-1]]
            
            chat = model.start_chat(history=chat_hist)
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
        except Exception as e:
            st.error(f"Erro: {e}")
