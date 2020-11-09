import discord
import json


class HatchiBot(discord.Client):

    _client_reference = None

    @property
    def client_reference(self):
        return self._client_reference

    @client_reference.setter
    def client_reference(self, reference):
        self._client_reference = reference

    @property
    def __version__(self):
        return "Version 1.1.20201109"

    @property
    def guild(self):
        for guild in self.guilds:
            if guild.name == "Tea Baggers":
                return guild

    @property
    def raid_channel(self):
        for voice_channel in self.guild.voice_channels:
            if voice_channel.name == "Mythic Raid":
                return voice_channel

    @property
    def raider_roles(self):
        return list(filter(lambda role: role.name == "Mythic Raider" or role.name == "Officer" or role.name == "Assistant GM" or role.name == "GM", self.guild.roles))

    async def on_ready(self):
        print(f'[+] HatchiBot Online {self.__version__}')

    async def on_message(self, message):
        if message.author != self.client_reference.user:
            if message.content.startswith("!raidtime"):
                print("[+] !raidtime Message Received")
                await self.raid_time()
            if message.content.startswith("!querymembers"):
                print("[+] !querymembers Message Received")
                await self.query_members()

    async def voice_members(self):
        return list(filter(lambda member: member.voice and member.voice.channel and not member.voice.afk, self.guild.members))

    async def raid_time(self):
        for member in await self.voice_members():
            if self.check_member_roles(member):
                await self.move_raider(member)

    async def check_member_roles(self, member):
        for role in member.roles:
            if role in self.raider_roles:
                yield True

    async def move_raider(self, member):
        print(f"[+] Moving Raider: {member}")
        await member.move_to(self.raid_channel)

    async def query_members(self):
        for member in await self.voice_members():
            print(f"[+] Member: {member}")


def load_config():
    with open('config', 'r') as config_file:
        return json.loads(config_file.read())


if __name__ == '__main__':
    config = load_config()
    client = HatchiBot()
    client.client_reference = client
    client.run(config['token'])
