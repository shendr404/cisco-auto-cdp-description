import re
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException
from ipaddress import ip_address

# ANSI-коды для цвета
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_RESET = "\033[0m"

def is_valid_ip(ip):
    try:
        ip_address(ip)
        return True
    except ValueError:
        return False

def generate_ip_range(start_ip, end_ip):
    start = ip_address(start_ip)
    end = ip_address(end_ip)
    
    if start > end:
        print(f"{COLOR_RED}Error: The starting IP address is greater than the ending IP address.{COLOR_RESET}")
        return []
    
    ip_list = []
    while start <= end:
        ip_list.append(str(start))
        start += 1
    
    return ip_list

def process_switch(ip_address, credentials):
    ip_address_str = str(ip_address)
    print(f"{COLOR_CYAN}Processing {ip_address_str}...{COLOR_RESET}")

    cisco_device = {
        'device_type': 'cisco_ios',
        'host': ip_address_str,
        'username': credentials['username'],
        'password': credentials['password'],
        'secret': credentials.get('secret', ''),
        'timeout': 10,
    }

    try:
        net_connect = ConnectHandler(**cisco_device)
        if credentials.get('secret'):
            net_connect.enable()

        cdp_output = net_connect.send_command("show cdp neighbors detail")

        device_id = None
        local_interface = None

        for line in cdp_output.splitlines():
            if "Device ID:" in line:
                device_id = re.split(r'\(|\.', line.split("Device ID:")[1].strip())[0]
                device_id = re.sub(r'[^\w-]', '', device_id)

            if "Interface:" in line:
                match = re.search(r"Interface:\s+(\S+),", line)
                if match:
                    local_interface = match.group(1)
                    print(f"{COLOR_YELLOW}Interface discovered: {local_interface} to the device {device_id}{COLOR_RESET}")

                    if device_id and local_interface:
                        commands = [
                            f"interface {local_interface}",
                            f"description (to_{device_id})"
                        ]

                        output = net_connect.send_config_set(commands)
                        print(f"{COLOR_GREEN}Sent commands: {commands}{COLOR_RESET}")
                        print(f"Device response:\n{output}")

                    device_id = None
                    local_interface = None

        save_output = net_connect.send_command_timing("copy running-config startup-config")
        if "Destination filename" in save_output:
            save_output += net_connect.send_command_timing("\n")

        print(f"{COLOR_GREEN}Saving configuration on {ip_address_str}:{COLOR_RESET}\n{save_output}")

        net_connect.disconnect()

        print(f"{COLOR_CYAN}Interface descriptions on {ip_address_str} have been successfully updated.{COLOR_RESET}")
        return True

    except NetmikoAuthenticationException:
        print(f"{COLOR_RED}Authentication error for {ip_address_str}.{COLOR_RESET}")
        return False
    except NetmikoTimeoutException:
        print(f"{COLOR_RED}Host {ip_address_str} is unavailable. Skipping.{COLOR_RESET}")
        return True
    except ValueError as e:
        if "Failed to enter configuration mode" in str(e):
            print(f"{COLOR_RED}Error: Failed to enter configuration mode on {ip_address_str}. Enable password is required.{COLOR_RESET}")
            return 'enable_failed'
        print(f"{COLOR_RED}Connection error to {ip_address_str}: {e}{COLOR_RESET}")
        return False


def main():
    ip_range_input = input("Enter the IP address or range of IP addresses (e.g., 192.168.0.1-192.168.0.10): ")

    if '-' in ip_range_input:
        start_ip, end_ip = ip_range_input.split('-')
        if is_valid_ip(start_ip) and is_valid_ip(end_ip):
            ip_list = generate_ip_range(start_ip, end_ip)
            if not ip_list:
                print(f"{COLOR_RED}Error: The IP range could not be created.{COLOR_RESET}")
                return
            print(f"{COLOR_CYAN}IP range is valid. Processing addresses: {ip_list}{COLOR_RESET}")
        else:
            print(f"{COLOR_RED}Error: One of the entered IP addresses is invalid.{COLOR_RESET}")
            return
    elif is_valid_ip(ip_range_input):
        ip_list = [ip_range_input]
        print(f"{COLOR_CYAN}Single IP address is valid: {ip_list[0]}{COLOR_RESET}")
    else:
        print(f"{COLOR_RED}Error: The entered IP address is invalid.{COLOR_RESET}")
        return

    credentials = {
        'username': input("Enter login: "),
        'password': input("Enter password: "),
    }

    use_enable = input("Is an enable password required? (y/n): ").strip().lower()
    if use_enable == 'y':
        credentials['secret'] = input("Enter enable password: ")

    for ip in ip_list:
        result = process_switch(ip, credentials)
        if result == 'enable_failed':
            credentials['secret'] = input(f"{COLOR_RED}Please re-enter the enable password for {ip}: {COLOR_RESET}")
            result = process_switch(ip, credentials)
        elif not result:
            print(f"{COLOR_RED}Please re-enter your credentials.{COLOR_RESET}")
            credentials['username'] = input("Enter login: ")
            credentials['password'] = input("Enter password: ")
            if 'secret' in credentials:
                credentials['secret'] = input("Enter enable password: ")
            result = process_switch(ip, credentials)

if __name__ == "__main__":
    main()
