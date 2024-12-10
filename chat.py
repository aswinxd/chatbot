mport asyncio
import openai
from pyrogram import Client, filters
from pyrogram.types import Message

# OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Pyrogram Userbot Client
app = Client(
    "humanlike_bot",
    api_id=12799559,  # Replace with your API ID
    api_hash="077254e69d93d08357f25bb5f4504580",  # Replace with your API Hash
)

def generate_response(prompt):
    """Generate a human-like response using OpenAI's GPT model."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a friendly and conversational chatbot."},
                {"role": "user", "content": prompt},
            ],
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return "I'm having trouble thinking right now. Can we try later?"

async def human_typing(simulated_delay: float, chat_id: int):
    """Simulate human typing action."""
    await app.send_chat_action(chat_id, "typing")
    await asyncio.sleep(simulated_delay)
    await app.send_chat_action(chat_id, "cancel")

@app.on_message(filters.mentioned & ~filters.bot & ~filters.service)
async def respond_to_mention(client: Client, message: Message):
    """Reply to mentions in a human-like manner."""
    try:
        user_message = message.text
        chat_id = message.chat.id

        # Simulate human delay
        delay = len(user_message) * 0.05  # Approximate human typing delay
        await human_typing(delay, chat_id)

        # Generate response using GPT
        reply = generate_response(user_message)

        # Reply to the message
        await message.reply_text(reply, quote=True)
    except Exception as e:
        await message.reply_text("Oops, something went wrong.", quote=True)

if __name__ == "__main__":
    print("Userbot is running...")
    app.run()
