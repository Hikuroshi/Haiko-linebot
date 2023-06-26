from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, JoinEvent, MemberJoinedEvent, MemberLeftEvent, PostbackEvent, SourceGroup
)
from helpers import check_group, line_bot_api, handler
from models.anime import hk_anime, hk_postback_anime
from models.helps import hk_help
from models.custom_message import hk_custom_message, hk_custom_message_response
from models.quote import hk_quote


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event, destination):
    if isinstance(event.source, SourceGroup):
        check_group(event.source.group_id)
    else:
        return line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Untuk Saat ini Haiko mencegah interaksi diluar grup"))
    
    text = event.message.text
    
    if text.lower().startswith("hk"):
        command = text[3:]
        profile = line_bot_api.get_profile(event.source.user_id)

        if command.lower() == "help":
            message_reply = hk_help(event.reply_token)

        elif command.lower().startswith("set"):
            message_reply = hk_custom_message(command, profile)
            
        elif command.lower().startswith(("quote", "q")):
            message_reply = hk_quote(command, event.reply_token)
            
        elif command.lower().startswith(("anime", "a")):
            message_reply = hk_anime(command, event.reply_token)
            
        else:
            message_reply = "Perintah tidak ditemukan. Ketik 'hk help' untuk melihat daftar perintah"

        if message_reply is not None:
            return line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message_reply))

    else:
        message_reply = hk_custom_message_response(text)
        if message_reply is not None:
            return line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message_reply))


@handler.add(PostbackEvent)
def handle_post_back(event):
    data = event.postback.data
    
    if data.startswith("anime"):
        hk_postback_anime(data, event.reply_token)
    return


@handler.add(JoinEvent)
def handle_join(event):
    data = read_data()
    group_id = event.source.group_id
    group_ids = [group['group_id'] for group in data['groups']]
    
    if group_id in group_ids:
        message = TextSendMessage(text=f"Watashi no nawa Haiko desu, yoroshiku onegaishimasu. \nKetik 'hk help' untuk melihat daftar perintah yang tersedia")
        line_bot_api.reply_message(event.reply_token, message)
    else:
        check_group(group_id)
    return


@handler.add(MemberJoinedEvent)
def handle_member_join(event):
    summary = line_bot_api.get_group_summary(event.source.group_id)
    
    message = f"Welcome to {summary.group_name}.\nJangan lupa cek note dan semoga betah ^^"
    line_bot_api.push_message(event.source.group_id, TextSendMessage(text=message))
    return


@handler.add(MemberLeftEvent)
def handle_member_leave(event):
    line_bot_api.push_message(event.source.group_id, TextSendMessage(text="Itterasshai. Jangan kangen yaa"))
    return
