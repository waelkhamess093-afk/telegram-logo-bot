from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "8536670434:AAGlAwuP5jGYCHYVM09zCwCLg3tItpmstmo""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ابعت أي صورة وأنا هضيف اللوجو عليها.")

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("استلمت الصورة 👍")

app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.PHOTO, photo))

print("Bot Started...")
app.run_polling()
