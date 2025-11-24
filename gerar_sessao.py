import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

async def main():
    print("🔑 Iniciando gerador de sessão...")
    
    # Cria o cliente com uma sessão vazia na memória
    client = TelegramClient(StringSession(), api_id, api_hash)
    
    # Faz o login (vai pedir telefone e código no terminal)
    await client.start()
    
    print("\n👇 COPIE O CÓDIGO GIGANTE ABAIXO E SALVE NO SEU .ENV COMO 'SESSION_STRING' 👇\n")
    # Aqui a mágica acontece: ele converte o login num texto
    print(client.session.save())
    print("\n👆 ----------------------------------------------------------------------------- 👆")
    
    await client.disconnect()

if __name__ == '__main__':
    # A SOLUÇÃO MANUAL PARA O WINDOWS:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(main())
    except Exception as e:
        print(f"Erro: {e}")