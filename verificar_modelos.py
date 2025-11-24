import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

print("🔍 Consultando modelos disponíveis para sua chave API...\n")

for m in genai.list_models():
    # Filtra apenas modelos que aceitam gerar conteúdo (generateContent)
    if 'generateContent' in m.supported_generation_methods:
        print(f"- Nome: {m.name}")