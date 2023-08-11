import yaml

with open("config.yml","r") as file:
    data = yaml.safe_load(file)
    discord_token = data["discord_token"]
    ocean_token = data["ocean_token"]
    slash_guilds = data["slash_guilds"]
    