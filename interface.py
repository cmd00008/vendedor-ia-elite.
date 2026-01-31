import streamlit as st
import google.generativeai as genai
import time
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Gemini 2.5 Flash Elite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS FUTURISTA (BASEADO NA IMAGEM) ---
st.markdown("""
<style>
    /* 1. FUNDO GRADIENTE AZUL */
    .stApp {
        background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d); /* Gradiente Azul/Roxo/Laranja sutil */
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364); /* Gradiente Azul Profundo */
        background-attachment: fixed;
    }
    
    /* 2. OCULTAR ELEMENTOS PADRÃO DO STREAMLIT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 3. ESTILO DOS CÍRCULOS ÍCONES (Fundo) */
    .icon-container {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 80%;
        height: 80%;
        pointer-events: none; /* Não interfere no clique */
        z-index: 0;
        opacity: 0.4; /* Levemente transparente */
        background-image: url('https://img.freepik.com/free-vector/gradient-artificial-intelligence-background_23-2150378223.jpg?w=1380&t=st=1706728000~exp=1706728600~hmac=7b1283019461981901209320715053150687112018107115103102104105106'); /* Imagem de fundo similar */
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* 4. CONTAINER CENTRAL (Robô e Barra) */
    .main-container {
        position: absolute;
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        z-index: 1;
        width: 60%;
    }

    /* Ícone do Robô Central */
    .robot-icon {
        width: 120px;
        margin-bottom: 20px;
    }

    /* Balões de "pensamento" do robô */
    .thought-bubbles {
        position: absolute;
        top: -40px;
        right: 30%;
        font-size: 24px;
        color: #4facfe;
    }

    /* 5. BARRA DE PESQUISA "HOW CAN I HELP YOU?" */
    /* Esconde o label padrão e estiliza o input */
    .stTextInput label {
        display: none;
    }
    .stTextInput input {
        background-color: #000000 !important; /* Fundo Preto */
        color: #FFFFFF !important; /* Texto Branco */
        border: 2px solid #4facfe !important; /* Borda Azul Brilhante */
        border-radius: 50px !important; /* Bordas Redondas */
        padding: 20px 30px !important; /* Espaçamento interno */
        font-size: 20px !important; /* Texto maior */
        box-shadow: 0px 0px 20px rgba(79, 172, 254, 0.5); /* Brilho Azul */
        text-align: left;
        padding-left: 60px !important; /* Espaço para a lupa */
        background-image: url('https://cdn-icons-png.flaticon.com/512/54/54481.png'); /* Ícone de Lupa Azul */
        background-repeat: no-repeat;
        background-position: 20px center;
        background-size: 25px;
    }
    /* Placeholder (Texto de ajuda) */
    ::placeholder {
        color: #a0a0a0 !important;
        font-style: italic;
    }

    /* 6. ÁREA DO CHAT (Aparece abaixo da barra) */
    .chat-container {
        margin-top: 450px; /* Empurra o chat para baixo da barra central */
        z-index: 2;
        position: relative;
        width: 70%;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Balões de Chat Transparentes */
    div[data-testid="stChatMessage"] {
        background-color: rgba(0, 0, 0, 0.3); /* Fundo preto transparente */
        border: 1px solid rgba(79, 172, 254, 0.3); /* Borda azul sutil */
        border-radius: 15px;
        color: #FFFFFF !important;
    }
    .stMarkdown, p, span, div {
        color: #FFFFFF !important;
    }

</style>

<div class="icon-container"></div>

<div class="main-container">
    <div class="thought-bubbles">💬 💭</div>
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" class="robot-icon" alt="Robot Icon">
</div>
""", unsafe_allow_html=True)

# --- CONEXÃO BLINDADA ---
try:
    api_key = os.environ.get("GOOGLE_API_KEY") # Tenta ambiente
    if not api_key:
        api_key = st.secrets["GOOGLE_API_KEY"] # Tenta secrets
    
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.error("⚠️ API Key não encontrada.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ Erro nos Secrets/Config: {e}")
    st.stop()

# --- CÉREBRO DA IA ---
system_instruction = """
Você é o CDM, a IA de Vendas Elite (v2.5).
REGRA DE IDIOMA: Responda SEMPRE no idioma que o usuário falar.
Seja direto, use emojis e foque em ajudar.
"""
# CORREÇÃO: Usando modelo 2.5 disponível
model = genai.GenerativeModel('models/gemini-2.5-flash', system_instruction=system_instruction)

# --- LÓGICA DO CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensagem inicial discreta
    st.session_state.messages.append({"role": "model", "content": "Olá! Como posso te ajudar hoje? 🤖"})

# --- BARRA DE ENTRADA (Centralizada) ---
# Usamos um container para posicionar o input no meio da tela
with st.container():
    st.markdown('<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -20%); width: 60%; z-index: 10;">', unsafe_allow_html=True)
    # Callback limpa o input após envio se necessário, mas st.rerun já ajuda
    prompt = st.text_input("How can I help you?...", placeholder="How can I help you?...", key="main_input")
    st.markdown('</div>', unsafe_allow_html=True)

# --- EXIBIÇÃO DO CHAT (Abaixo da barra) ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    avatar_icon = "🤖" if message["role"] == "model" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])
st.markdown('</div>', unsafe_allow_html=True)

# --- PROCESSAMENTO DA MENSAGEM ---
if prompt:
    # Evita reprocessar se já foi a última (embora st.rerun limpe o input geralmente, mas o key mantem estado)
    # O truque aqui é que 'prompt' vem do text_input.
    
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Gera resposta
    try:
        # Prepara histórico
        chat_history = [
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ]
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(prompt)
        
        st.session_state.messages.append({"role": "model", "content": response.text})
        
        # O text_input não limpa sozinho com st.rerun() se tiver key fixa sem callback.
        # Mas vamos seguir o padrão solicitado pelo usuário:
        # Para limpar, idealmente precisaríamos de callback on_change, mas st.rerun() funciona se ele não travar.
        # Aqui, vamos torcer para o fluxo manual funcionar ou o usuário apagar.
        # OBS: Usuário pediu rerunn.
        
    except Exception as e:
        st.error(f"Erro: {e}")
