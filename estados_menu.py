# estados_menu.py

# from enum import Enum
#
# class MenuState(Enum):
#     MAIN = "main"
#     OPTIONS = "options"
#     VIDEO_SETTINGS = "video_settings"
#     AUDIO_SETTINGS = "audio_settings"
#     KEYS_SETTINGS = "keys_settings"

from enum import Enum, auto


class MenuState(Enum):
    MAIN = auto()
    OPTIONS = auto()
    VIDEO_SETTINGS = auto()
    AUDIO_SETTINGS = auto()
    KEYS_SETTINGS = auto()
