import json
import asyncio
import discord
import random
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

__version__ = "1.3.20201119"


@bot.event
async def on_reaction_add(reaction, user):
    if user.name != "HatchiBot":
        if await check_message_ids(reaction.message):
            print(f"[+] {user.name} has added {reaction.emoji.name}")
            await assign_role(reaction, user)


@bot.event
async def on_reaction_remove(reaction, user):
    if user.name != "HatchiBot":
        if await check_message_ids(reaction.message):
            print(f"[-] {user.name} has removed {reaction.emoji.name}")
            await remove_role(reaction, user)


@bot.command(name="blind", help="Because Blind wanted a Command")
async def blind(context):
    await context.send("`Blind volunteered to do every Mechanic in Shadowlands raiding`")


@bot.command(name="hatchi", help="Back due to high demand")
async def blind(context):
    await context.send("`Fearless Raid Leader and Master to Hatchibot. "
                       "Doesn't understand Gen Z slang, and ask him to pronounce names`")


@bot.command(name="raidtime", help="Move all Mythic Raiders to the Mythic Raid Channel. Officers Only")
@commands.has_role("Officer")
async def raidtime(context):
    raid_channel = await get_raid_channel(context.guild)
    raider_roles = await get_raider_roles(context.guild)
    voice_members = await get_voice_members(context.guild)
    for member in voice_members:
        if check_member_roles(member, raider_roles):
            await move_raider(member, raid_channel)
            await asyncio.sleep(1)  # Using this to test issues with moving members too quickly


@bot.command(name="raid", help="Example: !raid -n Mythic Nathria -d 01/06/2021 -t 10:30PM CST")
@commands.has_role("Officer")
async def raid(context):
    """
    Basic idea here is to create new message, or load a previous message that is a scheduled raid.
    Allow players to sign up for the raid with reactions to the message.
    Modify the message text with Mentions and Emojis for raid signup, as well as modify role count

    Only allow raiders to sign up for 1 role
    have switches in the message for Name, Date, Time

    -n or -name : "Name"
    -d or -date : "Date"
    -t or -time : "Time"
    example: !raidevent -n Mythic Nathria -d 01/06/2021 -t 10:30PM CST

    In theory we should also be able to send direct messages to users who have signed up as a reminder before raid

    :param context:
    :return:
    """
    # TODO: Parse the switches from Text
    # These are going to be placeholders for testing until we solve Switches
    name = "Testing Raid Name"
    time = "10:30PM CST"
    date = "01/06/2020"
    tank_count = 0
    tank_max = 2
    healer_count = 0
    healer_max = 4
    dps_count = 0
    dps_max = 14
    tank_icon = await get_emoji_by_name(context, 'tank_role_icon')
    healer_icon = await get_emoji_by_name(context, 'healer_role_icon')
    dps_icon = await get_emoji_by_name(context, 'dps_role_icon')
    # TODO: Create Raid Signup Message
    raid_message = load_saved_template(r'docs/raid_signup_template')  # Loading the signup message
    formatted_message = raid_message.format(name=name, time=time, date=date, tank_count=tank_count, tank_max=tank_max,
                                            healer_count=healer_count, healer_max=healer_max, dps_count=dps_count,
                                            dps_max=dps_max, tanks="", healers="", dps="", tank_icon=tank_icon,
                                            healer_icon=healer_icon, dps_icon=dps_icon,
                                            mythic_raider_role="`Role Placeholder`")

    response = await context.send(formatted_message)
    # TODO: Add Reactions to Raid Signup
    await add_emojis(response)
    # TODO: Modify Main Message based on Reactions
    # TODO: Save message for reload if needed


@bot.command(name='version', help="Print the latest version of HatchiBot")
async def version(context):
    await context.send("__**HatchiBot Online**__\n"
                       f"`Version: {__version__}`")


@bot.command(name='belledelphine', help="Post a random Belle Delphine Gif")
async def belledelphine(context):
    if await is_nsfw_channel(context):
        await context.send(random.choice(load_belle_delphine_links()))


@bot.command(name='laurabailey', help="Post a random Laura Bailey Gif")
async def laurabailey(context):
    await context.send(random.choice(load_laura_bailey_links()))


@bot.command(name="weebs", help="Hatchi speaks for the Weebs")
async def weebs(context):
    await context.send("`Mister! He shouted with an Arcane Caprice`\n"
                       "`My Name is Hatchi, and I speak for the Weebs.`")


@bot.command(name="github", help="Print the link to HatchiBot's Github")
async def github(context):
    await context.send(f"`HatchiBot Github Link: https://github.com/DeaDHatchi/HatchiBot`")


@bot.command(name="development", help="Print the current list of HatchiBot's In-Development Projects")
async def development(context):
    await context.send(load_saved_template(r'docs\development_template'))


@bot.command(name='mage', help='For when Laz, Blind, or Gal make fun of me because they are mean')
async def mage(context):
    file = discord.File(r"images\class_peasantry.jpg")
    await context.send(file=file, content="The level of peasantry around here is too high")


@bot.command(name='fridaythe13th', help='Mandrah helped me craft this gem')
async def fridaythe13th(context):
    file = discord.File(r"images\pika.png")
    await context.send(file=file, content="`Not even death can save you from me.. Pika Pi`")


@bot.command(name='priest', help="Because Gal")
async def priest(context):
    await context.send("`The class that wishes they were mages. Why meeeee`")


@bot.command(name='laz', help="for Laz")
async def laz(context):
    await context.send("`Big Tank that enjoys collecting mounts and 20s pull timers`")


@bot.command(name="bass", help="for Bass")
async def bass(context):
    await context.send("`A better hunter then Blind`")


@bot.command(name="daz", help="for Daz")
async def daz(context):
    await context.send("`The official guild furry. Ask him about UWU and Yiffing`")


@bot.command(name="goth", help="for Goth")
async def goth(context):
    await context.send("`Hatchi's favorite because he went Mage to join the best class`")


@bot.command(name="sin", help="for Sin")
async def sin(context):
    await context.send("`Sin go hit your brother`")


@bot.command(name="bendali", help="for Bendali")
async def bendali(context):
    await context.send("`It is said that you can hear the cries of guildies being removed from miles away`")


@bot.command(name="teenytiny", help="For Teenytiny")
async def teenytiny(context):
    await context.send("`The First Gentleman of the Guild that enjoys fine whiskey, flying planes, and cheering for the raid`")


@bot.command(name="syng", help="for Syng")
async def syng(context):
    await context.send("`Our fearless leader, Guild Momma, and #1 target of Shal's heals.`")


@bot.command(name="shal", help="for Shal")
async def shal(context):
    await context.send("`Syyng!!! Brb need a cookie`")


@bot.command(name="cory", help="for Cory")
async def cory(context):
    await context.send("`Shhh. Bigfoots lurking around these parts`")


@bot.command(name="mandrah", help="for Mandrah")
async def mandrah(context):
    await context.send("`The Neko Lord, and hoarder of the Cat Girl Harem`")


@bot.command(name="nui", help="for Nui")
async def nui(context):
    await context.send("`It's Queen Nui. Respect the title`")


@bot.command(name="gal", help="for Gal")
async def gal(context):
    await context.send("`Why meeee!`")


@bot.command(name='sparkles', help="Example: !sparkles @Hatchi")
async def sparkles(context):
    for member in context.message.mentions:
        await context.send(f"`Good Job! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧` {member.mention}")


@bot.command(name="event", help="Used for Event Testing")
async def event(context):
    response = await context.send("__**Event Testing**__\n"
                                  "Testing Reactions")
    await add_emojis(response)


@bot.command(name="roleassignment", help="Used to create Class & Role Assignment. Officers Only")
@commands.has_role("Officer")
async def roleassignment(context):
    response = await context.send(load_saved_template(r'docs\class_and_role_assignment_template'))
    await add_emojis(response)
    await save_message_id(response)


@bot.command(name='internethistory', help="Because Teenytiny")
async def internethistory(context):
    # TODO: Add randomness to "search"
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


async def is_nsfw_channel(context):
    if context.message.channel == discord.utils.get(context.guild.channels, name="nsfw-shinanigans"):
        return True
    else:
        return False


@bot.command(name="eventplanner", help="Will be used for planning events with reaction based signup")
async def eventplanner(context):
    response = await context.send("__**EVENT PLANNER TEST**__\n"
                                  "Testing out Reactions with Event Planning")
    await add_reaction(response, ':mage_class_icon:')


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


async def get_emoji_by_name(context, name):
    return discord.utils.get(context.guild.emojis, name=name)


def load_config():
    with open('config', 'r') as config_file:
        return json.loads(config_file.read())


def load_emojis():
    with open(r'docs/emojis', 'r') as emojis_file:
        return list([x.strip('\n') for x in emojis_file.readlines()])


def load_laura_bailey_links():
    with open(r'docs/laura_bailey_links', 'r') as bailey_file:
        return list([x.strip('\n') for x in bailey_file.readlines()])


def load_belle_delphine_links():
    with open(r'docs/belle_delphine_links', 'r') as belle_file:
        return list([x.strip('\n') for x in belle_file.readlines()])


def load_saved_message_ids():
    with open(r'docs/message_ids', 'r') as message_file:
        return list([x.strip('\n') for x in message_file.readlines()])


def load_emoji_id_to_role():
    with open(r'docs/emoji_id_to_role', 'r') as emoji_file:
        return {int(key): value for key, value in json.loads(emoji_file.read()).items()}


def load_saved_template(template_path):
    with open(template_path, 'r') as template_file:
        return template_file.read()


if __name__ == '__main__':
    emojis = load_emojis()
    config = load_config()
    message_ids = load_saved_message_ids()
    bot.run(config['token'])
