import requests
from DAXXMUSIC import app
from pyrogram import filters
from utils import bs4, wget, asyncio, re, requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "99",
    "Origin": "https://saveig.app",
    "Connection": "keep-alive",
    "Referer": "https://saveig.app/en",
}

async def download(client, event) -> bool:
    link = extract_url(event.message.text)

    start_message = await event.respond("Processing Your insta link ....")
    try:
        url = link.replace("instagram.com", "ddinstagram.com").replace("==", "%3D%3D")
        await client.send_file(event.chat_id, url[:-1] if url.endswith("=") else url[:],
                               caption="Here's your Instagram content")
        return True
    except:
        content_type = determine_content_type(link)
        try:
            if content_type == 'reel':
                await download_reel(client, event, link)
                await start_message.delete()
                return True
            elif content_type == 'post':
                await download_post(client, event, link)
                await start_message.delete()
                return True
            elif content_type == 'story':
                await download_story(client, event, link)
                await start_message.delete()
                return True
            else:
                await event.reply(
                    "Sorry, unable to find the requested content. Please ensure it's publicly available.")
                await start_message.delete()
                return True
        except:
            await event.reply("Sorry, unable to find the requested content. Please ensure it's publicly available.")
            await start_message.delete()
            return False

async def download_reel(client, event, link):
    try:
        meta_tag = await get_meta_tag(link)
        content_value = f"https://ddinstagram.com{meta_tag['content']}"
    except:
        meta_tag = await search_saveig(link)
        content_value = meta_tag[0] if meta_tag else None

    if content_value:
        await send_file(client, event, content_value)
    else:
        await event.reply("Oops, something went wrong")

async def download_post(client, event, link):
    meta_tags = await search_saveig(link)
    if meta_tags:
        for meta in meta_tags[:-1]:
            await asyncio.sleep(1)
            await send_file(client, event, meta)
    else:
        await event.reply("Oops, something went wrong")

async def download_story(client, event, link):
    meta_tag = await search_saveig(link)
    if meta_tag:
        await send_file(client, event, meta_tag[0])
    else:
        await event.reply("Oops, something went wrong")

async def get_meta_tag(link):
    getdata = requests.get(link).text
    soup = bs4.BeautifulSoup(getdata, 'html.parser')
    return soup.find('meta', attrs={'property': 'og:video'})

async def search_saveig(link):
    meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"},
                             headers=headers)
    if meta_tag.ok:
        res = meta_tag.json()
        return re.findall(r'href="(https?://[^"]+)"', res['data'])
    return None

async def send_file(client, event, content_value):
    try:
        await client.send_file(event.chat_id, content_value, caption="Here's your Instagram content")
    except:
        fileoutput = f"{str(content_value)}"
        downfile = wget.download(content_value, out=fileoutput)
        await client.send_file(event.chat_id, fileoutput, caption="Here's your Instagram content")

@app.on_message(filters.command("instadownload"))
async def handle_insta_download(client, message):
    await download(client, message)