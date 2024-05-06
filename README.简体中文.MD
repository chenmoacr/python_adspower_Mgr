# ADS 类

## 简介
ADS（自动化设备服务）类提供了与 ADS 服务器交互的功能，该服务器管理用于自动化网页浏览任务的浏览器实例。

## 函数

### `__init__(matrix)`
- 初始化 ADS 类。
- 参数：
  - `matrix`（str）：ADS 服务器的基本 URL。

### `start_browser(user_id, open_tabs=0, ip_tab=1, launch_args="", headless=0, disable_password_filling=0, clear_cache_after_closing=0, enable_password_saving=0)`
- 启动浏览器实例。
- 参数：
  - `user_id`（str）：用户 ID。
  - `open_tabs`（int，可选）：要打开的标签页数。默认为 0。
  - `ip_tab`（int，可选）：IP 标签页的索引。默认为 1。
  - `launch_args`（str，可选）：附加的启动参数。默认为空字符串。
  - `headless`（int，可选）：是否以无头模式启动浏览器（1 表示 True，0 表示 False）。默认为 0。
  - `disable_password_filling`（int，可选）：是否禁用密码填充（1 表示 True，0 表示 False）。默认为 0。
  - `clear_cache_after_closing`（int，可选）：是否在关闭浏览器后清除缓存（1 表示 True，0 表示 False）。默认为 0。
  - `enable_password_saving`（int，可选）：是否启用密码保存（1 表示 True，0 表示 False）。默认为 0。
- 返回：
  - 元组：包含 chrome_driver 和 debug_port 的元组。

### `stop_browser(user_id)`
- 停止浏览器实例。
- 参数：
  - `user_id`（str）：用户 ID。
- 返回：
  - bool：如果操作成功，则为 True，否则为 False。

### `check_start_status(user_id)`
- 检查浏览器实例的状态。
- 参数：
  - `user_id`（str）：用户 ID。
- 返回：
  - bool：如果浏览器处于活动状态，则为 True，否则为 False。

### `create(name, is_proxy=False, proxy_type="", proxy_host="", proxy_port="", proxy_user="", proxy_password="", group_id="")`
- 创建新用户。
- 参数：
  - `name`（str）：用户名称。
  - `is_proxy`（bool，可选）：是否使用代理。默认为 False。
  - `proxy_type`（str，可选）：代理类型。默认为空字符串。
  - `proxy_host`（str，可选）：代理主机。默认为空字符串。
  - `proxy_port`（str，可选）：代理端口。默认为空字符串。
  - `proxy_user`（str，可选）：代理身份验证的用户名。默认为空字符串。
  - `proxy_password`（str，可选）：代理身份验证的密码。默认为空字符串。
  - `group_id`（str，可选）：组 ID。默认为空字符串。
- 返回：
  - str：创建的用户的 ID。

### `get_or_create_groupid()`
- 获取或创建组 ID。
- 返回：
  - str：组 ID。

### `get_browser(browser_list)`
- 检索浏览器列表。
- 参数：
  - `browser_list`（list）：用于存储浏览器信息的空列表。
- 返回：
  - bool：如果成功，则为 True，否则为 False。

### `del_browser(user_id)`
- 删除浏览器实例。
- 参数：
  - `user_id`（str）：用户 ID。
- 返回：
  - bool：如果成功，则为 True，否则为 False。

### `get_group(group_list)`
- 检索组列表。
- 参数：
  - `group_list`（list）：用于存储组信息的空列表。

### `get_info(user_id)`
- 检索用户信息。
- 参数：
  - `user_id`（str）：用户 ID。

## 使用方法
1. 从 `ads` 模块中导入 ADS 类。
2. 通过提供 ADS 服务器的基本 URL 初始化一个 ADS 对象。
3. 使用 ADS 类提供的各种函数与 ADS 服务器交互并管理浏览器实例。

## 示例
```python
from ads import ADS

# 初始化 ADS 对象
ads = ADS("http://local.adspower.net:50325")

# 创建新浏览器实例
user_id = ads.create("Browser", is_proxy=True, proxy_type="socks5", proxy_host="192.168.8.124", proxy_port="1080", proxy_user="123", proxy_password="123")

# 启动浏览器实例
chrome_driver, debug_port = ads.start_browser(user_id)

# 执行自动化网页浏览任务

# 停止浏览器实例
ads.stop_browser(user_id)

# 删除浏览器实例
ads.del_browser(user_id)
