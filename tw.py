import time
import asyncio
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from telegram import Bot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from itertools import cycle
import random
import hashlib

# Telegram Bot Token 和 Chat ID
TELEGRAM_TOKEN = '111'
CHAT_ID = '111'

# 监控的多个用户X页面
URLS = [
    'https://x.com/ariel_sands_dan',
    'https://x.com/EvaCmore',
    'https://x.com/ouyoung11',
]

# 代理池（可自行更新代理）
PROXIES = [
    'http://127.0.0.1:7890',
    'https://127.0.0.1:7890',
    'socks5://127.0.0.1:1080',
    'socks5://127.0.0.1:1081',
    'socks5://127.0.0.1:1082',
]

# 用户代理池
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
]

# 配置Selenium WebDriver


def setup_driver(proxy=None, user_agent=None):
    options = Options()
    if user_agent:
        options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--headless")  # 以无头模式运行
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-gpu")

    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    service = Service('/usr/local/bin/chromedriver')  # 指定Chromedriver路径
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# 启动浏览器并抓取多个页面元素


def scrape_data(driver, url):
    driver.get(url)

    try:
        # 等待多个目标元素加载
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[3]/div/div//span"))
        )

        # 提取每个元素的文本内容
        content_list = [element.text for element in elements]
        return content_list

    except Exception as e:
        print(f"错误: {e}")
        return None
    finally:
        driver.quit()

# 从 JSON 文件读取上次的抓取内容


def load_previous_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# 保存抓取的数据到 JSON 文件


def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 比较当前抓取的内容和上次的内容


def has_data_changed(current_data, previous_data):
    if not previous_data:
        return True
    # 比较哈希值
    current_hash = hashlib.md5(json.dumps(
        current_data, ensure_ascii=False).encode('utf-8')).hexdigest()
    previous_hash = hashlib.md5(json.dumps(
        previous_data, ensure_ascii=False).encode('utf-8')).hexdigest()
    return current_hash != previous_hash

# 发送 Telegram 消息


async def send_telegram_message(content_list, url):
    bot = Bot(token=TELEGRAM_TOKEN)
    # 合并所有内容为一条消息
    merged_content = "\n".join(content_list)
    # 发送合并后的消息
    await bot.send_message(chat_id=CHAT_ID, text=f"抓取的内容:\n{merged_content}\n来自: {url}")

# 异步的 main 函数


async def main():
    proxies = cycle(PROXIES)  # 循环使用代理池
    user_agents = cycle(USER_AGENTS)  # 循环使用User-Agent池

    for url in URLS:
        proxy = next(proxies)  # 获取下一个代理
        user_agent = next(user_agents)  # 获取下一个User-Agent
        driver = setup_driver(proxy=proxy, user_agent=user_agent)  # 配置驱动
        content_list = scrape_data(driver, url)  # 抓取数据

        # 设置保存数据的文件路径
        file_path = f"{url.split('/')[-1]}_data.json"

        # 读取上次的数据
        previous_data = load_previous_data(file_path)

        # 如果抓取的内容有变化，发送通知并保存新数据
        if content_list and has_data_changed(content_list, previous_data):
            await send_telegram_message(content_list, url)
            save_data(file_path, content_list)
        elif content_list:
            print(f"{url} 的内容没有变化。")  # 当没有变化时打印信息

        time.sleep(random.randint(5, 10))  # 每次访问间隔5到10秒，避免过于频繁

# 启动事件循环并执行异步任务
if __name__ == "__main__":
    asyncio.run(main())
