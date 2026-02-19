import sqlite3
import sys
from pathlib import Path

for x in Path("./fonts/default/").iterdir():
    if x.is_file():
        with open(x, "rb") as f:
            print(str(x.read_bytes()))
