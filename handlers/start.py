from telegram.ext.callbackcontext import CallbackContext
from handlers import import_user
from telegram  import Update,ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler
)
from help import cpd_head_chat_id

def start(update:Update,context:CallbackContext)->None:
    store_user_id_the_member(update,context)
    print(update.message.text.split())
    l=update.message.text.split()
    if len(l) ==  2:
        #he/she was select for the member for push notification
        context.bot.send_message(
            chat_id = update.effective_user.id,
            text = l[1]
        )

    elif update.effective_user.id ==  cpd_head_chat_id:
        context.bot.send_message(
            chat_id = update.effective_user.id,
            text = "head",
            reply_markup = ReplyKeyboardMarkup(
                [
                    ["Push Notification"]
                ],resize_keyboard=True)
        )
    else:
        context.bot.send_message(
            chat_id = update.effective_user.id,
            text = "hi!!"
        )




start_handler = CommandHandler('start',start)


def send(update,context):
    print("/send")

send_handler = CommandHandler('send',send)


from members import update_member
def store_user_id_the_member(update:Update,context:CallbackContext)->None:
    payload = {

        'user_name' :update.effective_user.username,
        'user_id' :update.effective_user.id
    }
    update_member(payload)
    





