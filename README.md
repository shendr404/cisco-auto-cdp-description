# Сisco Auto Cdp Description

[English](#english) | [Русский](#русский)

## English

Cisco Auto Cdp Description is a script for automating the configuration of Cisco switches, allowing bulk interface description setup based on data obtained through the proprietary CDP (Cisco Discovery Protocol). The script facilitates easy management of multiple switches using IP ranges and includes a mechanism for handling authentication and privileged access errors.

### Features

- **Bulk Configuration:** Ability to configure multiple switches using an IP range.
- **Authentication:** Supports login and password with optional enable password support.
- **Error Handling:** If authentication errors or the need for an enable password occur, the script will prompt for re-entry of the necessary information.
- **Flexibility:** The script works with Cisco switches that support `show cdp neighbors detail`.
- **Color-coded Output:** Interactive and informative output using ANSI codes for event indication.

### Installation

#### Option 1: Using a Virtual Environment (venv)
1. Clone the repository:
   ```bash
   git clone https://github.com/shendr404/cisco-auto-cdp-description.git
   ```
   2. Navigate to the project directory:
   ```bash
   cd cisco-auto-cdp-description
   ```
   3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
   4. Activate the virtual environment:
      - On Windows:
      ```bash
      venv\Scripts\activate
      ```
      - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

#### Option 2: Run in the System Shell
   1. Clone the repository:
   ```bash
   git clone https://github.com/shendr404/cisco-auto-cdp-description.git
   ```
   2. Navigate to the project directory:
   ```bash
   cd CiscoAutoConfig
   ```
   3. Install the required dependencies (if needed):
   ```bash
   pip install netmiko
   ```

### Usage
   1. Run the script:
   ```bash
   python en/cdp_description.py
   ```
   2. Enter the IP address or range of IP addresses for the switches you want to configure (e.g., 192.168.0.1 or 192.168.0.1-192.168.0.10).
   3. Enter the login, password, and, if necessary, the enable password to connect to the switches.
   4. The script will automatically connect to all switches within the specified range, gather information about neighboring devices via CDP, and configure the interface descriptions.

### Error Handling
   - If any errors occur during connection or when entering configuration mode, the script will notify you and prompt for re-entry of the necessary information.
   - If an enable password was not provided at the start but is required during the script's execution, you will be prompted to enter it.

### Example Usage
   ```plaintext
   Enter the IP address or range of IP addresses (e.g., 192.168.0.1-192.168.0.10): 192.168.0.1-192.168.0.10
   Enter login: admin
   Enter password: password
   Is an enable password required? (y/n): y
   Enter enable password: enablepassword
   ```
   After entering the information, the script will sequentially connect to each switch in the range, configure the interfaces, and save the configuration.

### Requirements

   - Python 3.6+
   - `netmiko` module

### License
   This project is licensed under the GPL-3.0 License — see the [LICENSE](https://github.com/shendr404/cisco-auto-cdp-description/blob/main/LICENSE) file for details.

### Support

   If you have any questions or suggestions, you can contact the author via [GitHub Issues](https://github.com/shendr404/cisco-auto-cdp-description/issues).

Author: [shendr404](https://github.com/shendr404)


## Русский

   Сisco Auto Cdp Description — это скрипт автоматизации настройки коммутаторов Cisco, который позволяет выполнять массовую настройку описания интерфейсов на основе данных, полученных с помощью проприетарного протокола CDP (Cisco Discovery Protocol). Скрипт позволяет легко управлять большим количеством коммутаторов, используя IP-диапазоны, и включает механизм обработки ошибок аутентификации и привилегированного доступа.

### Особенности

   - **Массовая настройка**: Возможность конфигурации нескольких коммутаторов по диапазону IP-адресов.
   - **Аутентификация**: Поддержка логина и пароля с возможностью использования enable пароля.
   - **Обработка ошибок**: При возникновении ошибок аутентификации или необходимости использования enable пароля скрипт предложит повторный ввод данных.
   - **Гибкость**: Скрипт работает с коммутаторами Cisco, поддерживающими `show cdp neighbors detail`.
   - **Цветной вывод**: Интерактивный и информативный вывод с использованием ANSI-кодов для цветовой индикации событий.

### Установка

#### Вариант 1: Использование виртуального окружения (venv)
   1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/shendr404/cisco-auto-cdp-description.git
   ```
   2. Перейдите в директорию проекта:
   ```bash
   cd cisco-auto-cdp-description
   ```
   3. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   ```
   4. Активируйте виртуальное окружение:
      - На Windows:
      ```bash
      venv\Scripts\activate
      ```
      - На macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

#### Вариант 2: Запуск в системной оболочке
   1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/shendr404/cisco-auto-cdp-description.git
   ```
   2. Перейдите в директорию проекта:
   ```bash
   cd CiscoAutoConfig
   ```
   3. Установите необходимые зависимости (если требуется):
   ```bash
   pip install netmiko
   ```

### Использование
   1. Запустите скрипт:
   ```bash
   python ru/cdp_description.py
   ```
   2. Введите IP-адрес или диапазон IP-адресов коммутаторов, которые вы хотите настроить (например, 192.168.0.1 или 192.168.0.1-192.168.0.10).
   3. Введите логин, пароль, и при необходимости, enable пароль для подключения к коммутаторам.
   4. Скрипт автоматически подключится ко всем коммутаторам в указанном диапазоне, соберет информацию о соседних устройствах через CDP, и настроит описание интерфейсов.

### Обработка ошибок
   - Если на каком-либо этапе подключения или при переходе в конфигурационный режим возникнет ошибка, скрипт уведомит вас об этом и предложит повторно ввести соответствующие данные.
   - Если enable пароль не был указан при запуске, но потребовался во время работы скрипта, его также можно будет ввести при необходимости.

### Пример использования
   ```plaintext
   Введите диапазон IP-адресов (например, 192.168.0.1-192.168.0.10): 192.168.0.1-192.168.0.10
   Введите логин: admin
   Введите пароль: password
   Требуется ли enable пароль? (y/n): y
   Введите enable пароль: enablepassword
   ```
   После ввода данных скрипт последовательно подключится к каждому коммутатору в диапазоне, настроит интерфейсы и сохранит конфигурацию.

### Требования

   - Python 3.6+
   - Модуль `netmiko`

### Лицензия
   Этот проект лицензирован под лицензией GPL-3.0 - подробности см. в файле [LICENSE](https://github.com/shendr404/cisco-auto-cdp-description/blob/main/LICENSE).

### Поддержка

   Если у вас возникли вопросы или предложения, вы можете связаться с автором через [GitHub Issues](https://github.com/shendr404/cisco-auto-cdp-description/issues).

Автор: [shendr404](https://github.com/shendr404)
