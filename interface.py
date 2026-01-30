import streamlit as st
import google.generativeai as genai
import time

# 1. Configuração da Página
st.set_page_config(page_title="IA Vendas Elite", page_icon="🤖")

# Visual Limpo: CSS para esconder Menu, Header e Footer
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("Demonstração: IA Vendas Elite")
st.markdown("---")

# 2. Configurações da API (Blindagem e st.secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("❌ Erro: Secret 'GOOGLE_API_KEY' não encontrado. Por favor, configure o arquivo .streamlit/secrets.toml.")
    st.stop()

# Modelo: Versão Final Gratuita (Blindada)
# O usuário reportou que a versão 1.5 tem erro 429, migrando para 2.5 conforme solicitado.
try:
    # Tenta instanciar o modelo solicitado
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    # Fallback seguro caso '2.5' seja typo ou não exista ainda, mas mantendo a lógica de armadura
    model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Inicialização do Histórico de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Exibir mensagens do histórico
for message in st.session_state.messages:
    # Avatars definidos: Robô para assistente, Usuário para user
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 5. Entrada do Usuário
if prompt := st.chat_input("Digite sua mensagem para o vendedor..."):
    # Adiciona mensagem do usuário ao histórico visual
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 6. Lógica do Vendedor (System Prompt + Persona)
    system_prompt = """
    ATUE COMO: Um Vendedor Consultivo Especialista Global.
    
    SUA MISSÃO:
    1. Identificar o idioma e o DIALETO/GÍRIA REGIONAL do cliente (ex: Português de Portugal vs. Brasil, Gírias de SP vs. Nordeste, Inglês Britânico vs. Texano).
    2. ADAPTAR seu tom de voz e vocabulário para espelhar o estilo do cliente (Rapport).
    3. Identificar a necessidade oculta do cliente e oferecer o produto perfeito.
    
    REGRA DE OURO: NUNCA escreva rótulos como [Dialeto], [Ação] ou [Resposta]. NUNCA explique seu raciocínio. Apenas responda diretamente ao usuário como se fosse uma conversa natural de WhatsApp.
    """
    
    # Prepara o conteúdo (Simulando chat stateless com contexto imediato ou full history se desejado)
    # Para garantir robustez e foco na instrução:
    content_to_send = [prompt, system_prompt]

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        
        # Blindagem Anti-Erro 429
        try:
            # Envia para o modelo
            response = model.generate_content(content_to_send)
            
            # Extrair texto da resposta
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # Adiciona resposta ao histórico
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception:
            # Mensagem amigável solicitada em caso de erro (Técnico oculto)
            st.warning('⏳ O Vendedor está atendendo muitos clientes. Aguarde 30 segundos e tente novamente.')
