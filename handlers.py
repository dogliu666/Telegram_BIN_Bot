import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
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

# 初始化 bot 和 dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start']))
async def start_command(message: types.Message):
    await message.reply("欢迎使用BIN查询机器人！请输入6位或8位BIN号码。")

@dp.message(Command(commands=['help']))
async def help_command(message: types.Message):
    await message.reply("使用方法：\n输入6位或8位BIN号码以获取相关信息。")

@dp.message()
async def handle_message(message: types.Message):
    bin_number = message.text.strip()
    
    # 先发送"查询中..."消息 
    waiting_msg = await message.reply("查询中...")
    
    # 获取查询结果
    result = check_bin(bin_number)
    
    # 删除"查询中..."消息
    await bot.delete_message(chat_id=waiting_msg.chat.id, message_id=waiting_msg.message_id)
    
    # 发送查询结果
    await message.reply(result)

# 添加启动事件处理器
@dp.startup()
async def on_startup():
    logger.info("机器人已启动")

async def main():
    # 使用轮询模式启动 bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("机器人已停止")
    except Exception as e:
        logger.error(f"机器人运行出错: {e}")
