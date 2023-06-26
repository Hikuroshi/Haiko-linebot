from linebot.models import TextSendMessage, FlexSendMessage
from jikanpy import Jikan
from helpers import line_bot_api
import time


last_command_time = 0
anime_info_count = {}

def hk_anime(command, token):
    global last_command_time, anime_info_count

    current_time = time.time()
    elapsed_time = current_time - last_command_time

    if elapsed_time < 20:
        wait_time = int(20 - elapsed_time)
        return f"Tunggu {wait_time} detik lagi untuk dapat mengirim perintah"

    last_command_time = current_time

    parts = command.split(" ", 2)

    if len(parts) >= 3:
        action = parts[1]
        query = parts[2]

        jikan = Jikan()

        if action.lower() in ["info", "i"]:
            anime = jikan.search("anime", query, page=1)

            if anime["data"]:
                carousels = []

                for anime_info in anime["data"][:5]:
                    image_url = anime_info["images"]["jpg"]["large_image_url"]
                    genres = ', '.join([genre['name'] for genre in anime_info["genres"]])
                    themes = ', '.join([theme['name'] for theme in anime_info["themes"]])
                    
                    score = anime_info["score"]
                    if score is None:
                        score = "N/A"
                        star_count = 0
                        gray_star_count = 5
                    else:
                        score = float(score)
                        star_count = int(score / 2)
                        gray_star_count = 5 - star_count
                    
                    stars = []
                    for _ in range(star_count):
                        stars.append({
                            "type": "icon",
                            "size": "sm",
                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                        })

                    for _ in range(gray_star_count):
                        stars.append({
                            "type": "icon",
                            "size": "sm",
                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                        })

                    carousel = {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "image",
                                    "url": image_url,
                                    "size": "full",
                                    "aspectMode": "cover",
                                    "aspectRatio": "2:3",
                                    "gravity": "top"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": anime_info['title'],
                                                    "size": "xl",
                                                    "color": "#ffffff",
                                                    "weight": "bold",
                                                    "wrap": True
                                                }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "margin": "md",
                                            "contents": stars + [
                                                {
                                                    "type": "text",
                                                    "text": str(score),
                                                    "size": "sm",
                                                    "color": "#999999",
                                                    "margin": "md",
                                                    "flex": 0
                                                }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "margin": "md",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": genres + " | " + themes,
                                                    "color": "#ebebeb",
                                                    "size": "sm",
                                                    "flex": 0,
                                                    "wrap": True
                                                }
                                            ]
                                        },
                                    ],
                                    "position": "absolute",
                                    "offsetBottom": "0px",
                                    "offsetStart": "0px",
                                    "offsetEnd": "0px",
                                    "backgroundColor": "#000000cc",
                                    "paddingAll": "20px",
                                    "paddingTop": "18px"
                                }
                            ],
                            "paddingAll": "0px"
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "postback",
                                            "label": "Selengkapnya",
                                            "data": f"anime info {anime_info['mal_id']}",
                                            "displayText": anime_info['title']
                                        },
                                        "color": "#ffffff",
                                        "gravity": "center",
                                        "style": "link"
                                    }
                                    ],
                                    "borderWidth": "1px",
                                    "cornerRadius": "4px",
                                    "spacing": "sm",
                                    "borderColor": "#ffffff",
                                    "height": "40px"
                                }
                            ],
                            "backgroundColor": "#000000",
                            "paddingAll": "20px",
                            "paddingTop": "0px"
                        }
                    }

                    carousels.append(carousel)

                flex_message = FlexSendMessage(alt_text="Informasi Anime", contents={"type": "carousel", "contents": carousels})
                line_bot_api.reply_message(token, flex_message)
                anime_info_count = {}
                return
            else:
                return f"Tidak ditemukan informasi anime dengan judul {query}"

        else:
            return "Perintah tidak valid. Gunakan format 'hk anime <action> <query>'."

    else:
        return "Format perintah 'anime' tidak valid. Gunakan format 'hk anime <action> <query>'."
    

def hk_postback_anime(data, reply_token):
    global anime_info_count
    
    parts = data.split(" ", 2)
    
    if len(parts) >= 2:
        action = parts[1]
        anime_id = parts[2]
        
        jikan = Jikan()
        
        if action.lower() == "info":
            anime = jikan.anime(anime_id)
            anime_info = anime["data"]
            
            if anime_id not in anime_info_count:
                anime_info_count[anime_id] = 0

            if anime_info_count[anime_id] < 2:
                anime_info_count[anime_id] += 1
            
                flex_content = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": anime_info["title"] or "Unknown",
                            "weight": "bold",
                            "size": "xxl",
                            "margin": "md",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": anime_info["synopsis"] or "Unknown",
                            "size": "xs",
                            "margin": "md",
                            "wrap": True
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "xxl",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "Episode",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(anime_info["episodes"]) or "Unknown",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end",
                                    "offsetEnd": "1px"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "Durasi",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": anime_info["duration"] or "Unknown",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end",
                                    "offsetEnd": "1px"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "Status",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": anime_info["status"] or "Unknown",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end",
                                    "offsetEnd": "1px"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0,
                                    "text": "Tayang"
                                },
                                {
                                    "type": "text",
                                    "text": anime_info['aired']['string'] or "Unknown",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end",
                                    "offsetEnd": "1px"
                                }
                                ]
                            },
                            {
                                "type": "separator",
                                "margin": "xxl"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0,
                                    "text": "Rank"
                                },
                                {
                                    "type": "text",
                                    "text": str(anime_info["rank"]) or "Unknown",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end",
                                    "offsetEnd": "1px"
                                }
                                ],
                                "paddingTop": "xl"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0,
                                    "text": "Popularitas"
                                },
                                {
                                    "type": "text",
                                    "text": str(anime_info["popularity"]) or "Unknown",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end",
                                    "offsetEnd": "1px"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0,
                                    "text": "Rating"
                                },
                                {
                                    "type": "text",
                                    "text": anime_info["rating"] or "Unknown",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end",
                                    "offsetEnd": "1px"
                                }
                                ]
                            }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "size": "sm",
                                "color": "#555555",
                                "text": "Studio",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": ', '.join([studio['name'] for studio in anime_info['studios']]) or "Unknown",
                                "size": "sm",
                                "color": "#111111",
                                "align": "end",
                                "offsetEnd": "1px",
                                "wrap": True
                            }
                            ],
                            "margin": "xl"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0,
                                "text": "Produser",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": ', '.join([producer['name'] for producer in anime_info['producers']]) or "Unknown",
                                "size": "sm",
                                "color": "#111111",
                                "align": "end",
                                "offsetEnd": "1px",
                                "wrap": True
                            }
                            ]
                        }
                        ]
                    },
                    "styles": {
                        "footer": {
                        "separator": True
                        }
                    }
                }

                flex_message = FlexSendMessage(alt_text="Informasi Lengkap Anime", contents=flex_content)
                line_bot_api.reply_message(reply_token, flex_message)
                return

    line_bot_api.reply_message(reply_token, TextSendMessage(text="Informasi lengkap sudah ada, scroll ke atas atau ketik ulang perintah"))
    return 