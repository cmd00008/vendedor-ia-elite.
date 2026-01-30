import streamlit as st
import google.generativeai as genai
import requests
from streamlit_lottie import st_lottie
import time

# 1. Configuração da Página
st.set_page_config(page_title="IA Vendas Elite", page_icon="🤖")

# 2. Visual 'Hacker/LiveChat' (CSS)
st.markdown("""
<style>
    /* Esconder Menu, Header, Footer */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Fundo Escuro Geral */
    .stApp {
        background-color: #0e1117;
        color: white;
    }

    /* Tentar forçar a cor das mensagens do usuário (verde) */
    [data-testid="stChatMessage"] {
        background-color: #1e1e1e; /* Fundo padrão (bot) */
        border: 1px solid #333;
    }
</style>
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

# Carregar Animação
lottie_url = "https://lottie.host/58830071-5803-420a-941e-315543769727/I1b3W6l8kE.json"
lottie_json = load_lottieurl(lottie_url)

# Exibir Animação (Se carregou)
if lottie_json:
    st_lottie(lottie_json, height=200, key="coding")

st.title("Demonstração: IA Vendas Elite")
st.markdown("---")

# 3. Configurações da API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("❌ Erro: Secret 'GOOGLE_API_KEY' não encontrado.")
    st.stop()

# 4. Motor (Indispensável): gemini-pro
try:
    model = genai.GenerativeModel('gemini-pro')
except Exception:
    model = genai.GenerativeModel('gemini-pro')

# 5. Inicialização do Histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Exibir mensagens do histórico
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        # Hack visual opcional mantido
        st.markdown(message["content"])

# 7. Entrada do Usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adicionar mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        # Estilo inline verde para usuário
        st.markdown(f'<div style="background-color: #2b8a3e; padding: 10px; border-radius: 5px; color: white;">{prompt}</div>', unsafe_allow_html=True)

    # 8. Lógica do Vendedor
    system_prompt = """
    Aja como um Vendedor Elite. Responda de forma curta e persuasiva. NUNCA use meta-tags como [Dialeto] ou [Resposta].
    """
    
    content_to_send = [prompt, system_prompt]

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        
        # Proteção com try/except
        try:
            response = model.generate_content(content_to_send)
            full_response = response.text
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception:
            # Mensagem de erro amigável
            st.warning('⏳ O Vendedor está recarregando as energias. Tente em 1 minuto.')
