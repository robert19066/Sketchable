import pynput # type: ignore

class Keyboard:
    """
    A class for listening keyboard input.
    """
    def __init__(self, asyncmode: bool = True):
        self.keyboard = pynput.keyboard.Controller()
        self.asyncmode = asyncmode
        self.listener = None
        
        # stores current key states
        self.key_states = {}

        if self.asyncmode:
            self.listener = pynput.keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )

    def on_press(self, key):
        self.key_states[key] = True

    def on_release(self, key):
        self.key_states[key] = False

    def is_pressed(self, key):
        return self.key_states.get(key, False)

    def start_listening(self):
        if self.asyncmode and self.listener:
            self.listener.start()
        else:
            raise ValueError(
                "you can't start listening in normal mode. "
                "set asyncmode=True"
            )

    def stop_listening(self):
        if self.listener:
            self.listener.stop()