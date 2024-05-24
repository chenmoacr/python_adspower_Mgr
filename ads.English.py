import requests
import json
import threading
import time

class ADS:
    def __init__(self, matrix):
        """
        初始化 ADS 类。

        Args:
            matrix (str): 矩阵 API 的 URL。
        """
        self.matrix = matrix
        self.lock = threading.Lock()  # 创建一个互斥锁
        self.group_id = self.get_or_create_groupid()

    def start_browser(self, user_id, open_tabs=0, ip_tab=1, new_first_tab=0, launch_args="", headless=0, disable_password_filling=0,
                    clear_cache_after_closing=0, enable_password_saving=0):
        """
        启动一个新的浏览器实例。

        Args:
            user_id (str): 浏览器用户的 ID。
            open_tabs (int, optional): 是否打开平台和历史页面,0 表示打开(默认),1 表示不打开。默认为 0。
            ip_tab (int, optional): 是否打开 IP 检测页,0 表示不打开,1 表示打开(默认)。默认为 1。
            new_first_tab (int, optional): 是否使用新版 IP 检测页,1 表示新版,0 表示旧版(默认)。默认为 0。
            launch_args (str, optional): 启动浏览器时传递的额外参数。默认为空字符串。
            headless (int, optional): 是否以无头模式启动浏览器,0 表示不启用(默认),1 表示启用。默认为 0。
            disable_password_filling (int, optional): 是否禁用密码自动填充功能,0 表示不禁用(默认),1 表示禁用。默认为 0。
            clear_cache_after_closing (int, optional): 是否在关闭浏览器后清除缓存,0 表示不清除(默认),1 表示清除。默认为 0。
            enable_password_saving (int, optional): 是否允许保存密码,0 表示不允许(默认),1 表示允许。默认为 0。

        Returns:
            tuple: 包含 WebDriver 路径和调试端口号的元组。如果启动失败,则返回 (None, None)。
        """
        with self.lock:
            for attempt in range(5):  # 重复启动五次
                time.sleep(3)  # 每次互斥 sleep 时间更改为 3 秒
                url = f"{self.matrix}/api/v1/browser/start?user_id={user_id}"
                if open_tabs == 1:
                    url += f"&open_tabs={open_tabs}"
                if ip_tab is not None:
                    url += f"&ip_tab={ip_tab}"
                if new_first_tab == 1:
                    url += f"&new_first_tab={new_first_tab}"
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

                try:
                    response = requests.get(url)
                    data = response.json()
                    print(data)

                    if data["code"] == 0:
                        webdriver = data["data"]["webdriver"]
                        debug_port = data["data"]["ws"]["selenium"]
                        return webdriver, debug_port
                    else:
                        print(f"第 {attempt+1} 次启动浏览器实例失败: {data['msg']}")
                except requests.exceptions.RequestException as e:
                    print(f"第 {attempt+1} 次启动浏览器实例时发生请求异常: {e}")

                time.sleep(3)  # 启动失败后等待 3 秒再重试

            print("启动浏览器实例失败,已尝试 5 次")
            return None, None

    def stop_browser(self, user_id):
        """
        停止指定用户 ID 的浏览器实例。

        Args:
            user_id (str): 浏览器用户的 ID。

        Returns:
            bool: 如果停止成功,返回 True,否则返回 False。
        """
        with self.lock:
            for attempt in range(5):  # 增加重试次数到 5 次
                time.sleep(3)  # 增加等待时间到 3 秒
                url = f"{self.matrix}/api/v1/browser/stop?user_id={user_id}"
                try:
                    response = requests.get(url)
                    data = response.json()
                    
                    if data["code"] == 0:
                        print(f"浏览器实例 {user_id} 停止成功")
                        return True
                    else:
                        print(f"第 {attempt+1} 次停止浏览器实例 {user_id} 失败: {data['msg']}")
                except requests.exceptions.RequestException as e:
                    print(f"第 {attempt+1} 次停止浏览器实例 {user_id} 时发生请求异常: {e}")

                time.sleep(3)  # 停止失败后等待 3 秒再重试

            print(f"停止浏览器实例 {user_id} 失败,已尝试 5 次")
            return False

    def check_start_status(self, user_id):
        """
        检查指定用户 ID 的浏览器实例是否处于活动状态。

        Args:
            user_id (str): 浏览器用户的 ID。

        Returns:
            bool: 如果浏览器实例处于活动状态,返回 True,否则返回 False。
        """
        with self.lock:
            for attempt in range(5):  # 循环检查五次
                time.sleep(3)  # 延时3秒
                url = f"{self.matrix}/api/v1/browser/active?user_id={user_id}"
                try:
                    response = requests.get(url)
                    data = response.json()

                    if data["code"] == 0 and data["data"]["status"] == "Active":
                        return True
                    else:
                        print(f"第 {attempt+1} 次检查,浏览器实例未处于活动状态")
                except requests.exceptions.RequestException as e:
                    print(f"第 {attempt+1} 次检查,发生请求异常: {e}")

            return False

    def create(self, name, is_proxy=False, proxy_type="", proxy_host="", proxy_port="", proxy_user="", proxy_password="", group_id="", cookies=None):
        """
        创建一个新的浏览器用户。

        Args:
            name (str): 浏览器用户的名称。
            is_proxy (bool, optional): 是否使用代理。默认为 False。
            proxy_type (str, optional): 代理类型。默认为空字符串。
            proxy_host (str, optional): 代理主机。默认为空字符串。
            proxy_port (str, optional): 代理端口。默认为空字符串。
            proxy_user (str, optional): 代理用户名。默认为空字符串。
            proxy_password (str, optional): 代理密码。默认为空字符串。
            group_id (str, optional): 组 ID。默认为空字符串。
            cookies (str, optional): Cookie 字符串。默认为 None。

        Returns:
            str: 新创建的浏览器用户的 ID,如果创建失败则返回空字符串。
        """
        with self.lock:
            for attempt in range(5):  # 重复创建五次
                time.sleep(3)  # 每次互斥 sleep 时间更改为 3 秒
                url = f"{self.matrix}/api/v1/user/create"
                payload = {
                    "name": name,
                    "group_id": group_id if group_id else self.group_id,
                    "fingerprint_config": {
                        "webrtc": "proxy"
                    }
                }

                if cookies:
                    payload["cookie"] = cookies

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

                ret = requests.post(url, json=payload, headers={"Content-type": "application/json"}, timeout=60).text
                print(ret)
                data = json.loads(ret)

                if data["msg"] == "Success":
                    print(f"创建浏览器成功,初始数据{ret}")
                    print(data["data"]["id"])
                    return data["data"]["id"]

                print(f"创建失败:{ret}")
                time.sleep(3)  # 创建失败后等待 3 秒再重试

            print(f"创建浏览器用户失败,已尝试 5 次")
            return None


    def get_or_create_groupid(self):
        """
        获取或创建一个组 ID。

        Returns:
            str: 组 ID,如果获取或创建失败则返回 "0"。
        """
        with self.lock:
            time.sleep(1.5)
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
            return "0"

    def get_browser(self, browser_list):
        """
        获取所有浏览器实例的列表。

        Args:
            browser_list (list): 用于存储浏览器实例信息的列表。

        Returns:
            bool: 如果获取成功,返回 True,否则返回 False。
        """
        with self.lock:
            time.sleep(1.5)
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
        with self.lock:
            for attempt in range(5):  # 重复删除五次
                time.sleep(3)  # 每次互斥 sleep 时间更改为 3 秒
                url = f"{self.matrix}/api/v1/user/delete"
                payload = {
                    "user_ids": [user_id]
                }
                headers = {
                    "Content-type": "application/json"
                }

                try:
                    response = requests.post(url, json=payload, headers=headers)
                    print(f"尝试删除浏览器{response.text}")

                    if response.json().get("code") == 0:
                        print(f"删除成功: {user_id}")

                        # 交叉验证删除是否成功
                        url = f"{self.matrix}/api/v1/user/list?user_id={user_id}"
                        response = requests.get(url, headers={"Content-type": "application/json"})

                        if response.json().get("code") == 0 and len(response.json().get("data", {}).get("list", [])) == 0:
                            print(f"交叉验证通过,浏览器用户 {user_id} 已成功删除")
                            return True
                        else:
                            print(f"交叉验证失败,浏览器用户 {user_id} 可能未被删除")
                            time.sleep(3)  # 交叉验证失败后等待 3 秒再重试
                    else:
                        print(f"删除失败: {response.json().get('msg')}")
                        time.sleep(3)  # 删除失败后等待 3 秒再重试
                except requests.exceptions.RequestException as e:
                    print(f"删除浏览器用户时发生异常: {e}")
                    time.sleep(3)  # 发生异常后等待 3 秒再重试

            print(f"删除浏览器用户失败,已尝试 5 次")
            return False

    def get_group(self, group_list):
        """
        获取组列表。
        Args:
            group_list (list): 用于存储组信息的列表。
        Returns:
            bool: 如果获取成功,返回 True,否则返回 False。
        """
        with self.lock:
            time.sleep(1.5)
            url = f"{self.matrix}/api/v1/group/list"
            
            # 设置查询参数，默认查询所有分组，每页2000条数据
            query_params = {
                "page": 1,
                "page_size": 2000
            }
            
            try:
                response = requests.get(url, params=query_params, headers={"Content-type": "application/json"})
                ret = response.text
                data = json.loads(ret)
                
                if data["code"] == 0:
                    group_list.clear()
                    for item in data["data"]["list"]:
                        group_info = {
                            "group_id": item["group_id"],
                            "group_name": item["group_name"],
                            "remark": item.get("remark", "")  # 备注字段可能存在也可能不存在
                        }
                        group_list.append(group_info)
                    
                    return True
                else:
                    print(f"获取分组失败: {data['msg']}")
                    return False
            except requests.exceptions.RequestException as e:
                print(f"获取分组列表时发生请求异常: {e}")
                return False

    def get_info(self, user_id):
        """
        获取指定用户 ID 的浏览器实例信息。

        Args:
            user_id (str): 浏览器用户的 ID。

        Returns:
            None
        """
        with self.lock:
            time.sleep(1.5)
            url = f"{self.matrix}/api/v1/user/list?user_id={user_id}"
            ret = requests.get(url, headers={"Content-type": "application/json"}).text
            print(ret)
            if json.loads(ret):
                # 这里原易语言代码没有实现具体的逻辑,需要根据实际需求补充
                pass