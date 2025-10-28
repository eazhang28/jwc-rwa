import yaml
import os
import numpy as np
import regex as re
from collections import deque


class Character():
    def __init__ (self, char, config):
        self.char: str = char
        self.config = config
        self.gcode: str  = self.__locate_chars(char) 
        self.coords: np.array  = self.__parse_gcode(self.gcode) 

    def __locate_chars(self, c:str):
        char_path = os.path.join(self.config["CHAR_DIR"], f"{c}.gcode")
        pattern = r'[a-zA-Z0-9]'
        if re.match(pattern, c):
            with open(char_path, "r") as f:
                char_gcode:str = f.read()
                return char_gcode

    def __parse_gcode(self, c:str):
        gcode:str = self.gcode
        lines = gcode.split('\n')
        pattern = r"[X][-]?\d+\.?\d+\s[Y][-]?\d+\.?\d+"
        positions = []
        for l in lines:
            if res := re.search(pattern=pattern, string=l):
                pos_X, pos_Y = res.group().split(' ')
                pos_X, pos_Y = deque(pos_X), deque(pos_Y)
                pos_X.popleft()
                pos_Y.popleft()
                positions.append([float(''.join(list(pos_X))), float(''.join(list(pos_Y)))])
        return np.array(positions)
        print(f"positions\n{np.array(positions) + np.array([1,2])}")

    def __translate(self):
        '''
        
        Internal method translates between gcode and coordinate mappings
        
        '''
        coords: np.array = self.coords
        pattern_x = r"[X][-]?\d+\.?\d+"
        pattern_y = r"[Y][-]?\d+\.?\d+"
        gcode = self.gcode
        lines = gcode.split('\n')
        print(lines[0])
        i = 0
        for l in lines:
            print(i)
            print(len(lines))
            X = "X"+str(coords[i][0])
            Y = "Y"+str(coords[i][1])
            l = re.sub(pattern_x, X, l)
            l = re.sub(pattern_y, Y, l)
            lines[i] = l + '\n'
            i += 1

        print(lines[0])



    def apply_shift(self, shift):
        '''
        Applies a linear shifts to coordinates, then updates the downstream gcode file to correspond
        '''
        print(self.coords[0])
        self.coords += shift
        print(self.coords[0])
        self.__translate()

if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file) 
        c = Character("a", config)
        # print(c.gcode)
        c.apply_shift(1)
        # print(c.gcode)