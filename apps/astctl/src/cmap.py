import yaml
import os
import numpy as np
import regex as re
from collections import deque


class Character:
    def __init__(self, char, config):
        self.char: str = char
        self.config = config
        self.gcode: str = self.__locate_chars(char)
        self.coords: np.array = self.__parse_gcode()

    def __locate_chars(self, c: str):
        if c.islower():
            char_path = os.path.join(self.config["CHAR_LOWER_DIR"], f"{c}.gcode")
            pattern = r"[a-z]"
            if re.match(pattern, c):
                with open(char_path, "r") as f:
                    char_gcode: str = f.read()
                    return char_gcode

            else:
                return None
        else:
            char_path = os.path.join(self.config["CHAR_DIR"], f"{c}.gcode")
            pattern = r"[A-Z0-9]"
            if re.match(pattern, c):
                with open(char_path, "r") as f:
                    char_gcode: str = f.read()
                    return char_gcode
            else:
                return None

    def __parse_gcode(self):
        gcode: str = self.gcode
        lines = gcode.split("\n")
        pattern = r"[X][-]?\d+\.?\d+\s[Y][-]?\d+\.?\d+"
        positions = []
        for l in lines:
            if res := re.search(pattern=pattern, string=l):
                pos_X, pos_Y = res.group().split(" ")
                pos_X, pos_Y = deque(pos_X), deque(pos_Y)
                pos_X.popleft()
                pos_Y.popleft()
                positions.append(
                    [float("".join(list(pos_X))), float("".join(list(pos_Y)))]
                )
        return np.array(positions)
        print(f"positions\n{np.array(positions) + np.array([1,2])}")

    def __translate(self):
        """

        Internal method translates between gcode and coordinate mappings

        """
        coords: np.array = self.coords
        pattern_x = r"[X][-]?\d+\.?\d+"
        pattern_y = r"[Y][-]?\d+\.?\d+"
        gcode = self.gcode
        lines = gcode.split("\n")
        i = 0
        j = 0
        for l in lines:
            line = l
            if re.search(pattern=pattern_x, string=l) and re.search(
                pattern=pattern_y, string=l
            ):
                i += 1
                X = f"X{coords[i - 1][0]:.2f}"
                Y = f"Y{coords[i - 1][1]:.2f}"
                l = re.sub(pattern_x, X, l)
                line = re.sub(pattern_y, Y, l)
            lines[j] = line
            j += 1
        lines = "\n".join(lines)
        self.gcode = lines

    def apply_shift(self, shift):
        """
        Applies a linear shifts to coordinates, then updates the downstream gcode file to correspond
        """
        self.coords += shift
        self.__translate()


if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
        c = Character("a", config)
        c.apply_shift(1)
        print(c.gcode)
