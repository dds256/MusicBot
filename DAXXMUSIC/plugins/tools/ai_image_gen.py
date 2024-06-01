import requests
import random
from pyrogram import filters
from DAXXMUSIC import app as app

# Define the API key directly
segmind_api_key = "SG_6dfcc437b7ce9445"

# Function to generate an image using the API
def generate_image_from_prompt(user_prompt):
    random_seed = random.randint(1, 10000000000000000)
    payload = {
        "prompt": user_prompt,
        "negative_prompt": "(worst quality, low quality, normal quality, lowres, low details, oversaturated, undersaturated, overexposed, underexposed, grayscale, bw, bad photo, bad photography, bad art)++++, (watermark, signature, text font, username, error, logo, words, letters, digits, autograph, trademark, name)+, (blur, blurry, grainy), morbid, ugly, asymmetrical, mutated malformed, mutilated, poorly lit, bad shadow, draft, cropped, out of frame, cut off, censored, jpeg artifacts, out of focus, glitch, duplicate, (airbrushed, cartoon, anime, semi-realistic, cgi, render, blender, digital art, manga, amateur)++, (3D ,3D Game, 3D Game Scene, 3D Character), (bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities)++",
        "scheduler": "dpmpp_2m",
        "num_inference_steps": 25,
        "guidance_scale": 5,
        "samples": 1,
        "seed": random_seed,
        "img_width": 512,
        "img_height": 768,
        "base64": False
    }
    api_url = "https://api.segmind.com/v1/sd1.5-juggernaut"
    headers = {
        "x-api-key": segmind_api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

# Command to generate an image from a text prompt
@app.on_message(filters.command(["aiimg"]))
async def generate_image_command(bot, message):
    args = message.command[1:]
    if not args:
        await message.reply("Please provide a prompt after the /gen command. For example: /gen YourPromptHere")
        return
    
    user_prompt = ' '.join(args)
    process_message = await message.reply("Generating image...")

    try:
        image_data = generate_image_from_prompt(user_prompt)
        image_url = image_data['image_url']  # Adjust based on actual API response structure

        await bot.send_photo(message.chat.id, image_url, reply_to_message_id=message.message_id)
        await process_message.delete()
    except Exception as e:
        await process_message.edit_text(f"An error occurred: {str(e)}")
