from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from PIL import Image
import os
import json

TOKEN = "8536670434:AAGlAwuP5jGYCHYVM09zCwCLg3tItpmstmo"

PRODUCTS_FILE = "products.json"


def load_products():
    try:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()

    input_path = "input.jpg"
    output_path = "output.jpg"

    await photo_file.download_to_drive(input_path)

    image = Image.open(input_path).convert("RGB")
    logo = Image.open("logo.png").convert("RGBA")

    # تصغير اللوجو
    new_width = image.width // 10
    ratio = new_width / logo.width
    new_height = int(logo.height * ratio)
    logo = logo.resize((new_width, new_height))

    # أسفل الشمال
    x = 20
    y = image.height - logo.height - 20

    image.paste(logo, (x, y), logo)

    image.save(output_path)

    await update.message.reply_photo(photo=open(output_path, "rb"))

    os.remove(input_path)
    os.remove(output_path)


async def save_amazon_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "amazon." not in text:
        return

    products = load_products()

    if text not in products:
        products.append(text)
        save_products(products)
        await update.message.reply_text("✅ تم حفظ الرابط وسيتم متابعته.")
    else:
        await update.message.reply_text("⚠️ الرابط موجود بالفعل.")


app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.PHOTO, photo))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_amazon_link))

print("Bot Started...")
app.run_polling()
