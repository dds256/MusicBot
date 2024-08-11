import re
from pyrogram import filters
from pyrogram.types import Message

from DAXXMUSIC import app
from DAXXMUSIC.utils.errors import capture_err

def convert_to_regex(search_term):
    pattern = re.compile(
        r'((iget|sget|sput|iput|invoke-\w+)'
        r'\s+([pv]\d+)(?:,\s*([pv]\d+))?,\s*L[^;]+;->\w+:\w)\s*(move-result ([pv]\d+))?',
        re.MULTILINE
    )
    
    def replace_line(match):
        instruction = match.group(1)
        move_result = match.group(6)
        
        instruction_regex = re.sub(r'([pv]\d+)', r'([pv]\\d+)', instruction)
        move_result_regex = re.sub(r'([pv]\d+)', r'([pv]\\d+)', move_result) if move_result else None
        
        return f"({instruction_regex})" + (f"\\s*(move-result {move_result_regex})" if move_result_regex else "")
    
    regex_pattern = pattern.sub(replace_line, search_term)
    
    return regex_pattern

@app.on_message(filters.command("regex"))
@capture_err
async def convert_regex_command(_, message: Message):
    # Check if the command has an argument
    if message.command and len(message.command) > 1:
        search_term = message.text.split(None, 1)[1]  # Get everything after the command
    else:
        # If no argument, check if it is a reply
        reply = message.reply_to_message
        if reply and reply.text:
            search_term = reply.text
        else:
            # Send a message if no input is provided
            return await message.reply(
                "Please provide the smali code as an input or reply with the command /regex to a message containing the code to convert."
            )

    regex_code = convert_to_regex(search_term)
    formatted_code = f"```Regex\n{regex_code}\n```\nGhostKiller thanks for the code"
    await message.reply(formatted_code, parse_mode="Markdown")
    
