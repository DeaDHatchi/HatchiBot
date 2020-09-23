import discord
import json


class HatchiBot(discord.Client):
    async def on_ready(self):
        print('[+] HatchiBot Online')

    async def on_message(self):
        print('[+] Message Received')

client = HatchiBot()
client.run('zAPaEefH2rih8E1WldpeF1FuAFDkz-dv')
