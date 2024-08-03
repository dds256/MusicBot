from pyrogram import filters
import requests, random
from bs4 import BeautifulSoup
from DAXXMUSIC import app
import pytgcalls
import os, yt_dlp 
from pyrogram.types import Message
from pytgcalls.types import AudioVideoPiped
from DAXXMUSIC.plugins.play import play
from DAXXMUSIC.plugins.play.pornplay import play

vdo_link = {}

async def get_video_stream(link):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
    }
    x = yt_dlp.YoutubeDL(ydl_opts)
    info = x.extract_info(link, False)
    video = os.path.join(
        "downloads", f"{info['id']}.{info['ext']}"
    )
    if os.path.exists(video):
        return video
    x.download([link])
    return video

def get_video_info(title):
    url_base = f'https://www.xnxx.com/search/{title}'
    try:
        with requests.Session() as s:
            r = s.get(url_base)
            soup = BeautifulSoup(r.text, "html.parser")
            video_list = soup.findAll('div', attrs={'class': 'thumb-block'})
            if video_list:
                random_video = random.choice(video_list)
                thumbnail = random_video.find('div', class_="thumb").find('img').get("src")
                if thumbnail:
                    # Replace the size in the thumbnail URL to get 500x500
                    thumbnail_500 = thumbnail.replace('/h', '/m').replace('/1.jpg', '/3.jpg')
                    link = random_video.find('div', class_="thumb-under").find('a').get("href")
                    if link and 'https://' not in link:  # Check if the link is a valid video link
                        return {'link': 'https://www.ex.com' + link, 'thumbnail': thumbnail_500}
    except Exception as e:
        print(f"Error: {e}")
    return None

@app.on_message(filters.command("porn"))
async def get_random_video_info(client, message):
    if len(message.command) == 1:
        await message.reply("Please provide a title to search.")
        return

    title = ' '.join(message.command[1:])
    await message.reply("Processing your request...")
    video_info = get_video_info(title)
    
    if video_info:
        video_link = video_info['link']
        video = await get_video_stream(video_link)
        vdo_link[message.chat.id] = {'link': video_link}
        await message.reply_video(video, caption=f"{title}")
    else:
        await message.reply(f"No video link found for '{title}'.")

@app.on_message(filters.command("xnxx"))
async def get_random_video_info(client, message):
    if len(message.command) == 1:
        await message.reply("Please provide a title to search.")
        return

    title = ' '.join(message.command[1:])
    await message.reply("Processing your request...")
    video_info = get_video_info(title)
    
    if video_info:
        video_link = video_info['link']
        video = await get_video_stream(video_link)
        
        # Placeholder for additional information
        views = "N/A"  # Replace with actual logic to get views
        ratings = "N/A"  # Replace with actual logic to get ratings

        await message.reply_video(
            video,
            caption=f"Add Title: {title}\nViews: {views}\nRatings: {ratings}"
        )
    else:
        await message.reply(f"No video link found for '{title}'.")
