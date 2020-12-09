import discord
import os
import youtube_dl
from discord.ext import commands
from discord.utils import get
client = commands.Bot(command_prefix = '/mt ')


vote_chest = [] #투표함
vote_time = False

@client.event
async def on_ready():
    print(client.user.id)
    print("ready")

@client.command()
async def 명령어(ctx):
    await ctx.send("```        ##### 명령어 리스트 #####"
                   "\n\n mt 등록 [?] : 해당 [?]을 투표목록에 추가합니다."
                   "\n\n mt 초기화 : 등록된 게임을 초기화 합니다"
                   "\n\n mt 투표시작 : 투표가 시작되며 더이상 추가할수 없습니다"
                   "\n\n mt 투표 [?] : 해당 [번호] 에  투표합니다."
                   "\n\n mt 투표종료 : 투표 결과를 확인합니다.```")

@client.command()
async def 등록(ctx,thing):

    global list

    if not vote_time:
        list.append(thing)
        await ctx.send(f"{thing} 등록 완료")
    else:
        await ctx.send("투표 진행중입니다. 등록할수 없습니다.")


@client.command()
async def 투표시작(ctx):

    global vote_time

    vote_time = True


    for i in range(0,len(list)):
        vote_chest.append(0)
        await ctx.send(f"{list[i]} 해당 번호 :  "+ str(i))




@client.command()
async def 투표(ctx,vote):

    if 0 <= int(vote) < len(list):
        vote_chest[int(vote)] += 1
        
        print(vote_chest)
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author} 투표완료")

    else:
        await ctx.send("올바르지 않은 숫자 입니다.")


@client.command()
async def  투표종료(ctx):

    global vote_time,list,vote_chest

    for i in range(0,len(list)):

        await ctx.send(f"{list[0]} 의 득표수 : {vote_chest[0]} ")
        del list[0]
        del vote_chest[0]

    vote_time = False

@client.command()
async def 초기화(ctx):

    global vote_chest,list

    for i in range(0,len(list)):

        del list[0]
        if len(vote_chest) != 0:
            del vote_chest[0]
    else:
        print((ctx.author).status)

@client.command()
async def 상태확인(ctx,member : discord.Member):
    await ctx.send(f"{member} 의 상태는 {member._client_status} 입니다. ")
    await client.change_presence(activity=discord.Game("긁적"),status=discord.Status.idle)

@client.command()
async def 음악재생(ctx):
    channel = ctx.author.voice.channel
    voice = await channel.connect()
    voice.play(discord.FFmpegPCMAudio("hasta.mp3"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.6
    voice.is_playing()
    print("Play")

@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send("ERROR: Music playing")
            return

        await ctx.send("Getting everything ready now")

        voice = get(client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing: {nname[0]}")
        print("playing\n")






client.run("Nzg1NDM3MDUwODUzMzkyNDE0.X831QQ.ziJlOp7wbpln-noYnJ6g1h7vj_o")