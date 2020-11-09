import discord
import json


class HatchiBot(discord.Client):

    _client_reference = None
    _main_guild = None

    @property
    def client_reference(self):
        return self._client_reference

    @client_reference.setter
    def client_reference(self, reference):
        self._client_reference = reference

    @property
    def _version(self):
        return "Version 1.1.20201108"

    @property
    def voice_members(self):
        members = []
        for member in self._main_guild.members:
            if member.voice and member.voice.channel and not member.voice.afk:
                members.append(member)
        return members

    @property
    def guild(self):
        for guild in self.guilds:
            if guild.name == "Tea Baggers":
                return guild

    @property
    def raid_channel(self):
        for voice_channel in self._main_guild.voice_channels:
            if voice_channel.name == "Mythic Raid":
                return voice_channel

    @property
    def raider_roles(self):
        raider_roles = []
        for role in self._main_guild.roles:
            if role.name == "Mythic Raider" or role.name == "Officer" or role.name == "Assistant GM" or role.name == "GM":
                raider_roles.append(role)
        return raider_roles

    async def on_ready(self):
        self._main_guild = self.guild
        print(f'[+] HatchiBot Online {self._version}')

    async def on_message(self, message):
        if message.author != self.client_reference.user:
            if message.content.startswith("!raidtime"):
                print("[+] Raidtime Message Received")
                await self.raid_time()

    async def raid_time(self):
        for member in self.voice_members:
            if self.check_member_roles(member):
                await self.move_raider(member)

    async def check_member_roles(self, member):
        for role in member.roles:
            if role in self.raider_roles:
                yield True

    async def move_raider(self, member):
        print(f"[+] Moving Raider: {member}")
        await member.move_to(self.raid_channel)


def load_config():
    with open('config', 'r') as config_file:
        return json.loads(config_file.read())


if __name__ == '__main__':
    config = load_config()
    client = HatchiBot()
    client.client_reference = client
    client.run(config['token'])
