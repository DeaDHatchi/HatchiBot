import json
import asyncio
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

__version__ = "1.2.20201111"


@bot.event
async def on_reaction_add(reaction, user):
    if user.name != "HatchiBot":
        if await check_message_ids(reaction.message):
            await assign_role(reaction, user)


@bot.event
async def on_reaction_remove(reaction, user):
    if user.name != "HatchiBot":
        if await check_message_ids(reaction.message):
            await remove_role(reaction, user)


@bot.command(name="raidtime", help="Move all Mythic Raiders to the Mythic Raid Channel. Officers Only")
@commands.has_role("Officer")
async def raidtime(context):
    raid_channel = await get_raid_channel(context.guild)
    raider_roles = await get_raider_roles(context.guild)
    voice_members = await get_voice_members(context.guild)
    for member in voice_members:
        if check_member_roles(member, raider_roles):
            await move_raider(member, raid_channel)
            await asyncio.sleep(.25)  # Using this to test issues with moving members too quickly


@bot.command(name='version', help="Print the latest version of HatchiBot")
async def version(context):
    await context.send(f"__**HatchiBot Online**__\n`Version: {__version__}`")


@bot.command(name="github", help="Print the link to HatchiBot's Github")
async def github(context):
    await context.send(f"`HatchiBot Github Link: https://github.com/DeaDHatchi/HatchiBot`")


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


@bot.command(name="event", help="Used for Event Testing")
async def event(context):
    response = await context.send("__**Event Testing**__\n"
                                  "Testing Reactions")
    await add_emojis(response)


@bot.command(name="roleassignment", help="Used to create Role Assignment Message. Officers Only")
@commands.has_role("Officer")
async def roleassignment(context):
    response = await context.send("__**Role Assignment Message**__\n"
                                  r"React to the Emoji's on this message to add your role assignments")
    await add_emojis(response)
    await save_message_id(response)


@bot.command(name='internethistory', help="Because Teenytiny")
async def internethistory(context):
    await context.send(r"`Internet History is Secured, but HatchiBot has recently searched for Belle Delphine`")


async def assign_role(reaction, member):
    emoji_id_to_role = load_emoji_id_to_role()
    role = discord.utils.get(member.guild.roles, name=emoji_id_to_role[reaction.emoji.id])
    if role not in member.roles:
        await member.add_roles(role)


async def remove_role(reaction, member):
    emoji_id_to_role = load_emoji_id_to_role()
    role = discord.utils.get(member.guild.roles, name=emoji_id_to_role[reaction.emoji.id])
    if role in member.roles:
        await member.remove_roles(role)


async def roles_by_id(roles):
    return {role.id: role for role in roles}


async def add_emojis(message):
    for emoji in emojis:
        await add_reaction(message, emoji)


async def save_message_id(message):
    message_ids.append(message.id)
    with open('docs/message_ids', 'a') as message_file:
        message_file.write(f'{message.id}\n')


async def check_message_ids(message):
    if message.id in message_ids:
        return True
    else:
        return False


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


async def add_reaction(message, reaction):
    await message.add_reaction(reaction)


def load_config():
    with open('config', 'r') as config_file:
        return json.loads(config_file.read())


def load_emojis():
    with open(r'docs/emojis', 'r') as emojis_file:
        return list([x.strip('\n') for x in emojis_file.readlines()])


def load_saved_message_ids():
    with open(r'docs/message_ids', 'r') as message_file:
        return list([x.strip('\n') for x in message_file.readlines()])


def load_emoji_id_to_role():
    with open(r'docs/emoji_id_to_role', 'r') as emoji_file:
        return {int(key): value for key, value in json.loads(emoji_file.read()).items()}


if __name__ == '__main__':
    emojis = load_emojis()
    config = load_config()
    message_ids = load_saved_message_ids()
    bot.run(config['token'])
