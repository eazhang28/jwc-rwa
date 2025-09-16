import numpy as np
import yaml

class Composer():
    def __init__(self, paragraph):
        self.offset: np.array = np.array([0,0])
        self.paragraph = paragraph

    def _parse_gcode(self):
        pass
        

if __name__ == "__main__":
    with open("config.yaml", 'r') as file:
        config = yaml.safe_load(file)
    
    c = Composer("whats up")
    print(c.paragraph)
    # c.compose