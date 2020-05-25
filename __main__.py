from pynput import keyboard
from pydub import AudioSegment
from pydub.playback import play

from time import time
import subprocess


# Set your push to talk keybindings here
PUSH_TO_TALK_KEYS = [keyboard.Key.ctrl_r]

# Load audio and make it -15 dB loader
activate_sound = AudioSegment.from_mp3("./ptt-activate.mp3") - 15
deactivate_sound = AudioSegment.from_mp3("./ptt-deactivate.mp3") - 15


def toggle_ptt(mute: bool) -> bool:
    if mute:
        command = "pactl set-source-mute 1 1"
    else:
        command = "pactl set-source-mute 1 0"

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    p.wait()

    if p.returncode == 0:
        return True
    return False


def on_press(key):
    if key in PUSH_TO_TALK_KEYS:
        play(activate_sound)
        
        toggle_ptt(mute=False)


def on_release(key):
    if key in PUSH_TO_TALK_KEYS:
        play(deactivate_sound)

        toggle_ptt(mute=True)


if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
