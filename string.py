rom pyrogram import Client
from pyrogram.session import StringSession

# Replace API_ID and API_HASH with your credentials
api_id = API_ID
api_hash = "API_HASH"

with Client(":memory:", api_id=api_id, api_hash=api_hash) as app:
    print("Your StringSession:")
    print(app.export_session_string())
