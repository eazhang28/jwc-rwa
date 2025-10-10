import numpy as np
import yaml
import os
import regex as re
from collections import deque

class Composer():
    '''
        Only one should exist in run time.
    '''
    def __init__(self, paragraph: str, config):
        self.offset: np.array = np.array([0,0])
        self.config = config
        self.paragraph: str= paragraph
        self._char_cache = {}
    
    def _get_chars(self):
        chars = set(list(self.paragraph))
        for c in chars:
            self._load_char_into_cache(c)

    def _load_char_into_cache(self, c:str):
        char_path = os.path.join(self.config["CHAR_DIR"], f"{c}.gcode")
        pattern = r'[a-zA-Z0-9]'
        if re.match(pattern, c):
            with open(char_path, "r") as f:
                char_gcode:str = f.read()
                self._char_cache[c] = char_gcode


    def _parse_gcode(self, c:str):
        gcode:str = self._char_cache[c]
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
        print(f"positions\n{np.array(positions) + np.array([1,2])}")


if __name__ == "__main__":
    with open("config.yaml", 'r') as file:
        config = yaml.safe_load(file)
        c = Composer("what", config)
        c._load_char_into_cache('a')
        c._parse_gcode('a')