from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import requests

TOKEN = '6944652004:AAHwny2n9DDJ6TSVsKeXrpCXMJqbtKKsLx8'
CHAT_ID = '781095523'

counter = 0

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Use /help to see available commands.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('/start - Start working with the bot.\n'
                              '/help - Show help information.\n'
                              '/reset - Reset the tap counter.\n'
                              '/stats - Show usage statistics.')

def reset(update: Update, context: CallbackContext) -> None:
    global counter
    counter = 0
    update.message.reply_text('The counter has been reset.')

def stats(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Current counter value: {counter}')

def tap(update: Update, context: CallbackContext) -> None:
    global counter
    counter += 1
    update.message.reply_text(f'Tap counter: {counter}')

def inline_buttons(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Tap", callback_data='tap'),
            InlineKeyboardButton("Reset", callback_data='reset')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose an action:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'tap':
        global counter
        counter += 1
        query.edit_message_text(text=f'Tap counter: {counter}')
    elif query.data == 'reset':
        counter = 0
        query.edit_message_text(text='The counter has been reset.')

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CommandHandler("tap", tap))
    dispatcher.add_handler(CommandHandler("buttons", inline_buttons))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
