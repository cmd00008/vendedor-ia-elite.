import streamlit as st
import os
import google.generativeai as genai

# 1. Configuração da Página (Deve ser o primeiro comando)
st.set_page_config(page_title="IA Vendas Elite 2.5", layout="centered")

# 2. CSS Personalizado (O "Segredo" do Design)
st.markdown("""
<style>
    /* Importando fonte moderna do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* Aplicando a fonte em tudo */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* FUNDO GERAL (Gradiente Dark Moderno) */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        background-attachment: fixed;
    }

    /* Esconder o menu padrão do topo e rodapé para ficar limpo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ESTILO DO TÍTULO (Gradiente no Texto) */
    h1 {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        text-align: center;
        padding-bottom: 20px;
    }
    
    h3 {
        color: #e2e8f0 !important;
        text-align: center;
        font-weight: 300 !important;
        font-size: 1.2rem !important;
    }

    /* CONTAINER PRINCIPAL (Glassmorphism) */
    /* Cria um efeito de vidro ao redor do conteúdo central, se desejar */
    .block-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 3rem !important;
        margin-top: 50px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* ESTILIZANDO A BARRA DE INPUT DE CHAT */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    
    .stChatInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 30px !important;
    }
    
    /* MENSAGENS DO CHAT */
    /* Usuário */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(79, 172, 254, 0.1);
        border-radius: 15px;
        border: 1px solid rgba(79, 172, 254, 0.3);
    }
    
    /* Botões de Idioma (Pequenos ajustes) */
    div.stButton > button {
        background-color: transparent;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 20px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #4facfe;
        border-color: #4facfe;
        color: white;
        transform: scale(1.05);
    }

</style>
""", unsafe_allow_html=True)

# 3. Configuração da API (Backend Integro)
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except:
        pass

model = None
if api_key:
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
    except Exception as e:
        # Fallback silencioso ou log, caso mude novamente
        st.error(f"Erro ao carregar modelo: {e}")

# Inicializa estado do idioma
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'pt'

# 4. Layout da Aplicação

# Seção de Idiomas (Topo)
col1, col2, col3, col4, col5 = st.columns([4, 1, 1, 1, 4])
with col2:
    if st.button("BR"):
        st.session_state['lang'] = 'pt'
        st.rerun()
with col3:
    if st.button("US"):
        st.session_state['lang'] = 'en'
        st.rerun()
with col4:
    if st.button("ES"):
        st.session_state['lang'] = 'es'
        st.rerun()

# Espaçamento
st.write("") 

# Título e Subtítulo
st.markdown("<h1>Demonstração: IA Vendas Elite 2.5</h1>", unsafe_allow_html=True)
st.markdown("<h3>🚀 Versão 2.5 Flash Turbo (Super Rápida)</h3>", unsafe_allow_html=True)

st.divider()

# --- LÓGICA DO CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Pronta para ir direto ao ponto e otimizar seu tempo? Diga-me, qual seu desafio principal hoje?"}
    ]

# Exibir mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input
if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
