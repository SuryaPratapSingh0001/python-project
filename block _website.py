import time
from datetime import datetime as dt
import os

# Paths for different operating systems
HOSTS_PATHS = {
    'nt': r'C:\Windows\System32\drivers\etc\hosts'  # Windows
}

# Get the correct hosts file path for the current operating system
hosts_path = HOSTS_PATHS.get(os.name)

# IP address to redirect blocked websites
redirect_ip = "127.0.0.1"

# Function to read websites from a file
def read_websites(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

# Function to write websites to a file
def write_websites(file_path, websites):
    try:
        with open(file_path, 'w') as file:
            for website in websites:
                file.write(f"{website}\n")
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

# Function to check if the current time is within working hours
def is_working_hours(start_hour, end_hour):
    now = dt.now()
    start_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=end_hour, minute=0, second=0, microsecond=0)
    return start_time <= now < end_time

# Function to block websites
def block_websites(websites_to_block):
    with open(hosts_path, 'r+') as file:
        content = file.read()
        for website in websites_to_block:
            if website not in content:
                file.write(f"{redirect_ip} {website}\n")
                print(f"Blocking {website}")

# Function to unblock websites
def unblock_websites(websites_to_block):
    with open(hosts_path, 'r+') as file:
        content = file.readlines()
        file.seek(0)
        for line in content:
            if not any(website in line for website in websites_to_block):
                file.write(line)
        file.truncate()
        print("Unblocking websites")

# Function to log actions
def log_action(action):
    with open('blocker.log', 'a') as log_file:
        log_file.write(f"{dt.now()} - {action}\n")

# Function to add a website to the block list
def add_website(website, websites_to_block, file_path):
    if website not in websites_to_block:
        websites_to_block.append(website)
        write_websites(file_path, websites_to_block)
        print(f"Added {website} to block list.")
    else:
        print(f"{website} is already in the block list.")

# Main loop to periodically check and block/unblock websites
def main(start_hour=9, end_hour=17, check_interval=300):
    websites_file = 'websites.txt'
    websites_to_block = read_websites(websites_file)
    
    try:
        while True:
            user_input = input("Enter a website to block (or 'continue' to proceed): ").strip()
            if user_input.lower() == 'continue':
                break
            else:
                add_website(user_input, websites_to_block, websites_file)

        while True:
            if is_working_hours(start_hour, end_hour):
                block_websites(websites_to_block)
                log_action("Blocked websites")
            else:
                unblock_websites(websites_to_block)
                log_action("Unblocked websites")
            time.sleep(check_interval)
    except KeyboardInterrupt:
        print("Stopping website blocker")
        log_action("Stopped website blocker")
    except Exception as e:
        print(f"An error occurred: {e}")
        log_action(f"Error: {e}")

if __name__ == "__main__":
    main()
    print("Website blocker stopped")
    
    