import requests
import json
import threading

class ADS:
    def __init__(self, matrix):
        """
        初始化ADS类。
        
        参数:
            matrix (str): ADS服务器的基本URL。
        """
        self.matrix = matrix
        self.group_id = self.get_or_create_groupid()

    def start_browser(self, user_id, open_tabs=0, ip_tab=1, launch_args="", headless=0, disable_password_filling=0,
                      clear_cache_after_closing=0, enable_password_saving=0):
        """
        启动浏览器实例。
        
        参数:
            user_id (str): 用户ID。
            open_tabs (int, 可选): 要打开的标签页数。默认为0。
            ip_tab (int, 可选): IP标签页的索引。默认为1。
            launch_args (str, 可选): 附加的启动参数。默认为空字符串。
            headless (int, 可选): 是否以无头模式启动浏览器（1表示True，0表示False）。默认为0。
            disable_password_filling (int, 可选): 是否禁用密码填充（1表示True，0表示False）。默认为0。
            clear_cache_after_closing (int, 可选): 是否在关闭浏览器后清除缓存（1表示True，0表示False）。默认为0。
            enable_password_saving (int, 可选): 是否启用密码保存（1表示True，0表示False）。默认为0。
        
        返回:
            tuple: 包含chrome_driver和debug_port的元组。
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
        停止浏览器实例。
        
        参数:
            user_id (str): 用户ID。
        
        返回:
            bool: 如果操作成功，则为True，否则为False。
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
        检查浏览器实例的状态。
        
        参数:
            user_id (str): 用户ID。
        
        返回:
            bool: 如果浏览器处于活动状态，则为True，否则为False。
        """
        url = f"{self.matrix}/api/v1/browser/active?user_id={user_id}"
        ret = requests.get(url).text
        data = json.loads(ret)
        if data["data"]["status"] == "active":
            return True
        return False

    def create(self, name, is_proxy=False, proxy_type="", proxy_host="", proxy_port="", proxy_user="", proxy_password="", group_id=""):
        """
        创建新用户。
        
        参数:
            name (str): 用户名。
            is_proxy (bool, 可选): 是否使用代理。默认为False。
            proxy_type (str, 可选): 代理类型。默认为空字符串。
            proxy_host (str, 可选): 代理主机。默认为空字符串。
            proxy_port (str, 可选): 代理端口。默认为空字符串。
            proxy_user (str, 可选): 代理身份验证的用户名。默认为空字符串。
            proxy_password (str, 可选): 代理身份验证的密码。默认为空字符串。
            group_id (str, 可选): 组ID。默认为空字符串。
        
        返回:
            str: 创建的用户的ID。
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
        获取或创建组ID。
        
        返回:
            str: 组ID。
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
        检索浏览器列表。
        
        参数:
            browser_list (list): 用于存储浏览器信息的空列表。
        
        返回:
            bool: 如果成功，则为True，否则为False。
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
        删除浏览器实例。
        
        参数:
            user_id (str): 用户ID。
        
        返回:
            bool: 如果成功，则为True，否则为False。
        """
        # 首先停止浏览器实例
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
        检索组列表。
        
        参数:
            group_list (list): 用于存储组信息的空列表。
        """
        url = f"{self.matrix}/api/v1/group/list?page=1&page_size=2000"
        ret = requests.get(url, headers={"Content-type": "application/json"}).text
        if json.loads(ret):
            group_list.clear()
            # 根据需求补充具体逻辑实现。

    def get_info(self, user_id):
        """
        检索用户信息。
        
        参数:
            user_id (str): 用户ID。
        """
        url = f"{self.matrix}/api/v1/user/list?user_id={user_id}"
        ret = requests.get(url, headers={"Content-type": "application/json"}).text
        print(ret)
        if json.loads(ret):
            # 根据需求补充具体逻辑实现。
            pass
