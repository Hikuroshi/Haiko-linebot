from linebot.models import TextSendMessage
from helpers import read_data, write_data, line_bot_api, group_report


def hk_custom_message(command, profile):
    data = read_data()
    user_name = profile.display_name
    user_id = profile.user_id
    set_message = len("set ")
    up_message = command.find(" up ")

    if up_message != -1:
        cmd_msg = command[set_message:up_message].strip()
        res_msg = command[up_message + len(" up "):].strip()

        custom_messages = data.get("custom_message", [])

        for custom_msg in custom_messages:
            if custom_msg["set"] == cmd_msg:
                custom_msg["up"] = res_msg
                write_data(data)
                send_custom_message_report(user_name, user_id, cmd_msg, res_msg, new_msg = False)
                return "Pesan custom berhasil diperbarui."

        custom_messages.append({"set": cmd_msg, "up": res_msg})
        data["custom_message"] = custom_messages

        write_data(data)
        send_custom_message_report(user_name, user_id, cmd_msg, res_msg, new_msg = True)
        return "Pesan custom berhasil disimpan."
    else:
        return "Format perintah 'set' tidak valid. Gunakan format 'hk set <command> up <response>'."

def send_custom_message_report(user_name, user_id, cmd_msg, res_msg, new_msg):
    custom_message_report = TextSendMessage(text=
        f"Pesan custom telah {'ditambahkan' if new_msg else 'diperbarui'} oleh:\n" \
        f"Nama User: {user_name}\n" \
        f"User ID: {user_id}\n" \
        f"Pesan: {cmd_msg}\n" \
        f"Balasan: {res_msg or '-'}"
    )
    line_bot_api.push_message(group_report, custom_message_report)
    return


def hk_custom_message_response(text):
    data = read_data()
    custom_messages = data.get("custom_message", [])
    message = None
    
    for custom_message in custom_messages:
        if custom_message["set"].lower() == text.lower():
            return custom_message["up"]