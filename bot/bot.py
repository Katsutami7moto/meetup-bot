import logging

from telegram import ParseMode, ReplyKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CommandHandler, Dispatcher, Filters,
                          MessageHandler, Updater)

from .admin_panel import get_main_menu, open_admin_panel
from .bot_helpers import read_json, write_json


def get_hello_message() -> str:
    hello_message = read_json('hello.json')['hello']
    return hello_message


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_hello_message(),
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu(update.effective_user.id)
    )


def return_to_main_menu(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Главное меню',
        reply_markup=get_main_menu(update.effective_user.id)
    )


def handle_menu_actions(update: Update, context: CallbackContext):
    menu_actions = {
        'Главное меню': return_to_main_menu,
        
    }
    action_text = update.message.text
    if action_text in menu_actions:
        action = menu_actions[action_text]
        action(update, context)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Пожалуйста, выберите действие из меню'
        )


def launch_bot(token):
    updater = Updater(token=token, use_context=True)
    dispatcher: Dispatcher = updater.dispatcher
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()

    menu_actions_handler = MessageHandler(Filters.text, handle_menu_actions)
    dispatcher.add_handler(menu_actions_handler)

    job_queue = updater.job_queue

    updater.idle()
