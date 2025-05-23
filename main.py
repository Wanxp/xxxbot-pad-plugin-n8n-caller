import tomllib

import aiohttp
import jieba
import requests

from WechatAPI import WechatAPIClient
from utils.decorators import *
from utils.plugin_base import PluginBase


class N8nWebhook(PluginBase):
    description = "N8N Webhook, 消息请求n8n回调功能"
    author = "Wanxp"
    version = "0.0.1"

    # Change Log
    # 初始化 2025-05-14 创建插件

    def __init__(self):
        super().__init__()

        with open("plugins/N8nWebhook/config.toml", "rb") as f:
            plugin_config = tomllib.load(f)

        config = plugin_config["N8nWebhook"]

        self.enable = config["enable"]
        self.sender = config["sender"]
        self.message_keyword = config["message-keyword"]
        self.webhook_url = config["n8n-webhook-url"]
        self.auth_type = config["auth-type"]
        self.auth_key = config["auth-key"]
        self.auth_value = config["auth-value"]


    @on_text_message
    async def handle_text(self, bot: WechatAPIClient, message: dict):
        if not self.enable:
            return True
        if message["FromWxid"] not in self.sender:
            return True


        content = message["Content"]
        content = content.strip()

        # 匹配keyword
        if not any(message["Content"].startswith(keyword) for keyword in self.message_keyword):
            return True
        # 处理消息
        for keyword in self.message_keyword:
            if message["Content"].startswith(keyword):
                content = content[len(keyword):]
                message["Content"] = content
                break

        api_url = self.webhook_url

        headers = {
            "Content-Type": "application/json",
        }
        if self.auth_type == "Header Auth":
            headers[self.auth_key] = self.auth_value
            response = requests.post(api_url, json=message, headers=headers, timeout=120)
        elif self.auth_type == "Basic Auth":
            headers["Authorization"] = f"Basic {self.auth_key}:{self.auth_value}"
            response = requests.post(api_url, json=message, headers=headers, timeout=120)
        elif self.auth_type == "None":
            response = requests.post(api_url, json=message, timeout=120)
        else:
            await bot.send_text_message(message["FromWxid"], f"Error: N8n Webhook插件auth-type配置不支持:{self.auth_type}")
            print("Invalid auth type. Please check your config.")
            return True

        if response.status_code != 200:
            err = f"Error: {response.status_code} - {response.text}"
            print(err)
            await bot.send_text_message(message["FromWxid"], err)
            return True
        response_data = response.text
        await bot.send_text_message(message["FromWxid"], response_data)
        return True