import json
from telegram import Update
from telegram.ext import(
    CallbackContext,
    MessageHandler,
    Filters
)
from telegram.files.videonote import VideoNote




def import_members(update:Update,context:CallbackContext)->None:
    print("csv",update)
    # create_store(update,context)
    download_the_csv_file(update,context)
    store_the_data(update,context)










import_members_handler = MessageHandler(Filters.document.file_extension('csv'),import_members)




def download_the_csv_file(update:Update,context:CallbackContext)->None:
    file_id = update.message.document.file_id
    context.bot.get_file(file_id).download('member.csv')

import csv
from help import cpd_head_chat_id
from members import store_members
def store_the_data(update:Update,context:CallbackContext)->None:
    path = "member.csv"
    file = open(path,'r')
    reader = csv.reader(file)
    header = next(reader)
    data = [line for line in reader]
    payload= {
        "members":[]
    }
    for i in data:
        x={
            header[0]:i[0],
            header[1]:i[1],
            'user_id':None,
            'messages':[]
        }
        payload['members'].append(x)
    store_members(payload)

    

def create_store(update:Update,context:CallbackContext)->None:
    pass
    # if context.bot_data.get(cpd_head_chat_id,1):
    #     context.bot_data.clear()
    
    # print("store_data")
    # print(context.bot_data)
    # context.bot_data[cpd_head_chat_id] = []
    # print(context.bot_data[cpd_head_chat_id])








