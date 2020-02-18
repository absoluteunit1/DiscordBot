DiscordBot

I was very interested in how Slack and Discord bot are built. I use discord quite often for gaming, for school and for chatting with friends
so I decided to build a chat bot for discord!

Using python and discord.py I was able to add a few features to the discord bot. Current commands are:

- /hello # replies to the user
- /goodbye # replies to the user
- /join # join a voice channel the user is in
- /leave # leaves a voice channel
- /play URL # plays the music in the youtube link provided, given that the bot is in the voice channel
- /pause /stop # pause and stops the music playing
- /queue # currently working on this feature. If more URLs are requested to play while the bot is currentply playing music, the bot will add them to the queue.

Tools used: Python, Discord.py, FFmpeg, youtube_dl, AWS EC2
