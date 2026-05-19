from ast import List
import keyboard
import mouse
from enum import Enum

class Keyboard:
    """
    An class for verifying keyboard presses(UPDATED)
    """
    def __init__(self):
        pass

    def is_key_pressed(self, key: str) -> bool:
        return keyboard.is_pressed(key)

    def simulate_key_press(self, key: str):
        keyboard.press_and_release(key)

    def waitForKey(self, key: str):
        keyboard.wait(key)

    import keyboard

    def runOnHotkey(hotkey, callback, condition_func, args=()):
        """
        Rulează imediat când apeși tasta, dar execută callback-ul DOAR dacă condiția e True.
        """
        def wrapper():
            if condition_func():
                # Rulează funcția ta cu argumentele ei
                callback(*args) 

        # Înregistrăm wrapper-ul în tastatură
        keyboard.add_hotkey(hotkey, wrapper)

class MouseBtns(Enum):
    LEFT_BTN='left'
    RIGHT_BTN='right'
    SCROLLWHEEL='middle'


class Mouse:
    """
    [NEW] Class to use and simulate mouse clicks/movement,
    CAUTION: THIS CLASS IS QUITE RISKY.
    """
    def __init__(self):
        pass
    
    def getPos():
        mouse.get_position()
        return mouse.position()

    def isKeyClicked(key: MouseBtns) -> bool:
        return mouse.is_pressed(key.value)

    def move_from(sX: int, sY: int, eX: int, eY: int):
        mouse.move(sX, sY, eX, eY, absolute=True, duration=0)

    def move_by(mX, mY):
        mouse.move(mX, mY, False, 0)

    def scroll_by(units: int):
        mouse.scroll(units)

    def recordUntil(keyPressed: str) -> List:
        return mouse.record(keyPressed)

    def playRecording(recording: List, speed_multiplier: float):
        mouse.play(recording, speed_factor=speed_multiplier)




