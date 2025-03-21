import os
import logging
from telebot import TeleBot
from dotenv import load_dotenv
from bin_service import check_bin
from currency_service import get_exchange_rate

# 配置日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 获取API令牌
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "欢迎使用BIN查询机器人！请输入6位或8位BIN号码。")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "使用方法：\n输入6位或8位BIN号码以获取相关信息。")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bin_number = message.text.strip()
    result = check_bin(bin_number)
    bot.reply_to(message, result)

def main():
    logger.info("机器人已启动")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            logger.error(f"机器人运行出错: {e}")
            logger.info("将在15秒后重试...")
            bot.stop_polling()
            time.sleep(15)  # 等待 15 秒后重试

if __name__ == "__main__":
    main()
