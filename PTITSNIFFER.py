import socket
import subprocess
import sys
from datetime import datetime
import threading

# Clear the screen (works on Unix-like systems)
subprocess.call('clear', shell=True)

# Ask for input
remote_server = input("Vui lòng nhập remote host: ")
try:
    remote_server_ip = socket.gethostbyname(remote_server)
except socket.gaierror:
    print("Không thể phân giải hostname. Đang thoát...")
    sys.exit()

print("_" * 60)
print(f">>>>> Đang quét các cổng khả dụng trên {remote_server} ({remote_server_ip}) >>>>>>")
print("_" * 60)

# Record start time
start_time = datetime.now()

# Define a function to scan each port
def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)  # Set a timeout for faster scanning
    result = sock.connect_ex((remote_server_ip, port))
    if result == 0:
        print(f"Port {port}:      Open")
    sock.close()

# Create a list of threads
threads = []

try:
    # Create and start a thread for each port in the range
    for port in range(1, 5001):
        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

except KeyboardInterrupt:
    print("\nBạn đã thoát chương trình.")
    sys.exit()

except socket.error:
    print("\nKhông thể kết nối tới server. Đang thoát...")
    sys.exit()

# Record end time
end_time = datetime.now()
total_time = end_time - start_time

print("_" * 60)
print(f"Quét hoàn thành! Thời gian thực hiện: {total_time}")
print("_" * 60)
