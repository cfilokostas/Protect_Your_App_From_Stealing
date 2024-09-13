import psutil
import subprocess
import hashlib

# Function to get the first disk serial number on Windows
def get_first_disk_serial_windows():
    try:
        command = "wmic diskdrive get serialnumber"
        result = subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
        output = result.stdout
        # Filter and clean up the output
        serial_numbers = [line.strip() for line in output.splitlines() if line.strip() and not line.startswith("SerialNumber")]
        
        # Return the first serial number if available
        if serial_numbers:
            return serial_numbers[0]
        else:
            return 0
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the command: {e}")
        return 0

#hashing function for mac and serial
def hash_function(mac_address):
    if mac_address !=0:
        # Normalize MAC address (e.g., remove colons or dashes)
        mac_address = mac_address.lower().replace(":", "").replace("-", "")

        # Create a SHA-256 hash object
        hash_object = hashlib.sha256()

        # Update the hash object with the MAC address encoded to bytes
        hash_object.update(mac_address.encode())

        # Get the hexadecimal representation of the hash
        hashed_mac_address = hash_object.hexdigest()

        return hashed_mac_address
    
# Get network interface details
net_if_addrs = psutil.net_if_addrs()

# Initialize variables to store MAC addresses
ethernet_mac_address = 0
wifi_mac_address = 0

# Look for the Ethernet adapter
ethernet_interface = "Ethernet"  # You may need to modify this name depending on your system
if ethernet_interface in net_if_addrs:
    for addr in net_if_addrs[ethernet_interface]:
        if addr.family == psutil.AF_LINK:  # AF_LINK is used for MAC addresses
            ethernet_mac_address = addr.address
            break

# Look for the Wi-Fi adapter
wifi_interface = "Wi-Fi"  # Change if your system uses a different name
if wifi_interface in net_if_addrs:
    for addr in net_if_addrs[wifi_interface]:
        if addr.family == psutil.AF_LINK:  # AF_LINK is used for MAC addresses
            wifi_mac_address = addr.address
            break

# Get the first disk serial number
first_disk_serial = get_first_disk_serial_windows()

#hasing the values from the macs and serial
hased_ethernet_mac_address=hash_function(ethernet_mac_address)
hased_wifi_mac_address=hash_function(wifi_mac_address)
hashed_first_disk_serial = hash_function(first_disk_serial)

# Define file path
file_path = "C:/Configuration.txt"

# Write the results to a file
def write_info_to_file(file_path, hased_ethernet_mac, hased_wifi_mac, hased_disk_serial):
    try:
        with open(file_path, 'w') as file:
            file.write(f"{hased_ethernet_mac if hased_ethernet_mac else 'None'}\n")
            file.write(f"{hased_wifi_mac if hased_wifi_mac else 'None'}\n")
            file.write(f"{hased_disk_serial if hased_disk_serial else 'None'}")
        print(f"Information written to {file_path}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

# Write the collected information to the file
write_info_to_file(file_path, hased_ethernet_mac_address, hased_wifi_mac_address, hashed_first_disk_serial)
