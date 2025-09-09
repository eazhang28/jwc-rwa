import argparse 
import os 
import sys 
import time 
import serial 
from tqdm import tqdm 

def main(): 

    predefined_filename = "C:\\Users\\patel\\OneDrive\\Desktop\\abcfinale.gcode"  # Default G-code file 
    parser = argparse.ArgumentParser( 
        prog="pyGcodeSender", 
        description="A simple Python script to send G-code over serial." 
    ) 
    parser.add_argument("filename", nargs="?", default=predefined_filename, help="Path to G-code file") 
    parser.add_argument("-p", "--port", help="Serial port name (e.g., COM7 or /dev/ttyUSB0)") 
    parser.add_argument("-b", "--baudrate", default=115200, type=int, help="Baud rate (default: 115200)") 
    args = parser.parse_args() 
    
    # === Validate the filename === 

    file_path = os.path.abspath(args.filename) 

    if not (os.path.isfile(file_path) and file_path.lower().endswith(".gcode")): 
        print(f"❌ Invalid G-code file: {file_path}") 
        print("Make sure the file exists, ends with .gcode, and is not hidden or renamed by mistake.") 
        sys.exit() 
    
    # Hardcoded port 
    port = "COM5" 
    print("=" * 60) 
    print("🛠️  G-code Sender") 
    print(f"📄 File: {file_path}\n🔌 Port: {port}\n📡 Baudrate: {args.baudrate}") 
    print("=" * 60) 
    if input("Continue? [y/n] ").strip().lower() != 'y': 

        sys.exit() 
    
    # === Read G-code lines === 
    try: 
        with open(file_path, 'r') as f: 
            codes = f.readlines() 
        print(f"✅ Loaded G-code file with {len(codes)} lines.") 
    except Exception as e: 
        print(f"❌ Error reading file: {e}") 
        sys.exit() 

    # === Open serial connection === 

    print(f"🔗 Connecting to {port}...") 

    try: 
        s = serial.Serial(port, args.baudrate, timeout=2) 
        time.sleep(2)  # Allow time for GRBL to initialize 
        s.write(b"\r\n\r\n")  # Wake up GRBL 
        time.sleep(2) 
        s.reset_input_buffer() 

        # Print any startup messages from GRBL 
        while s.in_waiting: 
            print(s.readline().decode().strip()) 
        print("✅ Connected and ready.") 
    except Exception as e: 
        print(f"❌ Failed to open serial port: {e}") 
        sys.exit() 

    # === Send G-code === 

    print("📤 Sending G-code...") 
    for code in tqdm(codes, unit=" lines"): 
        clean = code.strip() 
        if clean and not clean.startswith(';'): 
            s.write((clean + '\n').encode()) 
            time.sleep(0.1)  # Delay to give GRBL time to process 
    s.close() 
    print("✅ G-code transmission complete.") 
    print("=" * 60) 

if __name__ == "__main__": 
    main() 