import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="IA Vendas Elite", page_icon="🤖")

# Visual Limpo: Adicione um st.markdown no início com código CSS (<style>) para esconder o MainMenu, o header e o footer do Streamlit.
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("Demonstração: IA Vendas Elite")
st.markdown("---")

# 2. Configurações da API (Carregadas dos Segredos do Streamlit)
# Separação: Garanta que a lógica de st.secrets continue funcionando para a API Key.
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("❌ Erro: Secret 'GOOGLE_API_KEY' não encontrado. Por favor, configure o arquivo .streamlit/secrets.toml.")
    st.stop()

# Modelo: Mude explicitamente a variável model para usar 'gemini-1.5-flash'
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Inicialização do Histórico de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Exibir mensagens do histórico
for message in st.session_state.messages:
    # Avatars: Nos comandos st.chat_message, adicione o parâmetro avatar
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 5. Entrada do Usuário
if prompt := st.chat_input("Digite sua mensagem para o vendedor..."):
    # Adiciona mensagem do usuário ao histórico visual
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 6. Lógica do Vendedor (System Prompt + Input)
    system_prompt = """
    ATUE COMO: Um Vendedor Consultivo Especialista Global.
    
    SUA MISSÃO:
    1. Identificar o idioma e o DIALETO/GÍRIA REGIONAL do cliente (ex: Português de Portugal vs. Brasil, Gírias de SP vs. Nordeste, Inglês Britânico vs. Texano).
    2. ADAPTAR seu tom de voz e vocabulário para espelhar o estilo do cliente (Rapport).
    3. Identificar a necessidade oculta do cliente e oferecer o produto perfeito.
    
    FORMATO DA RESPOSTA:
    [Dialeto Detectado]: <Nome do Dialeto/Região>
    [Resposta do Vendedor]: <Sua resposta vendedora e adaptada>
    """
    
    # Monta o conteúdo para enviar ao Gemini
    content_to_send = [prompt, system_prompt]
    
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        try:
            response = model.generate_content(content_to_send)
            # Extrair texto da resposta
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # Adiciona resposta ao histórico
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Erro na API do Gemini: {e}")
