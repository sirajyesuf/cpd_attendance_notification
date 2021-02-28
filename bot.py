import logging
from telegram.ext import Updater,PicklePersistence
from dotenv import load_dotenv
from handlers import import_user

from help import token

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

#handlers
from handlers.start import start_handler
from handlers.import_user import import_members_handler
from handlers.export_user  import export_user_command_handler
from handlers.notification import notification_handler
from handlers.start import send_handler
def main():
    per = PicklePersistence(filename='persistance')
    updater = Updater(token=token,persistence=per,use_context=True)
    dispatcher = updater.dispatcher

    #add handlers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(import_members_handler)
    dispatcher.add_handler(export_user_command_handler)
    dispatcher.add_handler(notification_handler)
    dispatcher.add_handler(send_handler)
    



    
   


    
    #start the bot
    updater.start_polling()
    #until you press ctrl-c
    updater.idle()


if __name__ == '__main__':
    main()