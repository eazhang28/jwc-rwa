import numpy as np
import yaml
from cmap import Character
from collections import deque


class Composer:
    """
    Only one should exist in run time.
    """

    def __init__(self, text: str, config):
        self.config = config
        self.offset: np.array = np.array([0, 0])
        self.spacing: float = config["character_spacing"]
        self.text: str = text
        self.__char_cache = {}
        self.__get_chars()

    def __get_chars(self):
        chars = set(list(self.text))
        for c in chars:
            self.__char_cache[c] = Character(c)

    def run(self):
        """

        1. Compose the gcode
        2. Send the gcode

        """
        compiled_gcode = []
        for c in self.text:
            ch: Character = self.__char_cache[c]
            ch.apply_shift(self.offset)
            self.offset[0] += max(ch.coords[0]) + self.spacing
            # if self.offset[0] >=
            compiled_gcode.append(ch.gcode)

        # send gcode to gcode uploader


if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
        c = Composer("what", config)

