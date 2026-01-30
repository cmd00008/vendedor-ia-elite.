import google.generativeai as genai
import os

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    # Use the hardcoded key if env is missing (just for this debugging step if needed)
    pass 

genai.configure(api_key=api_key)

try:
    models = genai.list_models()
    with open("models.txt", "w") as f:
        for m in models:
            if "generateContent" in m.supported_generation_methods:
                f.write(f"{m.name}\n")
    print("Models listed to models.txt")
except Exception as e:
    print(f"Error: {e}")
