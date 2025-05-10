from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = '8180023065:AAE0IIRmyPD88XIIOp9xpjr7RFbYxcsENXc'

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🇺🇿 Ўзбек тили"), KeyboardButton("🇷🇺 Русский язык")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Ассалому алайкум! Илтимос, тилни танланг / Здравствуйте! Пожалуйста, выберите язык:", reply_markup=reply_markup)

# Обработка выбора языка
async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🇺🇿 Ўзбек тили":
        await update.message.reply_text("Сиз ўзбек тилини танладингиз.")
    elif text == "🇷🇺 Русский язык":
        await update.message.reply_text("Вы выбрали русский язык.")
    else:
        await update.message.reply_text("Илтимос, тилни танлаш учун тугмалардан фойдаланинг / Пожалуйста, выберите язык с помощью кнопок.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_language_choice))

    print("Бот запущен и ожидает выбора языка...")
    app.run_polling()

if __name__ == '__main__':
    main()