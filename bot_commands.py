
from telegram import Update
from telegram.ext import ContextTypes

async def mostrar_comandos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comandos = (
        "📋 Lista de comandos disponibles:\n\n"
        "/start - Mensaje de bienvenida\n"
        "/commands - Mostrar esta lista de comandos\n"
        "/help - Información sobre cómo usar el bot\n"
        "/Donate - Link para Donar a través de Ko-Fi\n"
    )
    await update.message.reply_text(comandos)
