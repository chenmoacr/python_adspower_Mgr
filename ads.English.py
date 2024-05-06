import requests
import json
import threading

class ADS:
    def __init__(self, matrix):
        """
        Initializes the ADS class.
        
        Args:
            matrix (str): The base URL of the ADS server.
        """
        self.matrix = matrix
        self.group_id = self.get_or_create_groupid()

    def start_browser(self, user_id, open_tabs=0, ip_tab=1, launch_args="", headless=0, disable_password_filling=0,
                      clear_cache_after_closing=0, enable_password_saving=0):
        """
        Starts a browser instance.
        
        Args:
            user_id (str): The ID of the user.
            open_tabs (int, optional): The number of tabs to open. Defaults to 0.
            ip_tab (int, optional): The index of the IP tab. Defaults to 1.
            launch_args (str, optional): Additional launch arguments. Defaults to "".
            headless (int, optional): Whether to start the browser in headless mode (1 for True, 0 for False). Defaults to 0.
            disable_password_filling (int, optional): Whether to disable password filling (1 for True, 0 for False). Defaults to 0.
            clear_cache_after_closing (int, optional): Whether to clear the cache after closing the browser (1 for True, 0 for False). Defaults to 0.
            enable_password_saving (int, optional): Whether to enable password saving (1 for True, 0 for False). Defaults to 0.
        
        Returns:
            tuple: A tuple containing the chrome_driver and debug_port.
        """
        url = f"{self.matrix}/api/v1/browser/start?user_id={user_id}"
        if open_tabs == 1:
            url += f"&open_tabs={open_tabs}"
        if ip_tab is not None:
            url += f"&ip_tab={ip_tab}"
        if launch_args != "":
            url += f"&launch_args={launch_args}"
        if headless == 1:
            url += f"&headless={headless}"
        if disable_password_filling == 1:
            url += f"&disable_password_filling={disable_password_filling}"
        if clear_cache_after_closing == 1:
            url += f"&clear_cache_after_closing={clear_cache_after_closing}"
        if enable_password_saving == 1:
            url += f"&enable_password_saving={enable_password_saving}"

        ret = requests.get(url).json()
        print(ret)
        if ret["code"] == 0:
            chrome_driver = ret["data"]["webdriver"]
            debug_port = ret["data"]["ws"]["selenium"]
            return chrome_driver, debug_port
        return "", ""

    def stop_browser(self, user_id):
        """
        Stops a browser instance.
        
        Args:
            user_id (str): The ID of the user.
        
        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        url = f"{self.matrix}/api/v1/browser/stop?user_id={user_id}"
        response = requests.get(url)
        data = response.json()

        if data["code"] == 0 and data["msg"] == "success":
            return True
        else:
            print(f"停止浏览器实例失败: {data}")
            return False

    def check_start_status(self, user_id):
        """
        Checks the status of the browser instance.
        
        Args:
            user_id (str): The ID of the user.
        
        Returns:
            bool: True if the browser is active, False otherwise.
        """
        url = f"{self.matrix}/api/v1/browser/active?user_id={user_id}"
        ret = requests.get(url).text
        data = json.loads(ret)
        if data["data"]["status"] == "active":
            return True
        return False

    def create(self, name, is_proxy=False, proxy_type="", proxy_host="", proxy_port="", proxy_user="", proxy_password="", group_id=""):
        """
        Creates a new user.
        
        Args:
            name (str): The name of the user.
            is_proxy (bool, optional): Whether to use a proxy. Defaults to False.
            proxy_type (str, optional): The type of proxy. Defaults to "".
            proxy_host (str, optional): The host of the proxy. Defaults to "".
            proxy_port (str, optional): The port of the proxy. Defaults to "".
            proxy_user (str, optional): The username for proxy authentication. Defaults to "".
            proxy_password (str, optional): The password for proxy authentication. Defaults to "".
            group_id (str, optional): The ID of the group. Defaults to "".
        
        Returns:
            str: The ID of the created user.
        """
        url = f"{self.matrix}/api/v1/user/create"
        payload = {
            "name": name,
            "group_id": group_id if group_id else self.group_id,
            "fingerprint_config": {
                "webrtc": "proxy"
            }
        }

        if is_proxy:
            payload["user_proxy_config"] = {
                "proxy_soft": "other",
                "proxy_type": proxy_type,
                "proxy_host": proxy_host,
                "proxy_port": int(proxy_port),
                "proxy_user": proxy_user, 
                "proxy_password": proxy_password
            }
        else:
            payload["user_proxy_config"] = {
                "proxy_soft": "no_proxy"
            }

        lock = threading.Lock()
        lock.acquire()
        ret = requests.post(url, json=payload, headers={"Content-type": "application/json"}, timeout=60).text 
        lock.release()
        
        print(ret)
        data = json.loads(ret)

        if data["msg"] == "Success":
            print(f"创建浏览器成功,初始数据{ret}")
            print(data["data"]["id"])
            return data["data"]["id"]
        
        print(f"创建失败:{ret}")
        return ""

    def get_or_create_groupid(self):
        """
        Gets or creates a group ID.
        
        Returns:
            str: The group ID.
        """
        url = f"{self.matrix}/api/v1/group/list"
        ret = requests.get(url).text
        data = json.loads(ret)
        if data["code"] == 0 and len(data["data"]["list"]) > 0:
            return data["data"]["list"][0]["group_id"]
        else:
            url = f"{self.matrix}/api/v1/group/create"
            payload = {
                "group_name": "default_group"
            }
            ret = requests.post(url, json=payload, headers={"Content-type": "application/json"}).text
            data = json.loads(ret)
            if data["code"] == 0:
                return data["data"]["group_id"]
        return ""

    def get_browser(self, browser_list):
        """
        Retrieves a list of browsers.
        
        Args:
            browser_list (list): An empty list to store browser information.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        url = f"{self.matrix}/api/v1/user/list?page=1&page_size=100"
        ret = requests.get(url).text
        browser_list.clear()

        if json.loads(ret):
            data = json.loads(ret)["data"]["list"]
            for i in range(len(data)):
                browser_info = {
                    "id": data[i]["user_id"],
                    "name": data[i]["name"],
                    "user": data[i]["username"]
                }
                browser_list.append(browser_info)
            return True
        return False

    def del_browser(self, user_id):
        """
        Deletes a browser instance.
        
        Args:
            user_id (str): The ID of the user.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        # First stop the browser instance
        self.stop_browser(user_id)
        
        url = f"{self.matrix}/api/v1/user/delete"
        payload = {
            "user_ids": [user_id]
        }
        lock = threading.Lock()
        lock.acquire()
        ret = requests.post(url, json=payload, headers={"Content-type": "application/json"}).text
        lock.release()

        if json.loads(ret):
            data = json.loads(ret)
            if data["msg"] == "Success":
                return True

        print(f"删除失败:{ret}")
        return False

    def get_group(self, group_list):
        """
        Retrieves a list of groups.
        
        Args:
            group_list (list): An empty list to store group information.
        """
        url = f"{self.matrix}/api/v1/group/list?page=1&page_size=2000"
        ret = requests.get(url, headers={"Content-type": "application/json"}).text
        if json.loads(ret):
            group_list.clear()
            # Specific logic implementation is needed here based on requirements.

    def get_info(self, user_id):
        """
        Retrieves information about a user.
        
        Args:
            user_id (str): The ID of the user.
        """
        url = f"{self.matrix}/api/v1/user/list?user_id={user_id}"
        ret = requests.get(url, headers={"Content-type": "application/json"}).text
        print(ret)
        if json.loads(ret):
            # Specific logic implementation is needed here based on requirements.
            pass
