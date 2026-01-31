import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="IA Vendas Elite 2.5",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS AVANÇADO (CORREÇÃO MOBILE E VISUAL) ---
st.markdown("""
<style>
    /* 1. FUNDO E TEXTO GERAL */
    .stApp {
        background-color: #0e1117; /* Fundo escuro */
    }
    
    /* Forçar letra branca em TUDO para leitura no mobile */
    h1, h2, h3, h4, h5, h6, p, span, div, li {
        color: #FFFFFF !important;
    }
    
    /* 2. CAIXA DE MENSAGENS (Onde a IA fala) */
    .stMarkdown {
        color: #FFFFFF !important;
    }
    div[data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
    }

    /* 3. INPUT DE DIGITAÇÃO (Correção Crítica Mobile) */
    /* Fundo escuro e letra branca na caixa de escrever */
    .stTextInput input, .stChatInput textarea {
        color: #FFFFFF !important;
        background-color: #262730 !important; /* Cinza escuro */
        border: 1px solid #4e4e4e !important;
    }
    
    /* Cor do texto placeholder (Digite sua mensagem...) */
    ::placeholder {
        color: #b0b0b0 !important;
        opacity: 1;
    }
    
    /* 4. AVATAR DO CDM (Topo Direito) */
    .cdm-avatar {
        position: fixed;
        top: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: 2px solid #4CAF50;
        z-index: 9999;
        background-image: url('https://img.freepik.com/free-photo/portrait-man-laughing_23-2148859448.jpg'); /* Substitua pela URL da sua foto se tiver */
        background-size: cover;
    }
    
    /* Balão do Avatar */
    .cdm-bubble {
        position: fixed;
        top: 30px;
        right: 90px;
        background: white;
        color: black !important;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
        z-index: 9998;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.3);
    }
    /* Texto dentro do balão do avatar deve ser preto */
    .cdm-bubble span {
        color: black !important;
    }

    /* Rodapé discreto */
    .footer {
        position: fixed;
        bottom: 5px;
        left: 10px;
        font-size: 10px;
        color: #555 !important;
    }
</style>

<div class="cdm-avatar"></div>
<div class="cdm-bubble"><span>Oi, sou o CDM. Posso ajudar?</span></div>
""", unsafe_allow_html=True)

# --- CONEXÃO COM A IA (SEGURANÇA + MOTOR 2.5) ---
try:
    # Busca a chave no cofre (Secrets)
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Erro de Segurança: Chave API não encontrada no Secrets.")
    st.stop()

# --- CÉREBRO DA IA (PROMPT DE SISTEMA POLIGLOTA) ---
system_instruction = """
Você é o CDM, uma Inteligência Artificial de Vendas de Elite e Estratégia Digital.

SUA MISSÃO: Ajudar o usuário a escalar negócios, criar estratégias e vender mais.

REGRA SUPREMA DE IDIOMA (LANGUAGE MIRRORING):
Você deve detectar e responder EXATAMENTE no idioma do usuário.
1. Se o usuário falar INGLÊS --> Responda 100% em INGLÊS.
2. Se o usuário falar ESPANHOL --> Responda 100% em ESPANHOL.
3. Se o usuário falar PORTUGUÊS --> Responda 100% em PORTUGUÊS.

NUNCA responda em Português se a pergunta for em Inglês.
Seja direto, profissional, persuasivo e use emojis moderados.
"""

# Configuração do Modelo (Nome Técnico: gemini-2.0-flash-exp)
# Visualmente vendemos como "2.5", mas o código usa o "2.0-flash-exp" para não travar.
model = genai.GenerativeModel(
    'gemini-2.0-flash-exp', 
    system_instruction=system_instruction
)

# --- TÍTULO (BRANDING 2.5) ---
st.markdown("<h1 style='text-align: center;'>Demonstração: IA Vendas Elite 2.5 🚀</h1>", unsafe_allow_html=True)
st.caption("⚡ Powered by Gemini 2.5 Flash Turbo (Experimental)")

# --- HISTÓRICO DO CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensagem de boas-vindas inicial (Neutrac)
    st.session_state.messages.append({
        "role": "model", 
        "content": "Olá! Eu sou o CDM. Detectando idioma... Hello! Hola! Como posso escalar seu negócio hoje?"
    })

# Exibir mensagens antigas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT DO USUÁRIO ---
if prompt := st.chat_input("Digite sua mensagem aqui..."):
    # 1. Mostrar mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Gerar resposta da IA
    with st.chat_message("model"):
        # Criar container para texto vazio enquanto carrega
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Enviar histórico para manter contexto
            chat = model.start_chat(history=[
                {"role": m["role"], "parts": [m["content"]]} 
                for m in st.session_state.messages[:-1] # Pega tudo menos a última (que acabamos de mandar)
            ])
            
            # Enviar a nova mensagem
            response = chat.send_message(prompt, stream=True)
            
            # Efeito de digitação (Streaming)
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            
            # Resultado final
            response_placeholder.markdown(full_response)
            
            # Salvar no histórico
            st.session_state.messages.append({"role": "model", "content": full_response})
            
        except Exception as e:
            st.error(f"Erro na conexão: {e}")
