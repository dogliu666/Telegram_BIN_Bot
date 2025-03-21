通过用户输入发卡行识别码获取卡片基础信息，用于 Telegram Bot

# 使用方法

### 1. 申请 [BIN查询API密钥](https://rapidapi.com/trade-expanding-llc-trade-expanding-llc-default/api/bin-ip-checker/playground/apiendpoint_a4100c71-d489-46dd-94c5-920175f34a14) 和 [Telegram Bot 令牌](https://telegram.me/BotFather)

### 2. 环境准备
安装依赖： 确保已安装所需的 Python 包。可以通过以下命令安装依赖：
```
pip install -r requirements.txt
```

确保将将`.env`文件替换为实际的 API 密钥和令牌。
例如:
```
# Telegram Bot API Token
TELEGRAM_BOT_TOKEN=7890123456:KFCcrazyThursdayVivo50-FBIOpentheDoor

# RapidAPI Key for BIN IP Checker
RAPIDAPI_KEY=1145141919810aaabbbcccdd

# RapidAPI Host for BIN IP Checker
RAPIDAPI_HOST=bin-ip-checker.p.rapidapi.com
```

### 3. 启动Bot
运行脚本 `handlers.py` 来启动 Telegram Bot：
```
python handlers.py
```

### 4. 使用Bot
查询 BIN 信息： 直接输入 6 位或 8 位的 BIN 号码，Bot会返回以下信息：

- 卡头、品牌、类型、种类、级别
- 商业卡、预付卡信息
- 发卡行名称、国家、地区、货币等
- 实时汇率（如适用）

以下为示例:
```
卡头: 51953000
品牌: MASTERCARD
类型: DEBIT
种类: MASTERCARD
级别: PREPAID
商业: 否
预付: 是
卡行: TRANSACT PAYMENTS, LTD.
国家: UNITED KINGDOM 🇬🇧
代码: GB
区号: 44
地区: Europe
货币: GBP £ (British pound)
汇率: 1 GBP = 1.29 USD
1 GBP = 9.37 CNY
1 USD = 7.25 CNY
```

### 5. 本地测试
如果需要在本地测试 check_bin 函数，可以运行 `handlers.py`：
```
python handlers.py
```

按照提示输入 BIN 号码，Bot会返回查询结果。
