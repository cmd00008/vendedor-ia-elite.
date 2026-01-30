import streamlit as st
import google.generativeai as genai
import requests
from streamlit_lottie import st_lottie
import time

# 1. Configuração da Página
st.set_page_config(page_title="IA Vendas Elite 2.0", page_icon="⚡")

# 2. Visual 'Ilha Paradisíaca' (Mobile Friendly)
st.markdown("""
<style>
    /* Esconder Menu, Header, Footer */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Fundo de Ilha (Responsivo) */
    .stApp {
        background-color: #0e1117; /* Fallback */
        background-image: url('[https://images.unsplash.com/photo-1596422846543-75c6fc197f07?q=80&w=2070'](https://images.unsplash.com/photo-1596422846543-75c6fc197f07?q=80&w=2070'));
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: white;
    }

    /* Mensagens com Transparência para Leitura */
    [data-testid="stChatMessage"] {
        background-color: rgba(30, 30, 30, 0.85); /* Fundo preto semi-transparente */
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }
    
    /* --- AVATAR FLUTUANTE (Topo Direito) --- */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); } /* Movimento suave */
        100% { transform: translateY(0px); }
    }

    .floating-avatar {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        border: 3px solid #4CAF50; /* Borda verde */
        
        /* Imagem como fundo para controle de corte/foco */
        background-image: url('[https://i.postimg.cc/SKhHjFHv/Gemini-Generated-Image-7tgz1j7tgz1j7tgz.png'](https://i.postimg.cc/SKhHjFHv/Gemini-Generated-Image-7tgz1j7tgz1j7tgz.png'));
        background-size: cover; 
        background-position: center top; /* Foca na parte de cima (rosto) */
        
        /* Posicionamento no TOPO (Ajustado PRO) */
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        
        /* Animação */
        animation: float 3s ease-in-out infinite;
        transition: transform 0.3s ease;
    }
    
    .floating-avatar:hover {
        transform: scale(1.05);
        cursor: pointer;
    }
    
    .speech-bubble {
        position: absolute;
        top: 35px; /* Ajuste PRO */
        right: 120px; /* Ajuste PRO */
        
        background-color: white;
        color: black;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        
        box-shadow: 0px 2px 5px rgba(0,0,0,0.3);
        font-weight: bold;
        font-size: 14px;
        width: max-content;
        max-width: 200px;
        text-align: right;
        display: block; /* Garante visibilidade */
    }
    
    /* --- CSS Responsivo para Celular --- */
    @media screen and (max-width: 600px) {
        .floating-avatar {
            width: 50px !important; /* Menor no celular */
            height: 50px !important;
            top: 15px !important;
            right: 10px !important;
        }
        .speech-bubble {
            display: block !important; /* Mantém VISÍVEL no celular */
            right: 65px !important; /* Ajusta distância para avatar menor */
            top: 10px !important;
            font-size: 11px !important; /* Texto menor */
            padding: 5px 10px !important;
        }
    }
    
</style>

<!-- Elementos Flutuantes -->
<div class="floating-avatar">
    <div class="speech-bubble">Oi, eu sou CDM. Posso te ajudar?</div>
</div>

""", unsafe_allow_html=True)

# Função para carregar Lottie
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Carregar Animação (Robô 3D)
lottie_url = "[https://lottie.host/58830071-5803-420a-941e-315543769727/I1b3W6l8kE.json](https://lottie.host/58830071-5803-420a-941e-315543769727/I1b3W6l8kE.json)"
lottie_json = load_lottieurl(lottie_url)

# Exibir Animação (Se carregou)
if lottie_json:
    st_lottie(lottie_json, height=200, key="coding")

st.title("Demonstração: IA Vendas Elite 2.0")
st.caption("⚡ Versão Turbo (Chave Validada)")
st.markdown("---")

# 3. Configurações da API (CONEXÃO SEGURA - BLINDADA)
try:
    # Lendo DIRETAMENTE do arquivo .streamlit/secrets.toml
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("❌ Erro CRÍTICO: Chave API não encontrada nos Secrets!")
    st.stop()

# 4. Motor (Turbo Liso): gemini-2.0-flash-exp
try:
    # O user GARANTIU que este é o nome correto sem erro
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
except Exception as e:
    st.error(f"Erro de Modelo: {e}")

# 5. Inicialização do Histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Exibir mensagens do histórico
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat
