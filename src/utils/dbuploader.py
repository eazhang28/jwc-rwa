import sqlite3
import os

font = "default"
font_path = "fonts/" + font + "/"
font_path_lower = font_path + "Lower_case"

conn = sqlite3.connect("fontdch.db")
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS FCLOOKUP (
        font TEXT,
        char TEXT,
        data BLOB,
        PRIMARY KEY (font, char)
    )
    """
)

for case in (font_path, font_path_lower):
    for filename in os.listdir(case):
        file_path = os.path.join(case, filename)
        try:
            with open(file_path, "rb") as f:
                blob = f.read()
                cur.execute(
                    "INSERT INTO FCLOOKUP (font,char,data) VALUES(?,?,?)",
                    ("default", filename.split(".", 1)[0], blob),
                )

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            continue

conn.commit()
conn.close()
