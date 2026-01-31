import streamlit as st
import os
import google.generativeai as genai

# --- Configuração da Página ---
st.set_page_config(page_title="IA Vendas Elite 2.5", layout="centered")

# --- CSS PESADO PARA RESTAURAR O VISUAL ---
st.markdown("""
    <style>
    /* 1. Forçar a Imagem de Fundo (Petronas Towers) em TELA CHEIA */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1549420078-45e0d37e624c?q=80&w=2574&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* 2. Deixar o cabeçalho do Streamlit transparente para a imagem subir */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }

    /* 3. Estilo dos Textos (Branco com Sombra para Leitura) */
    h1, h2, h3, p, span, div {
        color: #ffffff !important;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.8); /* Sombra preta forte */
    }

    /* 4. Estilo dos Botões de Bandeira (Pequenos e Discretos no Topo) */
    div.stButton > button {
        background-color: rgba(0, 0, 0, 0.6); /* Fundo semi-transparente */
        color: white;
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 8px;
        font-size: 20px;
    }
    div.stButton > button:hover {
        background-color: #00ff00; /* Brilho verde ao passar o mouse */
        color: black !important;
        border-color: #00ff00;
    }

    /* 5. Ajuste do Input de Chat (Para não sumir no fundo) */
    .stTextInput > div > div > input {
        background-color: rgba(0,0,0,0.7);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Configuração da API (Backend Restaurado) ---
api_key = os.environ.get("GOOGLE_API_KEY")
# Fallback para secrets se necessário
if not api_key:
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except:
        pass

model = None
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

# --- LAYOUT DO TOPO (Bandeiras + Avatar) ---
# Inicializa estado do idioma
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'pt'

col_flags, col_spacer, col_avatar = st.columns([3, 4, 1])

with col_flags:
    # Colunas internas para as bandeiras ficarem juntinhas
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        if st.button("🇧🇷"): 
            st.session_state['lang'] = 'pt'
            st.rerun()
    with c2:
        if st.button("🇺🇸"): 
            st.session_state['lang'] = 'en'
            st.rerun()
    with c3:
        if st.button("🇪🇸"): 
            st.session_state['lang'] = 'es'
            st.rerun()

with col_avatar:
    # Avatar redondo (simulado)
    st.image("https://randomuser.me/api/portraits/men/32.jpg", width=60)

# --- TÍTULO PRINCIPAL ---
st.markdown("<br>", unsafe_allow_html=True) # Espaço
st.markdown("""
    <h1 style='font-size: 3.5rem; line-height: 1.1; margin-bottom: 0;'>
        Demonstração: IA<br>Vendas Elite 2.5
    </h1>
    <p style='color: #ddd; font-style: italic; font-size: 1rem;'>
        🚀 Versão 2.5 Flash Turbo (Super Rápida)
    </p>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True) # Espaço para separar do chat

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
    with st.chat_message("user"):
        st.write(prompt)
    
    # Lógica Real do Vendedor
    if model:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("⏳ ...")
            
            try:
                # Prompt de Sistema Dinâmico
                lang = st.session_state['lang']
                lang_instruction = "Responda em PORTUGUÊS."
                if lang == 'en': lang_instruction = "Responda em INGLÊS."
                elif lang == 'es': lang_instruction = "Responda em ESPANHOL."

                system_prompt = f"""
                ATUE COMO: Um Vendedor Consultivo Especialista Global.
                {lang_instruction}
                1. Identifique o tom do cliente e adapte-se.
                2. Seja persuasivo mas profissional.
                3. Identifique a necessidade oculta.
                """
                
                content_to_send = [prompt, system_prompt]
                response = model.generate_content(content_to_send)
                final_text = response.text
                
                message_placeholder.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
            except Exception as e:
                message_placeholder.error(f"Erro na API: {e}")
    else:
        # Mock de erro se sem chave
        err_msg = "⚠️ Configure a API Key para ver a mágica acontecer."
        with st.chat_message("assistant"):
            st.error(err_msg)
        st.session_state.messages.append({"role": "assistant", "content": err_msg})
