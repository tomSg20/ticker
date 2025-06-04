import discord
from discord.ext import commands
from openai import OpenAI

# 替换为你的 Discord Bot Token
DISCORD_TOKEN = 'TOEK'
# 替换为你的 OpenAI API Key
OPENAI_API_KEY = 'sk-1234'
# (可选) 替换为你的 OpenAI API Base URL (如果使用自定义的 OpenAI API)
OPENAI_API_BASE = 'http://localhost:4000'  # 例如: "https://your-custom-openai-endpoint.com/v1"

# 创建 OpenAI 客户端
if OPENAI_API_BASE:
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_BASE
    )
else:
    client = OpenAI(api_key=OPENAI_API_KEY)

# 定义 Bot 前缀
BOT_PREFIX = '!'  # 可以修改为任何你喜欢的命令前缀

# 创建 Bot 实例，启用 Intents
intents = discord.Intents.default()
intents.message_content = True  # 必须启用才能读取消息内容
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# OpenAI 模型选择 (你可以根据需要选择不同的模型)
MODEL_ENGINE = "gpt-4.1-mini"  # 更新为最新的模型名称

# 系统角色初始化
system_role = """
你是一个 Discord 聊天机器人，能够进行有趣、知识渊博且引人入胜的对话。
你的目的是帮助用户解答疑问，提供信息，并参与友好的交流。
你需要使用简体中文进行交流。
你不需要暴露你是一个AI模型
""".strip()

# 事件: 当 Bot 准备就绪时触发
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')

# 命令: 使用 OpenAI API 生成回复
@bot.command(name='ai')
async def ask_ai(ctx, *, prompt):  # * 用于接收命令后的所有内容作为 prompt
    """
    使用 OpenAI AI 模型生成回复。
    用法: !ai [你的问题]
    """
    try:
        # 创建一个包含用户提示和预设角色prompt的messages列表。
        messages = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt},
        ]
        
        # 调用OpenAI API，传入消息列表
        completion = client.chat.completions.create(
            model=MODEL_ENGINE,
            messages=messages,
            max_tokens=500,  # 控制生成回复的最大长度，根据需要调整
            n=1,             # 生成回复的数量，默认为 1
            stop=None,        # 设置停止生成的词语，默认为 None
            temperature=0.7, # 调整生成回复的随机性 (0.0 - 1.0)，值越高越随机
        )
        
        # 获取 OpenAI API 的回复
        response = completion.choices[0].message.content
        
        # 将回复发送到 Discord 频道
        await ctx.send(response)
        
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        await ctx.send(f"抱歉，出现了一些问题。 OpenAI API 错误: {e}")

# 处理消息 (用于直接回复消息，而不需要命令前缀)
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # 忽略 Bot 自己的消息
    
    # 如果消息中 @ 提及了 Bot
    if bot.user.mentioned_in(message):
        try:
            # 获取消息内容
            prompt = message.content.replace(f'<@{bot.user.id}>', '').strip() #去除mention部分
            
            # 创建messages列表
            messages = [
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt},
            ]
            
            # 调用 OpenAI API
            completion = client.chat.completions.create(
                model=MODEL_ENGINE,
                messages=messages,
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.7,
            )
            
            # 获取 OpenAI API 的回复
            response = completion.choices[0].message.content
            
            # 发送回复到消息所在的频道
            await message.channel.send(response)
            
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            await message.channel.send(f"抱歉，出现了一些问题。 OpenAI API 错误: {e}")
    
    await bot.process_commands(message)  # 确保处理命令

# 运行 Bot
bot.run(DISCORD_TOKEN)
