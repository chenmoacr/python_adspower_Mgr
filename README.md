# ADS Class

## Introduction
The ADS (Automated Device Service) class provides functionalities to interact with an ADS server, which manages browser instances for automated web browsing tasks.

## Functions

### `__init__(matrix)`
- Initializes the ADS class.
- Parameters:
  - `matrix` (str): The base URL of the ADS server.

### `start_browser(user_id, open_tabs=0, ip_tab=1, launch_args="", headless=0, disable_password_filling=0, clear_cache_after_closing=0, enable_password_saving=0)`
- Starts a browser instance.
- Parameters:
  - `user_id` (str): The ID of the user.
  - `open_tabs` (int, optional): The number of tabs to open. Defaults to 0.
  - `ip_tab` (int, optional): The index of the IP tab. Defaults to 1.
  - `launch_args` (str, optional): Additional launch arguments. Defaults to "".
  - `headless` (int, optional): Whether to start the browser in headless mode (1 for True, 0 for False). Defaults to 0.
  - `disable_password_filling` (int, optional): Whether to disable password filling (1 for True, 0 for False). Defaults to 0.
  - `clear_cache_after_closing` (int, optional): Whether to clear the cache after closing the browser (1 for True, 0 for False). Defaults to 0.
  - `enable_password_saving` (int, optional): Whether to enable password saving (1 for True, 0 for False). Defaults to 0.
- Returns:
  - tuple: A tuple containing the chrome_driver and debug_port.

### `stop_browser(user_id)`
- Stops a browser instance.
- Parameters:
  - `user_id` (str): The ID of the user.
- Returns:
  - bool: True if the operation is successful, False otherwise.

### `check_start_status(user_id)`
- Checks the status of the browser instance.
- Parameters:
  - `user_id` (str): The ID of the user.
- Returns:
  - bool: True if the browser is active, False otherwise.

### `create(name, is_proxy=False, proxy_type="", proxy_host="", proxy_port="", proxy_user="", proxy_password="", group_id="")`
- Creates a new user.
- Parameters:
  - `name` (str): The name of the user.
  - `is_proxy` (bool, optional): Whether to use a proxy. Defaults to False.
  - `proxy_type` (str, optional): The type of proxy. Defaults to "".
  - `proxy_host` (str, optional): The host of the proxy. Defaults to "".
  - `proxy_port` (str, optional): The port of the proxy. Defaults to "".
  - `proxy_user` (str, optional): The username for proxy authentication. Defaults to "".
  - `proxy_password` (str, optional): The password for proxy authentication. Defaults to "".
  - `group_id` (str, optional): The ID of the group. Defaults to "".
- Returns:
  - str: The ID of the created user.

### `get_or_create_groupid()`
- Gets or creates a group ID.
- Returns:
  - str: The group ID.

### `get_browser(browser_list)`
- Retrieves a list of browsers.
- Parameters:
  - `browser_list` (list): An empty list to store browser information.
- Returns:
  - bool: True if successful, False otherwise.

### `del_browser(user_id)`
- Deletes a browser instance.
- Parameters:
  - `user_id` (str): The ID of the user.
- Returns:
  - bool: True if successful, False otherwise.

### `get_group(group_list)`
- Retrieves a list of groups.
- Parameters:
  - `group_list` (list): An empty list to store group information.

### `get_info(user_id)`
- Retrieves information about a user.
- Parameters:
  - `user_id` (str): The ID of the user.

## Usage
1. Import the ADS class from the `ads` module.
2. Initialize an ADS object by providing the base URL of the ADS server.
3. Use the various functions provided by the ADS class to interact with the ADS server and manage browser instances.

## Example
```python
from ads import ADS

# Initialize ADS object
ads = ADS("http://local.adspower.net:50325")

# Create a new browser instance
user_id = ads.create("Browser", is_proxy=True, proxy_type="socks5", proxy_host="192.168.8.124", proxy_port="1080", proxy_user="123", proxy_password="123")

# Start the browser instance
chrome_driver, debug_port = ads.start_browser(user_id)

# Perform automated web browsing tasks

# Stop the browser instance
ads.stop_browser(user_id)

# Delete the browser instance
ads.del_browser(user_id)
