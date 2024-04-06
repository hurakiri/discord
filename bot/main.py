import google.generativeai as genai
from interactions import Client, Intents, SlashContext, ContextMenuContext, Message, OptionType, slash_option, message_context_menu, listen, slash_command
import os

global chat

genai_key = os.getenv("GEMINI")

class talkgenai():
    def __init__(
            self,
            api_key:str=None,
            message:str=None
    ):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name='gemini-pro') 
        self.model = model
        self.chat = None
        if message:
            self.message = message

    def talk(
            self,
            message:str=None
            ):
        if message:
            self.message = message

        if not self.chat:
            chat = self.model.start_chat()
            self.chat = chat

        res = self.chat.send_message(message)
        # print(self.chat)
        return res
    
    def reset_talk(
            self
    ):
        global talkai
        talkai = talkgenai(genai_key)
        chat = self.model.start_chat()
        self.chat = chat

        return True

bot = Client(intents=Intents.ALL| Intents.MESSAGE_CONTENT)
talkai = talkgenai(genai_key)


@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

@slash_command(name='chat', description="Google Geminiと対話します")
@slash_option(
    name="talk",
    description="geminiと会話する内容を入力します",
    required=True,
    opt_type=OptionType.STRING
)
async def chat_ai(ctx: SlashContext, talk: str):
    await ctx.defer()
    res = talkai.talk(talk)
    # do stuff for a bit
    # await asyncio.sleep(600)

    await ctx.send(res.text)

@slash_command(name='reset', description="geminiとのトーク内容をリセットします")
async def chat_reset(ctx: SlashContext):
    status = talkai.reset_talk()
    if status is True:
        reset_alert = "トーク内容がリセットされました。"
        await ctx.send(reset_alert)

@slash_command(name='invite', description="このBotの招待リンクを送信します")
async def botinviteurl(ctx: SlashContext):
    await ctx.send("https://discord.com/oauth2/authorize?client_id=1224670967301935166&permissions=8&scope=bot")


#token
discord_token = os.getenv("TOKEN")

bot.start(discord_token)