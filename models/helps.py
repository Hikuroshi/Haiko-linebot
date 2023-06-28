from linebot.models import FlexSendMessage
from helpers import line_bot_api, generate_soft_color
import random

def hk_help(reply_token):
    all_command = [
        {
            "judul": "Daftar Perintah",
            "perintah": "hk help",
            "deskripsi": "Menampilkan Daftar Perintah"
        },
        {
            "judul": "Pesan Custom",
            "perintah": "hk set <pesan> up <balasan>",
            "deskripsi": "Menambahkan Pesan custom dengan bebas"
        },
        {
            "judul": "Quote Judul",
            "perintah": "hk quote title <judul anime>\nhk q t <judul anime>",
            "deskripsi": "Quote Random Berdasarkan Judul Anime"
        },
        {
            "judul": "Quote Karakter",
            "perintah": "hk quote char <nama karakter>\nhk q c <nama karakter>",
            "deskripsi": "Quote Random Berdasarkan Nama Karakter Anime"
        },
        {
            "judul": "Quote Random",
            "perintah": "hk quote random\nhk q r",
            "deskripsi": "Lihat quote anime acak"
        },
        {
            "judul": "Informasi Anime",
            "perintah": "hk anime info <judul anime>\nhk a i <judul anime>",
            "deskripsi": "Menampilkan Informasi Anime"
        },
        {
            "judul": "Anime Trending",
            "perintah": "hk anime trending\nhk a t",
            "deskripsi": "Menampilkan anime trending saat ini"
        }
    ]

    bubbles = []

    for command in all_command:
        bubble = {
            "type": "bubble",
            "size": "micro",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": command["judul"],
                        "color": "#ffffff",
                        "align": "start",
                        "size": "md",
                        "gravity": "center",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": command["perintah"],
                        "color": "#ffffff",
                        "align": "start",
                        "size": "xxs",
                        "gravity": "center",
                        "margin": "sm",
                        "wrap": True
                    }
                ],
                "backgroundColor": generate_soft_color(),
                "paddingTop": "19px",
                "paddingAll": "12px",
                "paddingBottom": "16px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": command["deskripsi"],
                                "color": "#8C8C8C",
                                "size": "sm",
                                "wrap": True
                            }
                        ],
                        "flex": 1
                    }
                ],
                "spacing": "md",
                "paddingAll": "12px"
            },
            "styles": {
                "footer": {
                    "separator": False
                }
            }
        }

        bubbles.append(bubble)

    carousel_content = {
        "type": "carousel",
        "contents": bubbles
    }

    line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text="Daftar Perintah", contents=carousel_content))
    return