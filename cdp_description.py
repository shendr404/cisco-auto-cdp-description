import re
from netmiko import ConnectHandler
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
        print(f"{COLOR_RED}Ошибка: Начальный IP-адрес больше конечного.{COLOR_RESET}")
        return []
    
    ip_list = []
    while start <= end:
        ip_list.append(str(start))
        start += 1
    
    return ip_list

def process_switch(ip_address, credentials):
    ip_address_str = str(ip_address)
    print(f"{COLOR_CYAN}Обрабатываем {ip_address_str}...{COLOR_RESET}")

    cisco_device = {
        'device_type': 'cisco_ios',
        'host': ip_address_str,
        'username': credentials['username'],
        'password': credentials['password'],
        'secret': credentials.get('secret', ''),
    }

    try:
        net_connect = ConnectHandler(**cisco_device)
        if credentials.get('secret'):
            net_connect.enable()

        cdp_output = net_connect.send_command("show cdp neighbors detail")

        device_id = None
        local_interface = None

        lines = cdp_output.splitlines()

        for line in lines:
            if "Device ID:" in line:
                device_id = line.split("Device ID:")[1].strip()
                device_id_cleaned = re.split(r'\(|\.', device_id)[0]
                device_id_cleaned = re.sub(r'[^\w-]', '', device_id_cleaned)
            
            if "Interface:" in line:
                match = re.search(r"Interface:\s+(\S+),", line)
                if match:
                    local_interface = match.group(1)

                print(f"{COLOR_YELLOW}Обнаружен интерфейс: {local_interface} для устройства {device_id_cleaned}{COLOR_RESET}")

                if device_id and local_interface:
                    commands = [
                        f"interface {local_interface}",
                        f"description (to_{device_id_cleaned})"
                    ]

                    output = net_connect.send_config_set(commands)
                    
                    print(f"{COLOR_GREEN}Отправленные команды: {commands}{COLOR_RESET}")
                    print(f"Ответ устройства:\n{output}")

                    device_id = None
                    local_interface = None

        save_output = net_connect.send_command_timing("copy running-config startup-config")
        if "Destination filename" in save_output:
            save_output += net_connect.send_command_timing("\n")

        print(f"{COLOR_GREEN}Сохранение конфигурации на {ip_address_str}:{COLOR_RESET}\n{save_output}")

        net_connect.disconnect()

        print(f"{COLOR_CYAN}Описание интерфейсов на {ip_address_str} успешно обновлено.{COLOR_RESET}")
        return True

    except ValueError as e:
        if "Failed to enter configuration mode" in str(e):
            print(f"{COLOR_RED}Ошибка: не удалось войти в конфигурационный режим на {ip_address_str}. Требуется enable пароль.{COLOR_RESET}")
            return 'enable_failed'
        print(f"{COLOR_RED}Ошибка подключения к {ip_address_str}: {e}{COLOR_RESET}")
        return False

def main():
    ip_range_input = input("Введите IP-адрес или диапазон IP-адресов (например, 192.168.0.1-192.168.0.10): ")

    if '-' in ip_range_input:
        start_ip, end_ip = ip_range_input.split('-')
        if is_valid_ip(start_ip) and is_valid_ip(end_ip):
            ip_list = generate_ip_range(start_ip, end_ip)
            if not ip_list:
                print(f"{COLOR_RED}Ошибка: Диапазон IP-адресов не может быть создан.{COLOR_RESET}")
                return
            print(f"{COLOR_CYAN}IP-диапазон валиден. Обрабатываем адреса: {ip_list}{COLOR_RESET}")
        else:
            print(f"{COLOR_RED}Ошибка: Один из введенных IP-адресов неверен.{COLOR_RESET}")
            return
    elif is_valid_ip(ip_range_input):
        ip_list = [ip_range_input]
        print(f"{COLOR_CYAN}Одиночный IP-адрес валиден: {ip_list[0]}{COLOR_RESET}")
    else:
        print(f"{COLOR_RED}Ошибка: Введенный IP-адрес неверен.{COLOR_RESET}")
        return

    credentials = {
        'username': input("Введите логин: "),
        'password': input("Введите пароль: "),
    }

    use_enable = input("Требуется ли enable пароль? (y/n): ").strip().lower()
    if use_enable == 'y':
        credentials['secret'] = input("Введите enable пароль: ")

    for ip_address in ip_list:
        result = process_switch(ip_address, credentials)
        if result == 'enable_failed':
            credentials['secret'] = input(f"{COLOR_RED}Повторите ввод enable пароля для {ip_address}: {COLOR_RESET}")
            result = process_switch(ip_address, credentials)
        while not result:
            print(f"{COLOR_RED}Ошибка аутентификации для {ip_address}. Повторите ввод учетных данных.{COLOR_RESET}")
            credentials['username'] = input("Введите логин: ")
            credentials['password'] = input("Введите пароль: ")
            if 'secret' in credentials:
                credentials['secret'] = input("Введите enable пароль: ")
            result = process_switch(ip_address, credentials)

if __name__ == "__main__":
    main()
