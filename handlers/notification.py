from typing import ContextManager
from telegram import ext, message
from telegram.ext import MessageFilter
from members import members, update_member

class FilterMember(MessageFilter):
    def filter(self, message):
        try:
            num = int(message.text)
            if num >= 1 and num <=len(members()):
                return 1
            else:
                return 0 
        except ValueError:
            return 0



from telegram import Update,ReplyKeyboardMarkup,ParseMode,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    ConversationHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler

)
from telegram.ext.filters import Filters
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup

MEMBER,MESSAGE = range(2)

def list_members(update:Update,context:CallbackContext)->None:
    context.user_data['message_id'] = []
    display(update,context)
    return MEMBER

def member_detail(update,context):
    print(update.message.text)
    context.user_data['member_id'] = int(update.message.text)-1
    display_detail(update,context,context.user_data['member_id'])
    return MEMBER

def select_member(update,context):
    query = update.callback_query
    query.answer()
    context.user_data['member']={
        "user_id":int(query.data)
    }
    display_detail(update,context,context.user_data['member_id'],flag=1)
    return MESSAGE


def delete_message(update,context):
    try:
        message_id =  context.user_data['message_id'][-1]
        context.bot.delete_message(
            chat_id = update.effective_user.id,
            message_id = message_id
        )
        context.user_data['message_id'].pop()
    except:
        print("message id not found")
from members import add_member_message
def message_for_member(update,context):
    print("update",update.message.text)
    msg = update.message.text
    x = context.user_data['member']
    print("x",x)
    x['msg'] = msg
    
    print("payload",x)
    add_member_message(x)
    msg = "\t\t\tNew Notification\t\t\t\n{}\nfrom head of cpd @MebaGT".format(msg)
    context.bot.send_message(
        chat_id = x['user_id'],
        text = msg
    )
    delete_message(update,context)
    delete_message(update,context)
    return MEMBER





    
def esc(update,context):
    delete_message(update,context)
    delete_message(update,context)
    return MEMBER


def cancel(update,context):
    delete_message(update,context)
    context.bot.send_message(
        chat_id = update.effective_user.id,
        text = "canceled!",
        reply_markup =  ReplyKeyboardMarkup(
                [
                    ["Push Notification"]
        ],resize_keyboard=True)

    )

    return ConversationHandler.END


def unknown(update,context):
    print("unkown input")



btn = ["Push Notification",'Cancel']
notification_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(btn),list_members)],
    states={
        MEMBER : [
            MessageHandler(FilterMember(),member_detail),
            CallbackQueryHandler(select_member)

        ],
        MESSAGE:[
            MessageHandler(Filters.text & ~(Filters.text(btn))& ~(Filters.command),message_for_member),
            CommandHandler('esc',esc)
        ]
    },
    fallbacks=[
        MessageHandler(Filters.text(btn),cancel),
        MessageHandler( Filters.all & ~(FilterMember()),unknown)

    ]
    
)

def display(update:Update,context:CallbackContext)->None:
    msg = "\t\t\tList OF CPD MEMEBERS\t\t\t\n\n FULL_NAME,TelegramUserName\n"
    j=0
    for i in members():
        msg = msg + "{}➖ {},@{}\n".format(j,i['full_name'],i['telegram_user_name'])
        j=j+1
    result = context.bot.send_message(

        chat_id  = update.effective_user.id,
        text = msg,
        parse_mode=ParseMode.HTML,
        reply_markup = ReplyKeyboardMarkup([
            ['Cancel']

        ],resize_keyboard=True)
    )
    context.bot.send_message(
        chat_id = update.effective_user.id,
        text = "enete the number for detail"
    )


def display_detail(update,context,member_id,flag=None):
    delete_message(update,context)
    member = members()[member_id]
    msg = "\t\t\t👤CPD MEMBER DETAIL\t\t\t\n✔️Full Name = {}\n✔️Telegram UserName = @{}\n\t\t\t\t\t📬Messages\t\t\t\n".format(member['full_name'],member['telegram_user_name'])
    if member['messages']:
        for i in member['messages']:
            msg = msg + "✔️"+i +"\n"

    else:
        msg = msg + "zero notice"
    if not flag:
        result = context.bot.send_message(
            chat_id = update.effective_user.id,
            text = msg,
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(text="send notice",callback_data=member['user_id'])]
            ])
        )
        context.user_data['message_id'].append(result['message_id'])
    if flag:
        result = context.bot.send_message(
            chat_id = update.effective_user.id,
            text = "eneter the next notice that should push to  @{} \n use this cmd to /esc ".format(member['telegram_user_name'])
        )
        context.user_data['message_id'].append(result['message_id'])
        result = context.bot.send_message(
        chat_id = update.effective_user.id,
        text = msg,
        )
        context.user_data['message_id'].append(result['message_id'])


    print(member)

