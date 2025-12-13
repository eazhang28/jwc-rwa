import numpy as np
import yaml
from cmap import Character


class Composer:
    """
    Only one should exist in run time.
    """

    def __init__(self, text: str, config):
        self.config = config
        self.offset: np.array = np.array([0, 0])
        self.spacing: float = config["SPACE_OFFSET"]
        self.white_space: float = config["WHITE_SPACE"]
        self.text: str = text
        self.__char_cache = dict()

    def __get_chars(self):
        chars = set(list(self.text))
        for c in chars:
            self.__char_cache[c] = Character(c, self.config)

    def run(self):
        """

        1. Compose the gcode
        2. Send the gcode

        """
        self.__get_chars()
        compiled_gcode = []
        for c in self.text:
            ch: Character = self.__char_cache[c]
            ch.apply_shift(self.offset)
            self.offset[0] += max(ch.coords[0]) + self.spacing
            # if self.offset[0] >=
            compiled_gcode.append(ch.gcode)
        print(len(compiled_gcode))
        # send gcode to gcode uploader
        # upload_gcode()
        #
        with open("example.gcode", "w") as file:
            for g in compiled_gcode:
                file.write(g)
                file.write("\n")


if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
        c = Composer("whataballgamehehe", config)
        c.run()
