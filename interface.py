import streamlit as st
import os
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="IA Vendas Elite", page_icon="🤖")

st.title("Demonstração: IA Vendas Elite")
st.markdown("---")

# 2. Configurações da API (Carregadas do ambiente ou input lateral)
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    st.warning("⚠️ GOOGLE_API_KEY não encontrada nas variáveis de ambiente.")
    api_key_input = st.text_input("Insira sua API Key do Google:", type="password")
    if api_key_input:
        api_key = api_key_input
else:
    # Opcional: Mostrar que a chave foi carregada com sucesso, mas escondida
    # st.success("API Key carregada com sucesso!")
    pass

if api_key:
    genai.configure(api_key=api_key)
    
    # Modelo (mesmo do hello.py)
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    # 3. Inicialização do Histórico de Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 4. Exibir mensagens do histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. Entrada do Usuário
    if prompt := st.chat_input("Digite sua mensagem para o vendedor..."):
        # Adiciona mensagem do usuário ao histórico visual
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 6. Lógica do Vendedor (System Prompt + Input)
        # Adaptado do hello.py para funcionar no fluxo de chat
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
        # Envia o prompt de sistema junto com a mensagem atual para garantir a persona
        content_to_send = [prompt, system_prompt]
        
        with st.chat_message("assistant"):
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

else:
    st.info("Por favor, configure a API Key para começar.")
