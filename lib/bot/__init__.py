from discord.ext.commands import Bot as BotBase
from discord import Embed
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from discord.ext.commands import CommandNotFound
from ..db import db

PREFIX = "."
OWNER_IDS = [190234030699053056]
CUSTOM_ICON =[739197678918828163]

class Bot(BotBase):
    def __init__(self):
        self.CUSTOM_ICON = CUSTOM_ICON 
        self.PREFIX = PREFIX
        self.ready =False
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        db.autosave(self.scheduler)

        super().__init__(command_prefix = PREFIX , owner_ids= OWNER_IDS)
    def run(self , version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()
        print("running bot ...")
        super().run(self.TOKEN , reconnect = True)
    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("something went wrong.")
            channel = self.get_channel(802491338200186880)
            await channel.send("An error occured .")
            raise

    async def on_command_error(self,ctx,exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc
    async def on_connect(self):
        print("bot connected")
    async def on_disconnect(self):
        print("bot disconnected")
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(187505904252354561)
            self.scheduler.start()

            channel = self.get_channel(802491338200186880)
            await channel.send("Now online")

            embed = Embed(title="Now online!" , description="Bot is now online and waiting for Commands" , colour=0x0077be
            ,timestamp=datetime.utcnow())
            fields = [("Discord Bot", "Bot Created by AGod#0610", True),
                        (".help" , "Get basic funktions" , True),
                        ("no descriptions for all func will add later ", "SHEEEEESH i am beamer",False)]
            for name,value,inline in fields:
                embed.add_field(name= name, value=value, inline=inline)
            embed.set_footer(text = "use fnd to find builds")
            embed.set_author(name="AGod" , icon_url=self.guild.icon_url)
            embed.set_thumbnail(url=self.guild.icon_url)
            embed.set_image(url=self.guild.icon_url)
            await channel.send(embed=embed)
            print("bot is ready")
        else:
            print("bot reconnected")
    async def on_message(self, message):
        pass
bot = Bot()

    