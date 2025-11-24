import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# 1. Configuração
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
gemini_key = os.getenv('GEMINI_API_KEY')
session_string = os.getenv('SESSION_STRING')

# Configura IA
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 2. Conexão Híbrida (PC vs Nuvem)
if session_string:
    print("☁️ Modo NUVEM detectado: Usando StringSession.")
    # Na nuvem, usamos a string da memória
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
else:
    print("💻 Modo LOCAL detectado: Usando arquivo de sessão.")
    # No PC, cria o arquivo 'sessao_espiao.session'
    client = TelegramClient('sessao_espiao', api_id, api_hash)

# 3. Lista de Alvos
# Coloque aqui os usernames ou IDs dos canais que quer monitorar
CANAIS_ALVO = [
    'me',  # Mensagens Salvas (Sempre bom manter para testes)
    # 'atacadao_ofertas', 
    # 'supermercado_bairro',
]

print(f"🕵️‍♂️ Espião Iniciado! Monitorando: {CANAIS_ALVO}")

@client.on(events.NewMessage(chats=CANAIS_ALVO))
async def handler(event):
    if event.photo:
        print(f"📸 Oferta detectada no chat: {event.chat_id}")
        
        # Baixa a foto temporariamente
        path = await event.download_media(file="temp_oferta.jpg")
        
        try:
            print("🧠 Analisando com IA...")
            prompt = """
            Analise este encarte de supermercado.
            Liste APENAS os 5 produtos com preços mais vantajosos.
            Formato: 🛒 [Produto] -> [Preço]
            Seja breve.
            """
            
            with Image.open(path) as img:
                response = model.generate_content([prompt, img])
                texto = response.text
            
            # Envia para você (Saved Messages)
            # Dica: Adicionamos o nome do canal de origem para você saber de onde veio
            origem = f"Canal ID: {event.chat_id}"
            if hasattr(event.chat, 'username') and event.chat.username:
                origem = f"@{event.chat.username}"
                
            msg_final = f"🚨 **OFERTA DETECTADA** em {origem}\n\n{texto}"
            
            await client.send_message('me', msg_final)
            print("✅ Relatório enviado!")

            os.remove(path)

        except Exception as e:
            print(f"❌ Erro: {e}")

async def main():
    # Inicia a conexão (usa a string ou o arquivo automaticamente)
    await client.start()
    print("✅ Sistema Operante. Pressione Ctrl+C para parar.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Mantém a correção para o seu Windows
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Desligando...")