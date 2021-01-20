#! /usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @name   : Discord-Bot-Template - Easy-to-learn template for discord bot making!
# @url    : https://github.com/Cisc0-gif
# @author : Cisc0-gif

import discord, asyncio, logging, os, random, time, sys

client = discord.Client(command_prefix='/', description='Basic Commands')
TOKEN = ''

# Go To https://discordapp.com/developers/applications/ and start a new application for Token

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(handler)

def client_run():
  client.loop.create_task(background_loop())
  client.run(TOKEN)

def logwrite(msg): #writes chatlog to MESSAGES.log
  with open('MESSAGES.log', 'a+') as f:
    f.write(msg + '\n')
  f.close()

async def background_loop():
  await client.wait_until_ready()
  while not client.is_closed:
    print("Booted Up @ " + time.ctime())
    logwrite("Booted Up @ " + time.ctime())
    await asyncio.sleep(3600)  #Bootup Message

@client.event
async def on_ready():
  print('--------------------------------------------------------------------------------------')
  print('Server Connect Link:')
  print('https://discordapp.com/api/oauth2/authorize?scope=bot&client_id=' + str(client.user.id))
  print('--------------------------------------------------------------------------------------')
  print('Logged in as:')
  print(client.user.name)
  print("or")
  print(client.user)
  print("UID:")
  print(client.user.id)
  print('---------------------------------------------')
  print("LIVE CHAT LOG - See MESSAGES.log For History")
  print("---------------------------------------------")
  await client.change_presence(activity=discord.Game("Running..."), status=discord.Status.online)

@client.event
async def on_member_join(member):
  print("Member:", member, "joined!")
  logwrite("Member: " + str(member) + " joined!")

@client.event
async def on_member_remove(member):
  print("Member:", member, "removed!")
  logwrite("Member: " + str(member) + " removed!")

@client.event
async def on_guild_role_create(role):
  print("Role:", role, "was created!")
  logwrite("Role: " + str(role) + " was created!")

@client.event
async def on_guild_role_delete(role):
  print("Role:", role, "was deleted!")
  logwrite("Role: " + str(role) + " was deleted!")

@client.event
async def on_guild_channel_create(channel):
  print("Channel:", channel, "was created!")
  logwrite("Channel: " + str(channel) + " was created!")

@client.event
async def on_guild_channel_delete(channel):
  print("Channel:", channel, "was deleted!")
  logwrite("Channel: " + str(channel) + " was deleted!")

@client.event
async def on_guild_channel_update(before, after):
  print("Channel Updated:", after)
  logwrite("Channel Updated: " + str(after))

@client.event
async def on_message(message):
  if message.author == client.user:
    return #ignore what bot says in server so no message loop
  channel = message.channel
  print(message.author, "said:", message.content, "-- Time:", time.ctime()) #reports to discord.log and live chat
  logwrite(str(message.author) + " said: " + str(message.content) + "-- Time: " + time.ctime())

  if message.content == "/nickname": #if author types /nickname bot asks for input for new nickname
    await channel.send("Type /name nicknamehere")
    def check(msg):
        return msg.content.startswith('/name')
    message = await client.wait_for('message', check=check)
    name = message.content[len('/name'):].strip()
    await channel.send('{} is your new nickname'.format(name))
    await message.author.edit(nick=name)

  if message.content == "/dm": #if author types /dm bot creates dm with author
    await channel.send("Creating DM with " + str(message.author))
    await message.author.send('*DM started with ' + str(message.author) + '*')
    await message.author.send('Hello!')

  if message.content == "/ulog": #if author types /ulog bot displays updatelog
    try:
      f = open("update_log.txt","r")
      if f.mode == 'r':
        contents = f.read()
        await channel.send(contents)
    finally:
      f.close()

  if message.content == "/whoami": #if author types /whoami bot responds with username
    await channel.send(message.author)

client_run()
