import google.generativeai as genai
import os

# Tenta pegar a chave do ambiente ou input manual
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    # Se não tiver no env, tenta ler do secrets local (dev)
    try:
        with open(".streamlit/secrets.toml", "r") as f:
            for line in f:
                if "GOOGLE_API_KEY" in line:
                    api_key = line.split("=")[1].strip().replace('"', '')
                    break
    except:
        pass

if not api_key:
    print("Erro: GOOGLE_API_KEY não encontrada.")
    exit()

genai.configure(api_key=api_key)

# Usando o modelo 2.5 que está disponível no ambiente
model = genai.GenerativeModel("models/gemini-2.5-flash")

print("Enviando 'Oi' para o modelo...")
try:
    response = model.generate_content("Oi")
    print(f"Resposta do Modelo 2.5: {response.text}")
    print("✅ Sucesso!")
except Exception as e:
    print(f"❌ Erro: {e}")
