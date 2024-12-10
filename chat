from telethon import TelegramClient, events
import openai
import asyncio
import random

# OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Ask for Telegram API credentials
API_ID = int(input("Enter your Telegram API ID: "))
API_HASH = input("Enter your Telegram API HASH: ")
PHONE_NUMBER = input("Enter your phone number with country code: ")  # E.g., +123456789

# Group details
GROUP_ID = input("Enter the Group ID or username: ")

# Chat history for contextual replies
chat_history = []

# Initialize the Telegram client
client = TelegramClient("dynamic_session", API_ID, API_HASH)

async def generate_response(prompt):
    """
    Generate a response using OpenAI GPT.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=100,
            temperature=0.9,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I can't think of anything to say right now."

@client.on(events.NewMessage(chats=GROUP_ID))
async def handle_new_message(event):
    global chat_history

    # Only respond if the bot is tagged or the message is a reply
    if event.is_reply or f"@{(await client.get_me()).username}" in event.text:
        original_message = ""
        
        # If it's a reply, get the replied-to message's text
        if event.is_reply:
            reply_msg = await event.get_reply_message()
            original_message = reply_msg.text if reply_msg else ""
        
        # Add the original and new messages to the chat history
        if original_message:
            chat_history.append({"role": "user", "content": original_message})
        chat_history.append({"role": "user", "content": event.text})

        # Keep chat history limited for efficiency
        if len(chat_history) > 10:
            chat_history = chat_history[-10:]

        # Delay before responding
        await asyncio.sleep(random.randint(5, 15))

        # Generate a response using OpenAI GPT
        response = await generate_response(chat_history)

        # Add the bot's response to the chat history
        chat_history.append({"role": "assistant", "content": response})

        # Send the response to the group
        await event.reply(response)

async def main():
    # Authenticate the client
    await client.start(phone=PHONE_NUMBER)
    
    # Join the group if not already a member
    try:
        await client.get_entity(GROUP_ID)  # Validate group
        print(f"Bot is running and monitoring messages in {GROUP_ID}...")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"Error accessing group: {e}")

# Run the client
with client:
    client.loop.run_until_complete(main())
