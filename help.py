import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('token')
cpd_head_chat_id = int(os.getenv('cpd_head'))
