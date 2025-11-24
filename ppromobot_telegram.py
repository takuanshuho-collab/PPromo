import os
import google.generativeai as genai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from PIL import Image

# 1. Carrega as chaves
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

# 2. Configura o Google Gemini
genai.configure(api_key=GEMINI_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Mande a foto do encarte e eu uso IA para ler as ofertas. 🤖🛒")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Recebi! Estou enviando para a IA analisar... 🧠")

    try:
        # --- BAIXAR A IMAGEM ---
        photo_file = update.message.photo[-1]
        new_file = await context.bot.get_file(photo_file.file_id)
        nome_arquivo = "encarte_temp.jpg"
        await new_file.download_to_drive(nome_arquivo)
        
        # --- A MÁGICA DO GEMINI ♊ ---
        # Configuração do modelo
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = """
        Analise este encarte de supermercado.
        Liste os 5 principais produtos e seus preços que aparecem na imagem.
        Formate a saída assim:
        - PRODUTO: [Nome] | PREÇO: [Valor]
        
        Se não encontrar preços, diga apenas que não encontrou ofertas visíveis.
        """
        
        # --- CORREÇÃO AQUI (Uso do WITH) ---
        # O 'with' abre a imagem e a fecha automaticamente quando o bloco termina
        with Image.open(nome_arquivo) as img:
            response = model.generate_content([prompt, img])
            texto_resposta = response.text
        
        # Agora o arquivo já está fechado, podemos enviar a resposta e deletar
        await update.message.reply_text(f"🛒 **Ofertas Encontradas:**\n\n{texto_resposta}")
        
        # Limpeza
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)

    except Exception as e:
        await update.message.reply_text(f"Erro na análise: {str(e)}")

if __name__ == '__main__':
    if not TELEGRAM_TOKEN or not GEMINI_KEY:
        print("ERRO: Verifique seu arquivo .env (Precisa do Token e da API Key)")
        exit()

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("Bot com IA Gemini Iniciado...")
    application.run_polling()