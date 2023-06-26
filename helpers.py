from linebot.models import TextSendMessage
from linebot import LineBotApi, WebhookHandler
from dotenv import load_dotenv
import json
import os
import sys
import random


load_dotenv()
sys.path.append('/')

data_json = "database/data.json"

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))
group_report = os.getenv("GROUP_REPORT")

def read_data():
    with open(data_json, 'r') as file:
        data = json.load(file)
    return data

def write_data(data):
    with open(data_json, 'w') as file:
        json.dump(data, file, indent=4)
    return

def check_group(group_id):
    data = read_data()
    group_ids = [group['group_id'] for group in data['groups']]
    
    if group_id not in group_ids:
        summary = line_bot_api.get_group_summary(group_id)
        message = TextSendMessage(text=f"Gomenasai, grup kamu belum terdaftar, silahkan hubungi line.me/ti/p/~hikuroshi")
        group_id_report = TextSendMessage(text=
                    f"Haiko telah diundang tapi grup tidak terdaftar. \n" \
                    f"Nama Grup: {summary.group_name} \n" \
                    f"Grup ID: {summary.group_id}"
        )
        
        line_bot_api.push_message(group_id, message)
        line_bot_api.push_message(os.getenv("GROUP_REPORT"), group_id_report)
        
        line_bot_api.leave_group(group_id)
        return


def generate_soft_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    average = (r + g + b) // 3

    r = (average + r) // 2
    g = (average + g) // 2
    b = (average + b) // 2

    hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)

    return hex_color