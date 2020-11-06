from pynput import keyboard
from pydub import AudioSegment
from pydub.playback import play

from time import time
import subprocess
import os
import threading


# Set your push to talk keybindings here
PUSH_TO_TALK_KEYS = [keyboard.Key.pause]

# Load audio and make it loader
activate_sound = AudioSegment.from_wav("./ptt-activate.wav") - 25
deactivate_sound = AudioSegment.from_wav("./ptt-deactivate.wav") - 25

# Microphone source id
SOURCE_ID = "1"

MUTE_STATUS_PATH = "/tmp/mute-status"


button_status = False

if not os.path.exists(MUTE_STATUS_PATH):
    open(MUTE_STATUS_PATH, "x").close()


def write_status_file(mute: bool) -> None:
    with open(MUTE_STATUS_PATH, "w") as status_file:
        if mute:
            status_file.write("A")
        else:
            status_file.write("B")


def toggle_ptt(mute: bool) -> bool:
    write_status_file(mute)

    if mute:
        command = f"pactl set-source-mute {SOURCE_ID} 1"
    else:
        command = f"pactl set-source-mute {SOURCE_ID} 0"

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    p.wait()

    if p.returncode == 0:
        return True
    return False


def on_press(key):
    global button_status

    if (key in PUSH_TO_TALK_KEYS) and (button_status == False):
        button_status = True
        # threading.Thread(target=play, args=(activate_sound,), name="press_sound").start()

        toggle_ptt(mute=False)


def on_release(key):
    global button_status

    if (key in PUSH_TO_TALK_KEYS) and (button_status == True):
        button_status = False
        # threading.Thread(target=play, args=(deactivate_sound,), name="release_sound").start()

        toggle_ptt(mute=True)


if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
