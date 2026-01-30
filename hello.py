import os
import time
import google.generativeai as genai

def chatbot_salesman():
    # 1. Configuration
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Erro: GOOGLE_API_KEY não encontrada.")
        return

    genai.configure(api_key=api_key)
    
    # Using the verified working model
    model = genai.GenerativeModel("gemini-1.5-flash")

    print("\n--- 🤖 Vendedor Global Multimodal (Gemini 1.5) ---")
    print("Posso atender por TEXTO ou ÁUDIO.")
    print("Digite sua mensagem OU o caminho de um arquivo de áudio (ex: audio.mp3).")
    print("------------------------------------------------------\n")

    while True:
        user_input = input("Você: ").strip()
        if user_input.lower() in ["sair", "exit", "quit"]:
            break
        
        content_to_send = []

        # 2. Check if input is a file path (Audio Mode)
        if os.path.exists(user_input) and os.path.isfile(user_input):
            print(f"🎤 Processando áudio: {user_input}...")
            try:
                # Upload file to Gemini
                audio_file = genai.upload_file(user_input)
                
                # Wait for processing
                while audio_file.state.name == "PROCESSING":
                    time.sleep(1)
                    audio_file = genai.get_file(audio_file.name)
                
                if audio_file.state.name == "FAILED":
                    print("⚠️ Erro no processamento do áudio pelo Gemini.")
                    continue
                
                content_to_send = [audio_file]
                print("✅ Áudio pronto! Analisando...")
            except Exception as e:
                print(f"Erro ao carregar arquivo: {e}")
                continue
        else:
            # Text Mode
            if not user_input: continue
            content_to_send = [user_input]

        # 3. System Prompt (Persona de Vendas + Dialeto)
        # Enviamos esta instrução junto com o conteúdo do usuário
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
        
        content_to_send.append(system_prompt)

        # 4. Generate Response
        try:
            response = model.generate_content(content_to_send)
            print(f"\n🤖 {response.text}\n")
        except Exception as e:
            print(f"Erro na API: {e}")

if __name__ == "__main__":
    chatbot_salesman()
