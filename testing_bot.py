import discord
import json
from discord.ext import commands

bot = commands.Bot(command_prefix="!")


@bot.command(name="raidtime", help="Move all Mythic Raiders to the Mythic Raid Channel")
@commands.has_role("GM")
async def raidtime(context):
    guild = context.guild
    raid_channel = await get_raid_channel(guild)
    raider_roles = await get_raider_roles(guild)
    voice_members = await get_voice_members(guild)
    for member in voice_members:
        if check_member_roles(member, raider_roles):
            await move_raider(member, raid_channel)


@bot.commands(name='queryusers', help="Print each voice member for debugging purposes")
async def queryusers(context):
    voice_members = await get_voice_members(context)
    for member in voice_members:
        print(f"Voice Member: {member}")


async def get_raid_channel(guild):
    for voice_channel in guild.voice_channels:
        if voice_channel.name == "Mythic Raid":
            return voice_channel


async def get_raider_roles(guild):
    raider_roles_names = ["Mythic Raider", "Officer", "Assistant GM", "GM"]
    return list(filter(lambda role: role.name in raider_roles_names, guild.roles))


async def get_voice_members(guild):
    return list(filter(lambda member: member.voice and member.voice.channel and not member.voice.afk, guild.members))


async def check_member_roles(member, raider_roles):
    for role in member.roles:
        if role in raider_roles:
            yield True


async def move_raider(member, raid_channel):
    print(f"[+] Moving Raider: {member}")
    await member.move_to(raid_channel)


def load_config():
    with open('config', 'r') as config_file:
        return json.loads(config_file.read())


if __name__ == '__main__':
    config = load_config()
    bot.run(config['token'])
