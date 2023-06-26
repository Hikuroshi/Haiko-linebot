import time
import requests
from linebot.models import FlexSendMessage
from jikanpy import Jikan
import random
from helpers import line_bot_api

last_request_time = 0

def hk_quote(command, token):
    global last_request_time
    current_time = time.time()

    if current_time - last_request_time >= 30:
        parts = command.split(" ", 2)

        if len(parts) >= 3:
            prompt, query = parts[1], parts[2]

            if prompt in ['title', 't']:
                url = f"http://animechan.melosh.space/random/anime?title={query}"
            elif prompt in ['char', 'c']:
                url = f"http://animechan.melosh.space/random/character?name={query}"
            else:
                return "Format perintah 'quote' tidak valid. Gunakan format 'hk quote title <judul anime>' atau 'hk quote char <nama karakter>'."

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if data:
                    anime = data["anime"]
                    character = data["character"]
                    quote_text = data["quote"]

                    jikan = Jikan()
                    search_result = jikan.search('characters', character, page=1)
                    mal_id = search_result["data"][0]["mal_id"]

                    character_result = jikan.characters(mal_id, extension="pictures")
                    character_image = random.choice(character_result["data"])["jpg"]["image_url"]

                    flex_content = {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "image",
                                    "url": character_image,
                                    "size": "full",
                                    "aspectMode": "cover",
                                    "aspectRatio": "3:4",
                                    "gravity": "center"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [],
                                    "position": "absolute",
                                    "background": {
                                        "type": "linearGradient",
                                        "angle": "0deg",
                                        "endColor": "#00000000",
                                        "startColor": "#000000ee"
                                    },
                                    "width": "100%",
                                    "height": "50%",
                                    "offsetBottom": "0px",
                                    "offsetStart": "0px",
                                    "offsetEnd": "0px"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                                {
                                                    "type": "box",
                                                    "layout": "horizontal",
                                                    "contents": [
                                                        {
                                                            "type": "text",
                                                            "text": character,
                                                            "size": "xl",
                                                            "align": "center",
                                                            "color": "#ffffff"
                                                        }
                                                    ]
                                                },
                                                {
                                                    "type": "box",
                                                    "layout": "horizontal",
                                                    "contents": [
                                                        {
                                                            "type": "text",
                                                            "text": anime,
                                                            "color": "#efefef",
                                                            "size": "xxs",
                                                            "align": "center"
                                                        }
                                                    ],
                                                    "spacing": "xs"
                                                },
                                                {
                                                    "type": "box",
                                                    "layout": "horizontal",
                                                    "contents": [
                                                        {
                                                            "type": "text",
                                                            "text": f"\"{quote_text}\"",
                                                            "color": "#C8C8C8",
                                                            "size": "sm",
                                                            "align": "center",
                                                            "style": "italic",
                                                            "wrap": True
                                                        }
                                                    ],
                                                    "paddingTop": "md"
                                                }
                                            ],
                                            "spacing": "xs"
                                        }
                                    ],
                                    "position": "absolute",
                                    "offsetBottom": "0px",
                                    "offsetStart": "0px",
                                    "offsetEnd": "0px",
                                    "paddingAll": "20px"
                                }
                            ],
                            "paddingAll": "0px"
                        }
                    }
                    
                    # Kirim pesan balasan dengan Flexbox kutipan anime dan gambar karakter
                    flex_message = FlexSendMessage(alt_text="Kutipan Anime", contents=flex_content)
                    line_bot_api.reply_message(token, flex_message)
                    return
                else:
                    return f"Tidak ditemukan kutipan untuk {'anime dengan judul' if prompt in ['title', 't'] else 'karakter dengan nama'} {query}"
            else:
                return "Terjadi kesalahan saat mengambil kutipan anime"

            last_request_time = time.time()
        else:
            return "Format perintah 'quote' tidak valid. Gunakan format 'hk quote title <judul anime>' atau 'hk quote char <nama karakter>'."
    else:
        remaining_time = int(30 - (current_time - last_request_time))
        return f"Tunggu {remaining_time} detik lagi untuk mengirim permintaan."