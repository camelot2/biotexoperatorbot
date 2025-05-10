import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = '8180023065:AAE0IIRmyPD88XIIOp9xpjr7RFbYxcsENXc'

# Состояния для ConversationHandler
LANGUAGE, CONSUMER_TYPE, NEW_CHOICE = range(3)

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🇺🇿 Ўзбек тили"), KeyboardButton("🇷🇺 Русский язык")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Ассалому алайкум! Илтимос, тилни танланг / Здравствуйте! Пожалуйста, выберите язык:", reply_markup=reply_markup)
    return LANGUAGE

# Обработка выбора языка
async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🇺🇿 Ўзбек тили":
        keyboard = [
            [KeyboardButton("Аҳоли"), KeyboardButton("Юридик")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Илтимос, тоифангизни танланг:", reply_markup=reply_markup)
        return CONSUMER_TYPE

    elif text == "🇷🇺 Русский язык":
        keyboard = [
            [KeyboardButton("Физический потребитель"), KeyboardButton("Юридический потребитель")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Пожалуйста, выберите тип потребителя:", reply_markup=reply_markup)
        return CONSUMER_TYPE

    else:
        await update.message.reply_text("Илтимос, тилни танлаш учун тугмалардан фойдаланинг / Пожалуйста, выберите язык с помощью кнопок.")
        return LANGUAGE

# Обработка выбора "Физический" или "Юридический"
async def handle_consumer_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🇺🇿 Аҳоли" or text == "Физический потребитель":
        keyboard = [
            [KeyboardButton("Тулов микдори"), KeyboardButton("Офис манзили")],
            [KeyboardButton("Хисоб ракамимни биламан"), KeyboardButton("Савол ва мурожаат колдириш")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Танлаш учун тугмани босинг / Нажмите на кнопку, чтобы выбрать", reply_markup=reply_markup)
        return NEW_CHOICE

    elif text == "Юридик" or text == "Юридический потребитель":
        await update.message.reply_text("Обработка юридического потребителя не реализована.")
        return ConversationHandler.END
    
    else:
        await update.message.reply_text("Неверный выбор, пожалуйста, выберите из предложенных опций.")
        return CONSUMER_TYPE

# Обработка выбора одного из новых пунктов
async def handle_new_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Тулов микдори" or text == "Сумма платежа":
        await update.message.reply_text("Вы выбрали: Сумма платежа / Тулов микдори")

    elif text == "Офис манзили" or text == "Адрес офиса":
        await update.message.reply_text("Вы выбрали: Адрес офиса / Офис манзили")

    elif text == "Хисоб ракамимни биламан" or text == "Я знаю свой лицевой счет":
        await update.message.reply_text("Введите свой лицевой счёт для дальнейшего поиска.")

    elif text == "Савол ва мурожаат колдириш" or text == "Оставить вопросов и обращений":
        await update.message.reply_text("Оставьте свой вопрос или обращение, и мы с вами свяжемся.")

    else:
        await update.message.reply_text("Неверный выбор. Пожалуйста, выберите из предложенных опций.")

    return NEW_CHOICE

# Завершаем разговор
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Процесс завершён.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_language_choice)],
            CONSUMER_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_consumer_type)],
            NEW_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_choice)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conversation_handler)

    print("Бот запущен и ожидает выбора языка...")
    app.run_polling()

if __name__ == '__main__':
    main()
