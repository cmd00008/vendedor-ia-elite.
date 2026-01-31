import streamlit as st
import time
import os
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURAÇÃO (Simples e Leve para não travar)
st.set_page_config(
    page_title="Elite AI",
    layout="centered",
    initial_sidebar_state="expanded" # Abre a lateral automaticamente
)

# -----------------------------------------------------------------------------
# 2. BACKEND (GEMINI AI RESTORED) - Conexão Real (Mantida)
# -----------------------------------------------------------------------------
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        api_key = st.secrets.get("GOOGLE_API_KEY")

    if api_key:
        genai.configure(api_key=api_key)
        
        # --- SYSTEM INSTRUCTION (MANDATORY LANGUAGE DETECTION) ---
        system_instruction = \"\"\"
Você é o CDM, uma IA de Vendas Global.
SUA REGRA NÚMERO 1 (INVIOLÁVEL): ESPELHAMENTO DE IDIOMA.
- Antes de responder, DETECTE o idioma do usuário.
- Se o usuário falar INGLÊS -> Responda 100% em INGLÊS.
- Se o usuário falar ESPANHOL -> Responda 100% em ESPANHOL.
- Se o usuário falar PORTUGUÊS -> Responda 100% em PORTUGUÊS.
Nunca responda em Português se a pergunta for em Inglês.
Seja curto, grosso e focado em vendas.
\"\"\"
        
        # Usando a versão FLASH 2.5 verificada COM System Instruction
        model = genai.GenerativeModel("models/gemini-2.5-flash", system_instruction=system_instruction)
    else:
        model = None
except Exception as e:
    model = None

# 2. DESIGN (CSS Corrigido para Celular e PC)
st.markdown("""
<style>
    /* Fundo Preto Absoluto */
    .stApp { background-color: #000000; color: white; }

    /* Estilo da Foto (Redonda e Centralizada) */
    .css-1v0mbdj img, .profile-pic {
        border-radius: 50%;
        border: 4px solid #00C9FF;
        box-shadow: 0 0 20px rgba(0, 201, 255, 0.5);
        object-fit: cover;
    }

    /* Balões de Chat (Legíveis no Mobile) */
    .stChatMessage { background-color: transparent !important; }
    
    /* Balão IA */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background: #111 !important;
        border-left: 3px solid #00C9FF;
    }
    
    /* Texto Branco Sempre */
    p, div, span { color: white !important; font-family: sans-serif; }

    /* Esconder menus chatos */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. BARRA LATERAL (ONDE VOCÊ COLOCA A FOTO)
with st.sidebar:
    st.title("📸 Configuração")
    st.info("Para sua foto aparecer, clique abaixo e selecione o arquivo do seu computador/celular.")
    
    # BOTÃO DE UPLOAD (A Mágica Acontece Aqui)
    arquivo_foto = st.file_uploader("Carregar Foto de Perfil", type=["jpg", "png", "jpeg"])

# 4. ÁREA PRINCIPAL
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # SE TIVER FOTO, MOSTRA A FOTO. SE NÃO, MOSTRA UM ÍCONE.
    if arquivo_foto is not None:
        image = Image.open(arquivo_foto)
        st.image(image, width=150) # Mostra a foto que você subiu
    elif os.path.exists("perfil.png"):
        # Fallback local se existir
        st.image("perfil.png", width=150)
    else:
        st.markdown('<div style="font-size: 80px; text-align: center;">�</div>', unsafe_allow_html=True)
        st.caption("Suba sua foto no menu lateral 👈")

    st.markdown("<h1 style='text-align: center; color: #00C9FF;'>IA VENDAS ELITE</h1>", unsafe_allow_html=True)

# 5. CHAT (Lógica com IA Real)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Olá! Sistema reconectado. Qual produto vamos vender hoje?"}]

# Mostra histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Campo de Digitação
if prompt := st.chat_input("Digite aqui..."):
    # Usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Resposta IA (Imediata)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if model:
            try:
                message_placeholder.markdown("⚡ Processando...")
                # Prompt Direto (Instrução já está no Sistema)
                response = model.generate_content(prompt)
                resposta = response.text
            except Exception as e:
                resposta = f"Erro na API: {e}"
        else:
            time.sleep(0.5)
            resposta = f"Entendi. A estratégia para '{prompt}' já está sendo processada. (Modo Simulação: Configure API Key)"

        message_placeholder.write(resposta)

    st.session_state.messages.append({"role": "assistant", "content": resposta})
