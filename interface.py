import streamlit as st
import os
import google.generativeai as genai

# --- Configuração da Página ---
st.set_page_config(page_title="IA Vendas Elite 2.5", layout="centered")

# --- CSS Personalizado (O Segredo do Visual) ---
# Aqui definimos a imagem de fundo, fontes e o estilo dos botões
st.markdown("""
    <style>
    /* Imagem de Fundo (Petronas Towers) */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1549420078-45e0d37e624c?q=80&w=2574&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Cor do Texto Geral */
    h1, h2, h3, p, div, span {
        color: white !important;
        text-shadow: 2px 2px 4px #000000; /* Sombra para leitura no fundo */
    }

    /* Estilo do Título Principal */
    h1 {
        font-weight: 800 !important;
        font-size: 3rem !important;
        padding-top: 0px;
    }

    /* Estilo da Mensagem do Usuário (Verde) */
    .st-emotion-cache-1c7y2kd {
        background-color: #2e7d32 !important; /* Verde escuro */
        color: white;
    }
    
    /* Botões de Bandeira (Estilo Transparente) */
    .stButton > button {
        background-color: rgba(0,0,0,0.5);
        border: 1px solid white;
        color: white;
        font-size: 24px;
        border-radius: 10px;
        padding: 5px 15px;
    }
    .stButton > button:hover {
        background-color: rgba(255,255,255,0.2);
        border-color: #00ff00;
        color: white;
    }
    
    /* Avatar no canto superior direito (Simulado via CSS ou Coluna) */
    </style>
    """, unsafe_allow_html=True)

# --- Configuração da API (Backend Restaurado) ---
api_key = os.environ.get("GOOGLE_API_KEY")

# Tenta pegar dos secrets se não estiver no ambiente
if not api_key:
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except:
        pass

if not api_key:
    st.warning("⚠️ API Key não encontrada. Configure GOOGLE_API_KEY no ambiente ou secrets.")
    # Input lateral opcional para fallback
    with st.sidebar:
        api_key = st.text_input("Insira API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Usando o modelo estável 1.5 Flash
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None


# --- Barra de Idiomas (No Topo) ---
if 'idioma' not in st.session_state:
    st.session_state['idioma'] = 'pt' # Padrão

col_lang1, col_lang2, col_lang3, col_vazia = st.columns([1, 1, 1, 5])

with col_lang1:
    if st.button("🇧🇷"):
        st.session_state['idioma'] = 'pt'
        st.rerun()
with col_lang2:
    if st.button("🇺🇸"):
        st.session_state['idioma'] = 'en'
        st.rerun()
with col_lang3:
    if st.button("🇪🇸"):
        st.session_state['idioma'] = 'es'
        st.rerun()

# --- Cabeçalho e Avatar ---
col_texto, col_avatar = st.columns([4, 1])

with col_texto:
    st.markdown("<h1>Demonstração: IA<br>Vendas Elite 2.5</h1>", unsafe_allow_html=True)
    st.caption("🚀 Versão 2.5 Flash Turbo (Super Rápida)")

with col_avatar:
    # Substitua pelo link da sua foto real
    st.image("https://randomuser.me/api/portraits/men/3.jpg", width=80) 

# --- Área de Chat ---
# Inicializa histórico se não existir
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Pronta para ir direto ao ponto e otimizar seu tempo? Diga-me, qual seu desafio principal hoje?"}
    ]

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do Usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    # Mostra mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Resposta (Backend Real)
    if model:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("⏳ Gerando resposta...")
            
            try:
                # System Prompt Dinâmico Baseado no Idioma Escolhido
                idioma_atual = st.session_state['idioma']
                instrucao_idioma = ""
                if idioma_atual == 'pt':
                    instrucao_idioma = "Responda em PORTUGUÊS."
                elif idioma_atual == 'en':
                    instrucao_idioma = "Responda em INGLÊS."
                elif idioma_atual == 'es':
                    instrucao_idioma = "Responda em ESPANHOL."
                
                system_prompt = f"""
                ATUE COMO: Um Vendedor Consultivo Especialista Global.
                {instrucao_idioma}
                1. Identifique o tom do cliente e adapte-se.
                2. Seja persuasivo mas profissional.
                3. Identifique a necessidade oculta.
                """
                
                # Monta a conversa para enviar (Contexto Simplificado)
                content_to_send = [prompt, system_prompt]
                
                response = model.generate_content(content_to_send)
                full_response = response.text
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                message_placeholder.error(f"Erro na API: {e}")
    else:
        with st.chat_message("assistant"):
            st.error("Configure a API Key para receber respostas reais.")
