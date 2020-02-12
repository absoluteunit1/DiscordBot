import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import youtube_dl
import random
import os
from text import greetings, farewells


token = os.environ['DISCORD_TOKEN']
client = commands.Bot(command_prefix = '/')

queues = {}

@client.event
async def on_ready():
    print('Braum is on the job')

@client.command()
async def probuilds(ctx, message: str):
    await ctx.send("https://www.probuilds.net/champions/details/" + message)

@client.command()
async def hello(ctx):
    await ctx.send('Hello {0.display_name}. '.format(ctx.author) +  random.choice(greetings))

@client.command()
async def bye(ctx):
    await ctx.send('Goodbye {0.display_name}. '.format(ctx.author) + random.choice(farewells))

@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Braum join {channel}")

@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Braum go now")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Not in voice channel")

@client.command()
async def play(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queded song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')
                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07
            else:
                queues.clear()
                return
        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")
    previous_song = os.path.isfile("song.mp3")
    try:
        if previous_song:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print('Trying to delete song file, but it is playing')
        await ctx.send("Silly {0.display_name}, I am playing this song now".format(ctx.author))
        return
    
    Queue_infile = os.path.isdir("./Queue")

    try:
        Queue_folder = ("./Queue")
        if Queue_infile is True:
            print("Removed old queue folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("Braum is on the job!") 

    voice = get(client.voice_clients, guild = ctx.guild)
    ydl_opts = {
         'format': 'bestaudio/best',
         'quiet': True,
         'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading audio now\n')
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname}")
    print("Playing\n")

@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Don't worry, Braum pause song")
    else:
        print("Music is not playing")
        await ctx.send("Silly {0.display_name}, no music playing now".format(ctx.author))

@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        print("Resume music")
        voice.resume()
        await ctx.send("Braum continue playing")
    else:
        print("Music is not paused.")
        await ctx.send("Braum never paused playing in first place")

@client.command()
async def stop(ctx):

    queues.clear()

    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print("Stopped music")
        voice.stop()
        await ctx.send("My shield can stop even music")
    else:
        print("Music is playing.")
        await ctx.send("Silly {0.display_name}, no music playing now".format(ctx.author))

# @client.command()
# async def queue(ctx, url: str):
#     Queue_infile = os.path.isdir("./Queue")
#     if Queue_infile is False:
#         os.mkdir("Queue")
#     DIR = os.path.abspath(os.path.realpath("Queue"))
#     q_num = len(os.listdir(DIR))
#     q_num += 1
#     add_queue = True
#     while add_queue:
#         if q_num in queues:
#             q_num += 1
#         else:
#             add_queue = False
#             queues[q_num] = q_num
#     queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s"))
#     ydl_opts = {
#          'format': 'bestaudio/best',
#          'quiet': True,
#          'outtmpl': queue_path,
#          'postprocessors':[{
#             'key':'FFmpegExtractAudio',
#             'preferredcodec':'mp3',
#             'preferredquality':'192',
#         }]
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         print('Downloading audio now\n')
#         ydl.download([url])
#     await ctx.send("Braum adding song " + str(q_num) + " to queue")
#     print("Song added to queue")


client.run(token)

