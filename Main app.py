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

#initialize validation variables
ethernet_valid=False
wifi_valid=False
disk_serial_valid=False
activation=False #variable that will define if the app will run or not

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
hased_first_disk_serial = hash_function(first_disk_serial)


# Define file path
file_path = "C:/Configuration.txt"

#open configuration file and check if the lines match
try:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Ensure there are exactly three lines
    if len(lines) != 3:
        raise ValueError("The file should contain exactly three lines.")

    # Strip newline characters from each line
    line1 = lines[0].strip()
    line2 = lines[1].strip()
    line3 = lines[2].strip()

    # Compare lines with the variables and print the corresponding result
    if line1 == hased_ethernet_mac_address:
        ethernet_valid=True
    if line2 == hased_wifi_mac_address:
        wifi_valid=True
    if line3 == hased_first_disk_serial:
        disk_serial_valid=True

except FileNotFoundError:
    print(f"Error: The file at {file_path} does not exist.")
except ValueError as ve:
    print(f"Error: {ve}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")




# check for at least one way to validate
if ethernet_valid:
    activation = True
elif wifi_valid:
    activation = True
elif disk_serial_valid:
    activation = True
else:
    print("not valid")

if activation==True:
    print("valid")
    #app code here



