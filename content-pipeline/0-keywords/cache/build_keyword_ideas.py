"""Merge competitor-gap + seed-modifier results into keyword-ideas.csv.

Sources are inlined from Layer 1b Ahrefs API calls.
"""
import csv
import json
from pathlib import Path

ROOT = Path(r"C:\Users\ndong\Downloads\blog-agent\content-pipeline\0-keywords")

# ---- Source data: competitor_gap (candy.ai, ourdream.ai, nastia.ai) ----
COMPETITOR_DATA = {
    "candy.ai": [
        ("ai girls", 26000, 50, 4542, 2, "informational", ["sitelink"]),
        ("ai girl", 29000, 59, 1052, 4, "informational", ["question", "video_th", "image_th"]),
        ("ai girlfriend chat", 5100, 43, 764, 4, "commercial", ["discussion"]),
        ("ai bf", 2400, 55, 350, 2, "commercial", ["video_th"]),
        ("free ai girlfriend", 14000, 43, 343, 10, "informational", []),
        ("girlfriend ai", 2900, 35, 342, 3, "commercial", ["sitelink", "question", "news", "video_th", "image_th"]),
        ("best ai girlfriend", 3200, 57, 302, 5, "commercial", ["ai_overview", "news", "image_th", "discussion", "video_th", "question"]),
        ("ai sext", 4800, 37, 217, 10, "informational", ["sitelink"]),
        ("create ai boyfriend", 250, 60, 205, 1, "commercial", ["ai_overview", "sitelink"]),
        ("sexting ai", 17000, 36, 196, 15, "informational", []),
        ("ai chat girlfriend", 1800, 47, 171, 4, "commercial", ["sitelink"]),
        ("sext ai", 2000, 31, 154, 5, "commercial", ["sitelink"]),
        ("sex chat ai", 17000, 48, 146, 16, "commercial", []),
        ("ai girl chat", 1800, 42, 135, 5, "commercial", ["video_th"]),
        ("ai gf chat", 1000, 35, 134, 4, "commercial", ["sitelink", "discussion"]),
        ("virtual gf", 1100, 54, 122, 3, "commercial", ["sitelink", "video_th"]),
        ("nsfw chat bot", 2800, 15, 108, 8, "informational", ["sitelink"]),
        ("free nsfw ai chat", 8400, 10, 106, 13, "informational", ["sitelink"]),
        ("best ai girlfriend app", 1300, 31, 101, 5, "commercial", []),
        ("nsfw ai chatbots", 2500, 28, 98, 8, "informational", ["sitelink"]),
        ("ai girlfriend simulator", 2500, 41, 97, 9, "commercial", ["ai_overview", "video_th", "image_th", "discussion", "question"]),
        ("horny ai", 2300, 19, 71, 9, "commercial", []),
        ("sexting bot", 900, 34, 68, 5, "commercial", ["sitelink"]),
        ("nsfw ai chat bots", 1600, 31, 62, 8, "informational", ["sitelink"]),
        ("ai sexting bot", 500, 55, 61, 3, "informational", ["sitelink"]),
        ("nsfw chatbot", 4700, 17, 59, 13, "informational", ["sitelink"]),
        ("ai sexting", 17000, 13, 58, 19, "commercial", ["sitelink"]),
        ("ai girlfriend game", 900, 34, 54, 7, "commercial", ["video_th", "news", "image_th"]),
        ("ai sexchat", 3300, 51, 51, 12, "commercial", ["sitelink"]),
        ("ai boyfriends", 500, 24, 46, 4, "informational", ["sitelink", "news", "video_th", "question"]),
        ("ai chat nsfw", 8500, 35, 44, 17, "commercial", ["sitelink"]),
        ("girlfriend ai chatbot", 350, 23, 42, 3, "commercial", ["discussion", "question", "news", "image_th"]),
        ("hentai chat", 1300, 53, 40, 12, "informational", []),
        ("chat ai girlfriend", 300, 50, 38, 4, "commercial", ["ai_overview", "discussion"]),
        ("virtual girlfriend ai", 500, 55, 36, 5, "commercial", ["sitelink", "news", "image_th", "video_th"]),
        ("horny ai chat", 700, 26, 34, 7, "commercial", []),
        ("ai boyfriend app", 1100, 33, 34, 10, "commercial", ["sitelink"]),
        ("ai porn girlfriend", 1700, 51, 33, 11, "commercial", ["sitelink"]),
        ("ai generated boyfriend", 90, 42, 32, 2, "commercial", ["ai_overview", "image_th", "sitelink", "news", "video_th"]),
        ("free ai girlfriend chatbot", 600, 58, 30, 7, "informational", ["sitelink"]),
        ("best free ai girlfriend", 800, 48, 30, 8, "informational", ["sitelink"]),
        ("ai boyfriend chat", 800, 43, 30, 8, "commercial", ["sitelink", "video_th"]),
        ("ai boyfriend chatbot", 200, 48, 29, 2, "commercial", ["sitelink"]),
        ("best ai girlfriends", 400, 37, 29, 5, "commercial", []),
        ("sexy ai chatbot", 600, 42, 28, 7, "commercial", ["sitelink"]),
        ("ai boyfriend free", 700, 55, 28, 8, "informational", []),
        ("ai nsfw chatbot", 900, 50, 27, 9, "informational", []),
        ("ai nsfw chat", 6300, 35, 26, 18, "informational", []),
        ("boyfriend ai", 800, 50, 24, 10, "commercial", ["question", "discussion", "video_th"]),
        ("my ai boyfriend", 200, 43, 24, 3, "informational", ["sitelink", "discussion", "question"]),
        ("free ai gf", 2400, 49, 24, 14, "informational", ["discussion", "question", "news", "image_th", "video_th"]),
        ("chatbot girlfriend", 150, 56, 24, 4, "informational", ["ai_overview", "sitelink", "question", "news", "image_th"]),
        ("ai sexting app", 500, 48, 20, 8, "commercial", ["snippet", "sitelink"]),
        ("best ai boyfriend", 250, 15, 20, 6, "commercial", ["ai_overview", "image_th", "question", "sitelink"]),
        ("chat with ai boyfriend", 150, 49, 19, 3, "informational", ["sitelink", "discussion"]),
        ("ai chat boyfriend", 500, 38, 19, 8, "commercial", ["snippet", "sitelink"]),
        ("ai sext chat", 700, 46, 19, 10, "informational", ["sitelink"]),
        ("best free ai girlfriend app", 200, 38, 18, 4, "informational", ["sitelink"]),
        ("ai sexting chatbot", 200, 45, 18, 4, "informational", ["sitelink"]),
        ("dirty ai chat", 900, 33, 18, 11, "commercial", ["sitelink", "news", "image_th", "discussion", "video_th"]),
        ("best ai girlfriend apps", 350, 35, 18, 8, "commercial", ["ai_overview", "video_th", "sitelink", "question", "news", "image_th"]),
        ("free nsfw chatbot", 700, 34, 17, 10, "informational", ["sitelink"]),
        ("ai sexting chat", 350, 49, 17, 7, "commercial", ["sitelink"]),
        ("best ai gf app", 200, 60, 17, 4, "commercial", ["sitelink"]),
        ("ai girlfriend experience", 150, 39, 17, 3, "commercial", ["sitelink", "news", "video_th", "question"]),
        ("ai chat girls", 450, 56, 17, 8, "commercial", []),
        ("dirty talking ai", 200, 29, 16, 5, "informational", []),
        ("sexchat ai", 1000, 39, 16, 12, "commercial", ["sitelink"]),
    ],
    "ourdream.ai": [
        ("dream ai chat", 1400, 29, 494, 1, "informational", []),
        ("ai dream girl", 450, 19, 158, 1, "informational", ["sitelink"]),
        ("dream girlfriend ai", 250, 49, 95, 1, "commercial", ["sitelink"]),
        ("create your own ai girl", 600, 47, 53, 4, "commercial", ["video_th", "question"]),
        ("ai furry porn generator", 450, 38, 43, 4, "informational", []),
        ("dream ai girl", 100, 55, 41, 1, "commercial", ["sitelink"]),
        ("nsfw ai companion", 350, 51, 38, 3, "commercial", ["sitelink"]),
        ("dream chat ai", 100, 24, 37, 1, "commercial", []),
        ("nsfw maker", 100, 44, 36, 1, "informational", ["sitelink"]),
        ("nsfw ai creator", 400, 45, 35, 4, "informational", ["sitelink"]),
        ("dream ai porn", 1700, 9, 27, 12, "informational", ["sitelink"]),
        ("ai girlfriend image generator", 350, 44, 21, 6, "informational", []),
        ("best free ai porn generators", 300, 40, 19, 6, "informational", ["sitelink"]),
        ("create your dream girl", 80, 42, 17, 3, "informational", []),
        ("naked ai chat", 450, 57, 17, 8, "commercial", []),
        ("virtual gf ai", 150, 48, 17, 3, "commercial", ["sitelink"]),
        ("ai generator girlfriend", 100, 42, 16, 2, "commercial", ["news", "image_th"]),
        ("ai horny", 250, 45, 15, 6, "commercial", ["question"]),
        ("ai dream girls", 150, 11, 13, 4, "informational", ["sitelink"]),
        ("ai girlfriend creator", 350, 59, 13, 8, "commercial", ["sitelink", "question"]),
        ("create nsfw ai", 90, 39, 13, 2, "informational", ["sitelink"]),
        ("ai chat gf", 400, 43, 12, 9, "commercial", ["sitelink"]),
        ("furry porn ai generator", 250, 32, 12, 7, "informational", ["sitelink"]),
        ("girlfriend maker", 150, 60, 10, 5, "commercial", ["discussion"]),
        ("my ai girlfriend", 600, 48, 9, 13, "commercial", ["question", "discussion", "news", "image_th", "video_th", "sitelink"]),
        ("nsfw ai voice chat", 150, 26, 8, 7, "commercial", ["sitelink"]),
        ("create virtual girlfriend", 60, 53, 8, 2, "commercial", ["sitelink"]),
        ("character nsfw ai", 100, 37, 8, 5, "informational", ["sitelink"]),
        ("furry nsfw ai generator", 150, 24, 8, 6, "informational", []),
        ("nsfw ai picture generator", 900, 40, 7, 15, "informational", ["sitelink"]),
        ("virtual ai girlfriend", 450, 48, 7, 12, "commercial", ["sitelink"]),
        ("ai chat character nsfw", 150, 60, 6, 7, "informational", ["sitelink"]),
        ("ai nsfw character chat", 100, 55, 6, 6, "informational", ["sitelink"]),
    ],
    "nastia.ai": [
        ("spicy ai", 131000, 1, 3227, 10, "commercial", ["sitelink"]),
        ("ai girlfriend free", 14000, 34, 1619, 3, "informational", ["sitelink", "discussion", "video_th"]),
        ("uncensored ai generator", 13000, 38, 1555, 3, "informational", []),
        ("free ai sexting", 4200, 40, 616, 2, "informational", []),
        ("free ai sex chat", 7300, 44, 444, 6, "informational", []),
        ("nsfw ai chat", 21000, 51, 425, 11, "informational", ["sitelink"]),
        ("ai sexting free", 2000, 53, 237, 3, "informational", []),
        ("ai sex bot", 6900, 24, 192, 8, "informational", []),
        ("free ai porn chat", 3500, 47, 177, 7, "informational", []),
        ("free uncensored ai generator", 2200, 55, 169, 5, "informational", ["sitelink"]),
        ("uncensored ai image generator", 4400, 47, 168, 8, "informational", ["sitelink"]),
        ("dirty ai", 3300, 12, 161, 7, "informational", ["paid_top", "paid_bottom", "paid_sitelink"]),
        ("ai sex chat free", 3100, 56, 151, 7, "informational", []),
        ("romantic ai", 3100, 51, 121, 8, "commercial", ["sitelink"]),
        ("ai girlfriend no sign up", 1000, 46, 118, 3, "informational", []),
        ("nsfw chat", 5000, 54, 100, 13, "informational", ["sitelink"]),
        ("nasty ai", 200, 29, 99, 1, "informational", ["sitelink", "question", "video_th"]),
        ("best nsfw ai chat", 2200, 24, 89, 10, "informational", ["sitelink"]),
        ("ai dirty talk", 1400, 40, 86, 6, "informational", ["paid_top"]),
        ("uncensored chat", 900, 48, 83, 4, "informational", ["sitelink", "discussion", "video_th"]),
        ("naughty ai", 2600, 0, 80, 9, "commercial", []),
        ("free ai girlfriend chat", 700, 43, 79, 3, "informational", ["sitelink"]),
        ("ai girlfriends", 4000, 37, 76, 12, "commercial", []),
        ("nude ai chat", 1000, 55, 75, 5, "informational", ["sitelink"]),
        ("ai sex roleplay", 450, 30, 69, 2, "commercial", ["sitelink"]),
        ("free sexting ai", 700, 57, 69, 4, "informational", ["sitelink"]),
        ("nsfw ai apps", 1300, 25, 63, 7, "commercial", ["sitelink"]),
        ("talk dirty ai", 1300, 8, 62, 7, "informational", []),
        ("uncensored ai generator free", 700, 40, 62, 4, "informational", ["sitelink"]),
        ("ai chat girlfriend free", 150, 49, 61, 1, "informational", ["sitelink"]),
        ("ai chat sex", 4800, 58, 60, 13, "commercial", []),
        ("dirty talk ai", 1000, 20, 53, 7, "informational", []),
        ("free uncensored ai", 1700, 34, 52, 9, "informational", []),
    ],
}

# ---- Source data: seed_modifier (matching-terms expansion) ----
SEED_MODIFIER_DATA = [
    # ai girlfriend expansion (top traffic_potential)
    ("ai girlfriend experience", 150, 39, 71000, "ai girlfriend", "informational", ["sitelink", "news", "video_th", "question"]),
    ("online girlfriend ai", 50, 55, 71000, "ai girlfriend", "commercial", []),
    ("ai chat girlfriend", 1500, 47, 71000, "ai girlfriend", "commercial", ["sitelink"]),
    ("chat with an ai girlfriend", 100, 58, 71000, "ai girlfriend", "commercial", ["sitelink", "discussion"]),
    ("ai girlfriend love simulator", 1600, 50, 69000, "ai girlfriend", "commercial", ["question", "discussion"]),
    ("free sexy ai girlfriend", 100, 60, 69000, "ai girlfriend", "informational", []),
    ("ai girlfriend chat bot", 100, 43, 69000, "ai girlfriend", "commercial", ["discussion", "news", "image_th", "question"]),
    ("ai girlfriend chat", 4900, 43, 69000, "ai girlfriend", "commercial", ["discussion"]),
    ("ai chat bot girlfriend", 150, 26, 69000, "ai girlfriend", "commercial", ["sitelink", "ai_overview", "discussion", "question", "news", "image_th"]),
    ("ai girlfriend text", 200, 34, 68000, "ai girlfriend", "commercial", ["sitelink", "news", "video_th", "image_th"]),
    ("ai girlfriend simulator", 2200, 41, 44000, "ai girlfriend", "commercial", ["ai_overview", "ai_overview_sitelink", "video_th", "image_th", "discussion", "question"]),
    ("ai chatbot girlfriend", 600, 51, 43000, "ai girlfriend", "commercial", ["ai_overview", "news", "image_th", "video_th"]),
    ("ai girlfriend games", 200, 30, 41000, "ai girlfriend", "commercial", ["discussion"]),
    ("ai girlfriend game", 1100, 34, 41000, "ai girlfriend", "commercial", ["video_th", "news", "image_th"]),
    ("fake ai girlfriend", 60, 33, 41000, "ai girlfriend", "commercial", ["sitelink", "news", "image_th", "video_th"]),
    ("virtual reality ai girlfriend", 100, 46, 39000, "ai girlfriend", "commercial", ["sitelink"]),
    ("romantic girlfriend ai chat", 70, 54, 33000, "ai girlfriend", "commercial", ["sitelink"]),
    ("romantic ai girlfriend", 200, 47, 33000, "ai girlfriend", "commercial", ["sitelink"]),
    ("ai girlfriend simulator free", 200, 49, 33000, "ai girlfriend", "informational", ["ai_overview", "ai_overview_sitelink", "image_th", "video_th", "sitelink", "discussion"]),
    ("ai sexual girlfriend", 60, 57, 33000, "ai girlfriend", "commercial", ["sitelink"]),
    ("ai girlfriend best", 100, 56, 32000, "ai girlfriend", "commercial", ["sitelink"]),
    ("ai girlfriend movie", 250, 20, 31000, "companion movie", "informational", ["ai_overview", "image_th", "question", "video_th", "sitelink", "news"]),
    ("dream girlfriend ai", 300, 49, 29000, "ai girlfriend", "commercial", ["sitelink"]),
    ("free ai girlfriend", 12000, 43, 26000, "ai girlfriend free", "informational", []),
    ("free ai girlfriend simulator", 50, 48, 26000, "ai girlfriend free", "informational", ["sitelink", "discussion", "question"]),
    ("ai girlfriend no sign up", 2000, 46, 26000, "ai girlfriend free", "informational", []),
    ("ai girlfriend free no sign up", 600, 54, 26000, "ai girlfriend free", "informational", []),
    ("free ai chat girlfriend", 200, 41, 26000, "ai girlfriend free", "informational", ["sitelink"]),
    ("free ai girlfriend chat", 900, 43, 26000, "ai girlfriend free", "informational", ["sitelink"]),
    ("ai chatbot girlfriend free", 80, 43, 26000, "ai girlfriend free", "informational", []),
    ("ai girlfriend for free", 200, 40, 26000, "ai girlfriend free", "informational", ["discussion"]),
    ("ai girlfriend free online", 150, 60, 23000, "ai girlfriend", "informational", ["question", "news"]),
    ("ai generator girlfriend", 100, 47, 23000, "ai girlfriend", "commercial", ["sitelink", "discussion", "news", "video_th", "image_th"]),
    ("free ai girlfriend generator", 1000, 55, 20000, "ai girlfriend", "informational", ["sitelink", "video_th"]),
    ("girlfriend ai chatbot", 350, 23, 20000, "ai girlfriend", "commercial", ["discussion", "question", "news", "image_th"]),
    ("best ai chatbot girlfriend", 100, 41, 20000, "ai girlfriend", "commercial", ["ai_overview", "discussion", "question"]),
    ("the best ai girlfriend app", 80, 19, 20000, "ai girlfriend", "commercial", ["ai_overview", "ai_overview_sitelink", "video_th", "image_th", "sitelink", "question"]),
    ("girlfriend chat ai", 200, 60, 19000, "ai girlfriend", "commercial", []),
    ("ai free girlfriend", 200, 24, 19000, "ai girlfriend", "commercial", []),
    ("most realistic ai girlfriend", 150, 24, 18000, "ai girlfriend", "commercial", ["ai_overview", "ai_overview_sitelink", "video_th", "sitelink", "question", "news", "image_th"]),
    ("ai girlfriend generator free", 150, 51, 18000, "ai girlfriend", "informational", ["sitelink"]),
    ("ai girlfriend creator", 350, 59, 18000, "ai girlfriend", "commercial", ["sitelink", "question"]),
    ("free ai girlfriend chatbot", 450, 58, 18000, "ai girlfriend", "informational", ["sitelink"]),
    ("ai girlfriend sexting", 350, 23, 17000, "ai sex chat", "commercial", ["sitelink"]),
    ("best girlfriend ai app", 50, 22, 16000, "ai girlfriend", "commercial", ["ai_overview", "sitelink", "question", "news", "image_th"]),
    ("ai girlfriend app free", 250, 47, 15000, "ai girlfriend", "informational", ["sitelink"]),
    ("ai girlfriend image generator", 350, 44, 15000, "ai girls", "informational", []),
    ("dream ai girlfriend", 450, 32, 15000, "ai girlfriend", "commercial", ["sitelink"]),
    ("ai girlfriend chat app", 150, 47, 15000, "ai girlfriend", "commercial", ["snippet", "sitelink"]),
    ("girlfriend ai free", 250, 24, 15000, "ai girlfriend", "informational", ["sitelink", "news", "discussion"]),
    ("free girlfriend ai", 350, 41, 12000, "ai girlfriend free", "informational", ["discussion"]),
    ("ai girlfriend generator", 1100, 44, 11000, "ai girls", "commercial", ["sitelink", "news", "video_th"]),
    # ai companion expansion (filtering out zoom, razer, class noise)
    ("nsfw ai companion", 350, 51, 64000, "spicy chat ai", "commercial", ["sitelink"]),
    ("ai companion porn", 100, 48, 14000, "ai porn", "commercial", []),
    ("ai companion free", 350, 58, 14000, "kindroid", "informational", ["ai_overview", "ai_overview_sitelink", "image_th", "question", "sitelink", "news"]),
    ("best nsfw ai companion", 150, 48, 5400, "nsfw bot", "commercial", ["sitelink"]),
    ("best ai companion apps", 250, 6, 3600, "ai companion", "commercial", ["ai_overview", "ai_overview_sitelink", "video_th", "image_th", "sitelink", "question", "discussion", "news"]),
    ("what is the best ai companion", 150, 56, 3500, "ai companion", "commercial", ["ai_overview", "ai_overview_sitelink", "image_th", "video_th", "question", "sitelink", "news"]),
    ("dream companion ai", 1500, 32, 2100, "dream companion", "commercial", ["sitelink"]),
    ("ai companion app for adults", 150, 54, 1600, "ai companion app", "commercial", ["discussion", "question", "sitelink", "news", "video_th", "image_th"]),
    ("best free ai companion app", 150, 48, 1500, "ai companion app", "informational", ["snippet", "sitelink"]),
    # nsfw ai + ai roleplay + virtual girlfriend expansion
    ("ai roleplay app", 150, 59, 350000, "character ai", "informational", ["sitelink"]),
    ("nsfw ai app", 1200, 39, 132000, "undress ai", "commercial", []),
    ("ai nsfw generator free", 150, 42, 123000, "perchance", "informational", ["sitelink"]),
    ("free ai art generator nsfw", 150, 36, 116000, "perchance", "informational", ["sitelink"]),
    ("nsfw ai image generator no login", 200, 45, 115000, "perchance", "informational", ["sitelink"]),
    ("nsfw ai generator no login", 150, 48, 115000, "perchance", "informational", ["sitelink"]),
    ("nsfw ai generator image", 100, 47, 111000, "perchance", "informational", ["sitelink"]),
    ("ai nsfw gen", 450, 47, 99000, "perchance", "informational", ["sitelink"]),
    ("image generator ai nsfw", 200, 39, 94000, "perchance", "informational", ["sitelink"]),
    ("nsfw ai photo maker", 100, 41, 94000, "perchance", "informational", []),
    ("nsfw ai pic generator", 150, 39, 94000, "perchance", "informational", ["sitelink"]),
    ("realistic ai nsfw", 100, 1, 60000, "ai porn", "informational", ["sitelink"]),
    ("chat ai nsfw", 1400, 11, 48000, "nsfw ai", "commercial", ["sitelink"]),
    ("ai chat nsfw free", 600, 16, 48000, "spicyai", "informational", ["sitelink"]),
    ("free nsfw ai writer", 100, 45, 47000, "ai writer", "informational", ["sitelink"]),
    ("ai nsfw chat", 5800, 35, 46000, "nsfw ai", "informational", []),
    ("ai nsfw chat bot", 300, 18, 46000, "nsfw ai", "informational", ["sitelink"]),
    ("ai roleplay porn", 350, 41, 46000, "ai sex chat", "informational", ["sitelink"]),
    ("ai chat nsfw", 7700, 35, 46000, "nsfw ai", "commercial", ["sitelink"]),
    ("nsfw ai chat porn", 150, 51, 46000, "ai sex chat", "commercial", ["sitelink"]),
    ("virtual ai girlfriend", 600, 48, 43000, "ai girlfriend", "commercial", ["sitelink"]),
    ("ai chat character roleplay", 100, 22, 41000, "joyland ai", "informational", ["sitelink"]),
    ("nsfw ai art generator no sign up", 300, 50, 40000, "ai art generator", "informational", []),
    ("ai chatbot nsfw", 1900, 12, 39000, "nsfw ai", "informational", []),
    ("nsfw ai free", 3300, 33, 37000, "nsfw ai", "informational", []),
    ("free nsfw ai", 8300, 34, 37000, "nsfw ai", "informational", ["sitelink"]),
    ("nsfw ai chatbot free", 600, 4, 36000, "spicyai", "informational", []),
    ("nsfw ai chat free", 2600, 33, 36000, "spicyai", "informational", ["sitelink"]),
    ("ai nsfw chat free", 600, 12, 31000, "spicyai", "informational", ["sitelink"]),
    ("nsfw ai chats", 4500, 46, 30000, "nsfw ai chat", "informational", ["sitelink"]),
    ("nsfw ai chat bot", 3400, 2, 30000, "nsfw ai chat", "commercial", []),
    ("nsfw chat ai", 11000, 47, 30000, "nsfw ai chat", "commercial", ["sitelink"]),
    ("nsfw ai chatbot", 5800, 8, 30000, "nsfw ai chat", "commercial", []),
    ("ai roleplay generator", 400, 21, 29000, "perchance ai", "informational", ["question", "discussion"]),
    ("nsfw ai gen", 2600, 1, 28000, "ai nsfw", "informational", []),
    ("nsfw ai images", 1400, 38, 28000, "ai nsfw", "informational", ["sitelink"]),
    ("ai nsfw generator", 3800, 4, 28000, "ai nsfw", "informational", []),
    ("nsfw ai", 56000, 38, 26000, "ai nsfw", "informational", ["sitelink"]),
    ("nsfw ai image", 5100, 53, 26000, "ai nsfw", "informational", []),
    ("nsfw image ai", 500, 27, 25000, "ai nsfw", "informational", ["sitelink"]),
    ("nsfw ai character generator", 100, 42, 25000, "ai nsfw", "informational", []),
]

# ---- Brand keyword pollution filter (Zoom, Razer, Class Companion are unrelated AI companion meanings) ----
EXCLUDE_SUBSTRINGS = ["zoom", "razer", "class companion", "vector robot", "vector 2.0", "candy a"]

def is_polluted(kw: str) -> bool:
    kl = kw.lower()
    return any(p in kl for p in EXCLUDE_SUBSTRINGS)

# ---- Merge ----
rows = {}  # keyword -> dict

# competitor_gap pass
for competitor, kw_list in COMPETITOR_DATA.items():
    for kw, vol, kd, traffic, pos, intent, serp in kw_list:
        if is_polluted(kw):
            continue
        if kw in rows:
            r = rows[kw]
            # take best (lowest) competitor position
            if r.get("competitor_top_position") is None or pos < r["competitor_top_position"]:
                r["competitor_top_position"] = pos
            r["competitor_domains"] = r.get("competitor_domains", set()) | {competitor}
            # track traffic_potential proxy (use sum_traffic from this competitor as upper bound)
            if r.get("competitor_traffic_max", 0) < traffic:
                r["competitor_traffic_max"] = traffic
        else:
            rows[kw] = {
                "keyword": kw,
                "volume": vol,
                "kd": kd,
                "traffic_potential": None,  # filled by seed_modifier pass if available
                "competitor_top_position": pos,
                "competitor_traffic_max": traffic,
                "competitor_domains": {competitor},
                "parent_topic": "",
                "intent": intent,
                "source": "competitor_gap",
                "serp_features": ";".join(serp) if serp else "",
            }

# seed_modifier pass - merge or insert
for kw, vol, kd, tp, parent, intent, serp in SEED_MODIFIER_DATA:
    if is_polluted(kw):
        continue
    if kw in rows:
        r = rows[kw]
        r["traffic_potential"] = tp
        r["parent_topic"] = parent
        r["source"] = "both"
        # if seed_modifier has a clearer intent, prefer it
        if not r.get("intent"):
            r["intent"] = intent
    else:
        rows[kw] = {
            "keyword": kw,
            "volume": vol,
            "kd": kd,
            "traffic_potential": tp,
            "competitor_top_position": None,
            "competitor_traffic_max": 0,
            "competitor_domains": set(),
            "parent_topic": parent,
            "intent": intent,
            "source": "seed_modifier",
            "serp_features": ";".join(serp) if serp else "",
        }

# Final estimate of traffic_potential for rows missing it: use competitor_traffic_max * 5 as a rough proxy
for kw, r in rows.items():
    if r["traffic_potential"] is None:
        r["traffic_potential"] = max(r.get("competitor_traffic_max", 0) * 5, r["volume"])

# ---- Write CSV ----
out = ROOT / "keyword-ideas.csv"
fieldnames = [
    "keyword",
    "volume",
    "kd",
    "traffic_potential",
    "competitor_top_position",
    "competitor_domains",
    "parent_topic",
    "intent",
    "source",
    "serp_features",
    # Empty placeholders for downstream layers
    "brand_fit",
    "product_fit",
    "serp_intent",
    "dr_top10_median",
    "weak_link_count",
    "bid_verdict",
    "bid_reason",
    "has_aio",
    "aio_completeness_score",
    "aio_click_intent",
    "aio_verdict",
    "aio_reasoning",
    "redteam_verdict",
    "redteam_priority_delta",
    "redteam_critique_summary",
    "priority_score",
    "notes",
]
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for kw, r in sorted(rows.items(), key=lambda x: -x[1]["traffic_potential"]):
        w.writerow({
            "keyword": r["keyword"],
            "volume": r["volume"],
            "kd": r["kd"],
            "traffic_potential": r["traffic_potential"],
            "competitor_top_position": r["competitor_top_position"] if r["competitor_top_position"] is not None else "",
            "competitor_domains": ";".join(sorted(r["competitor_domains"])) if r["competitor_domains"] else "",
            "parent_topic": r["parent_topic"],
            "intent": r["intent"],
            "source": r["source"],
            "serp_features": r["serp_features"],
            "brand_fit": "",
            "product_fit": "",
            "serp_intent": "",
            "dr_top10_median": "",
            "weak_link_count": "",
            "bid_verdict": "",
            "bid_reason": "",
            "has_aio": "",
            "aio_completeness_score": "",
            "aio_click_intent": "",
            "aio_verdict": "",
            "aio_reasoning": "",
            "redteam_verdict": "",
            "redteam_priority_delta": "",
            "redteam_critique_summary": "",
            "priority_score": "",
            "notes": "",
        })

# Summary
src_counts = {"competitor_gap": 0, "seed_modifier": 0, "both": 0, "aio_gap": 0}
for r in rows.values():
    src_counts[r["source"]] = src_counts.get(r["source"], 0) + 1
print(f"Total rows: {len(rows)}")
print(f"By source: {src_counts}")
print(f"Top 5 by traffic_potential:")
for kw, r in sorted(rows.items(), key=lambda x: -x[1]["traffic_potential"])[:5]:
    print(f"  - {r['keyword']:40s} TP={r['traffic_potential']:>7} V={r['volume']:>6} KD={r['kd']:>2} src={r['source']}")
