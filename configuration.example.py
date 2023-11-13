from typing import List


# Bot config

api_url: str = "http://127.0.0.1:2525/control"

bot_owners: List[int] = []
eval_owners: List[int] = []

cogs_on_start: List[str] = []

client_id: int = ...
permissions: int = 537184257
invite_link: str = \
    f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions={permissions}&scope=bot%20applications.commands"

discord_token: str = ""

# Server config

control_redirects_allowed_ips: List[str] | None = ["127.0.0.1"]

