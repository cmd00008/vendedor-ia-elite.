import streamlit as st
import google.generativeai as genai
import time
import os

# --- CONFIGURAÇÃO DA PÁGINA (TOP DE LINHA) ---
st.set_page_config(
    page_title="Gemini 2.5 Flash Elite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS DE LUXO (VISUAL PERFEITO NO MOBILE) ---
st.markdown("""
<style>
    /* 1. FUNDO E CONTRASTE */
    .stApp {
        background-color: #0e1117; /* Preto Profundo */
    }
    
    /* Forçar TODAS as letras a serem BRANCAS para leitura perfeita */
    h1, h2, h3, h4, h5, h6, p, span, div, li, label {
        color: #FFFFFF !important;
    }
    
    /* 2. CAIXAS DE MENSAGEM (Chat) */
    .stMarkdown {
        color: #FFFFFF !important;
    }
    div[data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.08); /* Vidro fumê */
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
    }

    /* 3. CAIXA DE DIGITAÇÃO (Fundo Escuro para não ofuscar) */
    .stTextInput input, .stChatInput textarea {
        color: #FFFFFF !important;       /* Letra Branca */
        background-color: #202123 !important; /* Cinza Chumbo */
        border: 1px solid #505050 !important;
    }
    ::placeholder {
        color: #a0a0a0 !important; /* Cinza claro no texto de ajuda */
    }
    
    /* 4. BRANDING 2.5 (Topo da Tela) */
    .branding-badge {
        position: fixed;
        top: 60px;
        right: 20px;
        background: linear-gradient(45deg, #FF0000, #FF8800);
        color: white !important;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 10px;
        z-index: 9997;
        box-shadow: 0px 0px 10px rgba(255, 69, 0, 0.5);
    }

    /* 5. AVATAR CDM */
    .cdm-avatar {
        position: fixed;
        top: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: 2px solid #00FF00;
        z-index: 9999;
        background-image: url('https://img.freepik.com/free-photo/portrait-man-laughing_23-2148859448.jpg');
        background-size: cover;
    }
</style>

<div class="cdm-avatar"></div>
<div class="branding-badge">⚡ v2.5 TURBO</div>
""", unsafe_allow_html=True)

# --- CONEXÃO SEGURA (SEM ERRO 404) ---
# Usando estrutura robusta para garantir conexão tanto Local quanto Cloud
try:
    api_key = os.environ.get("GOOGLE_API_KEY") # Tenta ambiente primeiro
    if not api_key:
        api_key = st.secrets["GOOGLE_API_KEY"] # Tenta secrets do Streamlit
    
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.error("⚠️ API Key não encontrada.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ Erro de Configuração: {e}")
    st.stop()

# --- CÉREBRO POLIGLOTA (Detecta Idioma Sozinho) ---
system_instruction = """
Você é o CDM, a IA de Vendas mais avançada do mercado (Versão 2.5).

REGRA DE IDIOMA (ESPELHAMENTO):
- Se o usuário falar INGLÊS -> Responda em INGLÊS.
- Se o usuário falar ESPANHOL -> Responda em ESPANHOL.
- Se o usuário falar PORTUGUÊS -> Responda em PORTUGUÊS.

COMPORTAMENTO:
Seja confiante, rápido e persuasivo. Use emojis. Foque em fechar negócios.
"""

# --- O MOTOR BLINDADO ---
# CORREÇÃO AUTOMÁTICA DE ANTIGRAVITY:
# O código original pedia 'gemini-1.5-flash', porém neste ambiente (2026),
# diagnosticamos que '1.5' gera 404 e '2.5' é o disponível.
# Mantendo 'models/gemini-2.5-flash' para garantir funcionalidade.
model = genai.GenerativeModel(
    'models/gemini-2.5-flash', 
    system_instruction=system_instruction
)

# --- INTERFACE ---
st.markdown("<h1 style='text-align: center;'>IA Vendas Elite <span style='color:#FF4B4B !important;'>2.5</span> 🚀</h1>", unsafe_allow_html=True)
st.caption("⚡ Sistema Operacional: Gemini 2.5 Flash Experimental")

# --- LÓGICA DO CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "model", 
        "content": "Olá! Hello! ¡Hola! Sou o CDM 2.5. Qual meta vamos bater hoje?"
    })

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite aqui para acelerar suas vendas..."):
    # Usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Resposta da IA
    with st.chat_message("model"):
        response_placeholder = st.empty()
        try:
            # Constrói histórico compatível com a API gemini
            # (A API espera 'user' e 'model', o state usa 'user' e 'model')
            chat_history = [
                {"role": m["role"], "parts": [m["content"]]} 
                for m in st.session_state.messages[:-1]
            ]
            
            chat = model.start_chat(history=chat_history)
            
            # Envia a mensagem com streaming
            response = chat.send_message(prompt, stream=True)
            
            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "model", "content": full_response})
            
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
