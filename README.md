# tw-monitor
## 1、在安装依赖
pip3 install -r requirements.txt
## 2、修改代码
### 2、1 搜索TELEGRAM_TOKEN和CHAT_ID改成你的，怎么玩呢？这里有博文：https://hellodk.cn/post/743 可以学习
```python
# Telegram Bot Token 和 Chat ID
TELEGRAM_TOKEN = '111'
CHAT_ID = '111'
```
### 2、2 修改要监控的用户：

```python
URLS = [
    'https://x.com/ariel_sands_dan',
    'https://x.com/EvaCmore',
    'https://x.com/ouyoung11',
]
```
### 2、3 修改代理地址
```python
# 代理池（可自行更新代理）
PROXIES = [
    'http://127.0.0.1:7890'
    # 'socks5://127.0.0.1:1080',  # 示例代理
    # 'socks5://127.0.0.1:1081',
    # 'socks5://127.0.0.1:1082',
]
```

### 3、运行脚本
python tw.py
