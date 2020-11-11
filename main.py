import json
import asyncio
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

__version__ = "1.2.20201111"


@bot.command(name="raidtime", help="Move all Mythic Raiders to the Mythic Raid Channel")
@commands.has_role("Officer")
async def raidtime(context):
    raid_channel = await get_raid_channel(context.guild)
    raider_roles = await get_raider_roles(context.guild)
    voice_members = await get_voice_members(context.guild)
    for member in voice_members:
        if check_member_roles(member, raider_roles):
            await move_raider(member, raid_channel)
            await asyncio.sleep(.25)  # Using this to test issues with moving members too quickly


@bot.command(name='queryusers', help="Print each voice member for debugging purposes")
async def queryusers(context):
    voice_members = await get_voice_members(context.guild)
    for member in voice_members:
        print(f"Voice Member: {member}")


@bot.command(name='version', help="Print the latest version of HatchiBot")
async def version(context):
    await context.send(f"[+] HatchiBot Online - Version: {__version__}")


@bot.command(name="github", help="Print the link to HatchiBot's Github")
async def github(context):
    await context.send(f"[+] HatchiBot Github Link: https://github.com/DeaDHatchi/HatchiBot")


@bot.command(name="development", help="Print the current list of HatchiBot's In-Development Projects")
async def development(context):
    await context.send("__**Currently Under Development Features**__\n"
                       "`Dueling Game: Developed by Hatchi, Gal, Goth`\n"
                       "`Reaction Based Role Assignment: Assign Roles, Classes based on Reactions`\n"
                       "`Event Planner: Basic Event Planner based on Reactions`")


@bot.command(name='mage', help='For when Laz, Blind, or Gal make fun of me because they are mean')
async def mage(context):
    file = discord.File(r"images\class_peasantry.jpg")
    await context.send(file=file, content="The level of peasantry around here is too high")


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
    if member.voice.channel.name != raid_channel.name:
        print(f"[+] Moving Raider: {member}")
        await member.move_to(raid_channel)


def load_config():
    with open('config', 'r') as config_file:
        return json.loads(config_file.read())


if __name__ == '__main__':
    config = load_config()
    bot.run(config['token'])
