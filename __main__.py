from pynput import keyboard
from pydub import AudioSegment
from pydub.playback import play

from time import time
import subprocess

import threading


# Set your push to talk keybindings here
PUSH_TO_TALK_KEYS = [keyboard.Key.pause]

# Load audio and make it loader
activate_sound = AudioSegment.from_wav("./ptt-activate.wav") - 25
deactivate_sound = AudioSegment.from_wav("./ptt-deactivate.wav") - 25

# Microphone source id
source_id = "6"

button_status = False


def toggle_ptt(mute: bool) -> bool:
    if mute:
        command = f"pactl set-source-mute {source_id} 1"
    else:
        command = f"pactl set-source-mute {source_id} 0"

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    p.wait()

    if p.returncode == 0:
        return True
    return False


def on_press(key):
    global button_status

    if (key in PUSH_TO_TALK_KEYS) and (button_status == False):
        button_status = True
        threading.Thread(target=play, args=(activate_sound,),
                         name="press_sound").start()

        toggle_ptt(mute=False)


def on_release(key):
    global button_status

    if (key in PUSH_TO_TALK_KEYS) and (button_status == True):
        button_status = False
        threading.Thread(target=play, args=(deactivate_sound,),
                         name="release_sound").start()

        toggle_ptt(mute=True)


if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
