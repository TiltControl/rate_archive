from backtracked import Client, Presence, Message, Song, User, SongInfo
import logging
import asyncio
from datetime import datetime
import copy
import os
from dotenv import load_dotenv
from configparser import ConfigParser
from pathlib import Path

load_dotenv('.env')

QUEUP_USER  = os.getenv('QUEUP_USER')
QUEUP_PASS = os.getenv('QUEUP_PASS')

config = ConfigParser()
config.read('config.ini')
rate_folder = config.get('RATE','rate')
reveal_day = config.get('RATE','reveal_day')
queup_room = config.get('RATE','queup_room')


def main():

    c = Client()
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(name)s: %(message)s")

    file_dir = "rate_reveal_archive/" + rate_folder + "/"
    Path(file_dir).mkdir(parents=True, exist_ok=True)

    file_name = "Day " + str(reveal_day) + ".txt"
    f = open(file_dir + file_name, "a")

    @c.event
    async def on_ready():
        print("Logged in as {0.username}".format(c.user))
        await c.join_room(queup_room)
        f.write("Bot is online!\n")
        f.write("Tracking starting at " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '\n')

    @c.event
    async def on_chat(message: Message):
        user = message.author.username
        timestamp = message.created_at.strftime("%H:%M:%S")
        content = message.content
        messageFormatted = "[" + timestamp + "] " + user + ": " + content + "\n"
        f.write(messageFormatted)
        f.flush()

    @c.event  
    async def on_playlist_song_add(song: Song):
        timestamp = song.played_at.strftime("%H:%M:%S")
        user = song.user.username
        try:
            song_info = copy.deepcopy(song.song_info)
            songFormatted= ""
            songName = song_info.name
            songLink = ""
            songSource = song_info.source
            if songSource == "youtube":
                songMediaID = song_info.media_id
                songLink = "https://www.youtube.com/watch?v=" + songMediaID
            songFormatted = "\t[" + timestamp + "]\n"
            songFormatted+= "\tTitle: " + songName + "\n" 
            songFormatted+= "\tLink: " + songLink + "\n"
            songFormatted+= "\tQueued by: " + user 
        except:
            songFormatted = "Song failed to play"
        f.write("\n---------SONG PLAYING---------\n")
        f.write("" + songFormatted)
        f.write("\n---------SONG PLAYING---------\n")
        f.flush()
    try:
        #c.run(email="popheadssonglist@gmail.com", password="winners2bestrevealEVAR!")
        print(QUEUP_USER)
        print(QUEUP_PASS)
        c.run(email=QUEUP_USER, password=QUEUP_PASS)
    finally:
        f.write("\nTracking ended at " + datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        f.write("\nBot offline")
        f.close()


if __name__ == "__main__":
    main()