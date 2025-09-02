import serial
import time

# Replace with your actual serial port and baud rate
port = 'COM7'  # Adjust for your system
baud_rate = 115200

# Open the serial connection
try:
    s = serial.Serial(port, baud_rate, timeout=1)
    print(f"Connected to {port} at {baud_rate} baud rate.")
except:
    print(f"Failed to connect to {port}. Please check your connection and port.")
    exit()

# Wait for the microcontroller to wake up
time.sleep(2)  # Give it a moment to respond
s.write(b"\r\n\r\n")  # Wake up signal (common for GRBL controllers)
time.sleep(1)  # Wait for the device to process the wake-up signal

# Read initial response (optional)
response = s.readline()
print(f"Response: {response.decode('utf-8')}")

# Function to send a command and print the response
def send_command(command):
    print(f"Sending: {command}")
    s.write((command + '\n').encode())  # Send command to the DrawBot
    response = s.readline()  # Read response from DrawBot
    print(f"Response: {response.decode('utf-8')}")

# Now, you can send manual G-code commands:
while True:
    command = input("Enter G-code command (or type 'exit' to quit): ")
    if command.lower() == 'exit':
        break
    else:
        send_command(command)

# Close the serial connection when done
s.close()
