from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
import yt_dlp
import os
import sys
import asyncio
from bot_commands import mostrar_comandos  # <-- archivo renombrado

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("❌ No se encontró el token. Configura la variable TELEGRAM_BOT_TOKEN.")
    exit(1)

def obtener_ruta_ffmpeg():
    # Si está empacado con PyInstaller, los archivos adicionales estarán en _MEIPASS
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(base, 'ffmpeg', 'bin')  # Ajusta la ruta según tu carpeta
    return ruta

FFMPEG_LOCATION = obtener_ruta_ffmpeg()

# Carpeta temporal para guardar los mp3
TEMP_DIR = "downloads"
os.makedirs(TEMP_DIR, exist_ok=True)

async def descargar_mp3(url):
    """Descarga el audio del video en formato MP3 y devuelve la ruta al archivo."""
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(TEMP_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': FFMPEG_LOCATION,
    }

    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=True)
        titulo = ydl.prepare_filename(info)
        mp3_path = os.path.splitext(titulo)[0] + ".mp3"
        return mp3_path

async def recibir_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    if "youtube.com" in texto or "youtu.be" in texto:
        await update.message.reply_text("🎧 Descargando audio, espera un momento...")
        try:
            mp3_path = await descargar_mp3(texto)
            await update.message.reply_audio(audio=open(mp3_path, "rb"))
            os.remove(mp3_path)
        except Exception as e:
            await update.message.reply_text(f"❌ Error al procesar el enlace:\n{e}")
    else:
        await update.message.reply_text("Envíame un enlace de YouTube para convertirlo a MP3 🎵")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy tu bot 🎵\nEnvíame un enlace de YouTube y lo convertiré a MP3.\nUsa /commands para ver todos los comandos."
    )

# Comando /help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Cómo usar: \n 1️⃣ Envía un enlace de YouTube en el chat.\n2️⃣ El bot descargará el audio y te lo enviará en formato MP3.\n⚠️ Asegúrate de enviar enlaces completos (youtube.com o youtu.be).\n🎵 Disfruta de tu música en MP3 de forma rápida y sencilla."
    )

# Comando /donate
async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💖 ¡Gracias por tu interés en apoyar el bot!\n\n"
        "Si te gusta mi trabajo y quieres ayudarme a seguir creando, puedes hacer una donación a través de Ko-fi:\n"
        "👉 [Haz tu donación aquí] https://ko-fi.com/k4isersp\n\n"
        "Cada aporte, grande o pequeño, ayuda mucho y me permite mantener el bot activo y mejorar sus funciones. ¡Mil gracias por tu apoyo! 🎵"
    )


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("donate", donate))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("commands", mostrar_comandos))

    # Handler para mensajes normales (YouTube)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_mensaje))
    
    print("🤖 Bot en marcha... (Ctrl+C para detener)")
    asyncio.run(app.run_polling())
    

if __name__ == "__main__":
    main()
