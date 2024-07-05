from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests


TOKEN = '6944652004:AAHwny2n9DDJ6TSVsKeXrpCXMJqbtKKsLx8'
WEB_APP_URL = 'http://127.0.0.1:5000/'

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! Use /help to see available commands.')

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Отправка справочной информации о командах бота
    await update.message.reply_text('/start - Start working with the bot.\n'
                                    '/help - Show help information.\n'
                                    '/reset - Reset the tap counter.\n'
                                    '/stats - Show usage statistics.')

# Обработчик команды /reset
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Отправка POST-запроса к веб-приложению для сброса счетчика
    response = requests.post(f'{WEB_APP_URL}/reset')
    if response.status_code == 200:
        await update.message.reply_text('The counter has been reset.')
    else:
        await update.message.reply_text('Failed to reset the counter.')

# Обработчик команды /stats
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Отправка GET-запроса к веб-приложению для получения текущей статистики
    response = requests.get(f'{WEB_APP_URL}/stats')
    if response.status_code == 200:
        data = response.json()
        await update.message.reply_text(f'Current counter value: {data["counter"]}')
    else:
        await update.message.reply_text('Failed to retrieve statistics.')

# Обработчик команды /tap
async def tap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Отправка POST-запроса к веб-приложению для увеличения счетчика
    response = requests.post(f'{WEB_APP_URL}/tap')
    if response.status_code == 200:
        data = response.json()
        await update.message.reply_text(f'Tap counter: {data["counter"]}')
    else:
        await update.message.reply_text('Failed to tap.')

# Обработчик команды /buttons для создания интерактивных кнопок
async def inline_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Создание клавиатуры с кнопками Tap и Reset
    keyboard = [
        [
            InlineKeyboardButton("Tap", callback_data='tap'),
            InlineKeyboardButton("Reset", callback_data='reset')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправка сообщения с кнопками пользователю
    await update.message.reply_text('Choose an action:', reply_markup=reply_markup)

# Обработчик нажатий на интерактивные кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Обработка нажатия кнопки Tap
    if query.data == 'tap':
        response = requests.post(f'{WEB_APP_URL}/tap')
        if response.status_code == 200:
            data = response.json()
            await query.edit_message_text(text=f'Tap counter: {data["counter"]}')
        else:
            await query.edit_message_text(text='Failed to tap.')
    # Обработка нажатия кнопки Reset
    elif query.data == 'reset':
        response = requests.post(f'{WEB_APP_URL}/reset')
        if response.status_code == 200:
            await query.edit_message_text(text='The counter has been reset.')
        else:
            await query.edit_message_text(text='Failed to reset the counter.')

def main() -> None:
    # Создание приложения Telegram
    application = Application.builder().token(TOKEN).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("tap", tap))
    application.add_handler(CommandHandler("buttons", inline_buttons))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
