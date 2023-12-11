from typing import List
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Server config
server_ip = os.getenv("SERVER_IP")
server_port = int(os.getenv("SERVER_PORT"))
server_domen = os.getenv("SERVER_DOMEN")
control_redirects_allowed_ips = os.getenv("CONTROL_REDIRECTS_ALLOWED_IPS").split(",") if os.getenv(
    "CONTROL_REDIRECTS_ALLOWED_IPS") else None

# Bot config
api_url = os.getenv("API_URL")
bot_owners = [int(owner_id) for owner_id in os.getenv("BOT_OWNERS", "").split(",") if owner_id]
eval_owners = [int(owner_id) for owner_id in os.getenv("EVAL_OWNERS", "").split(",") if owner_id]
cogs_on_start = os.getenv("COGS_ON_START").split(",") if os.getenv("COGS_ON_START") else []
client_id = int(os.getenv("CLIENT_ID"))
permissions = int(os.getenv("PERMISSIONS"))
invite_link = os.getenv("INVITE_LINK")
discord_token = os.getenv("DISCORD_TOKEN")
