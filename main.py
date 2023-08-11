import disnake
from disnake.ext import commands
from src.yaml import slash_guilds, discord_token
from src.commands import DiscordCommands

bot = commands.InteractionBot(test_guilds=slash_guilds,activity=disnake.Activity(type=disnake.ActivityType.listening,name="requests"))
               
if __name__ == "__main__":      
  bot.add_cog(DiscordCommands(bot))
  bot.run(discord_token)