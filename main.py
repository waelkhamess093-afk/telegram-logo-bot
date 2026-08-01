
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from PIL import Image
import os

TOKEN = "8536670434:...stmo"

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()

    input_path = "input.jpg"
    output_path = "output.jpg"

    await photo_file.download_to_drive(input_path)

    image = Image.open(input_path).convert("RGB")
    logo = Image.open("logo.jpg").convert("RGB")

    # تصغير اللوجو
    new_width = image.width // 4
    ratio = new_width / logo.width
    new_height = int(logo.height * ratio)
    logo = logo.resize((new_width, new_height))

    # أسفل الشمال
    x = 20
    y = image.height - logo.height - 20

    image.paste(logo, (x, y))

    image.save(output_path)

    await update.message.reply_photo(photo=open(output_path, "rb"))

    os.remove(input_path)
    os.remove(output_path)

app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.PHOTO, photo))

print("Bot Started...")
app.run_polling()
