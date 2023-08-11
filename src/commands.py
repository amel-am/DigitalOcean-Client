from disnake.ext import commands
from src.ocean_embed import DigitalOceanEmbed

class DiscordCommands(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self._bot = bot
        self._ocean_embed= DigitalOceanEmbed()
  
    @commands.slash_command(name="digitalocean",description=  "Info of your digitalocean components")
    async def vps(self,interaction,option = commands.Param(autocomplete=["ssh","droplets","account"])):
       await self._ocean_embed.creation(option)
       embed = self._ocean_embed.embed
       await interaction.response.send_message(embed=embed)
     
    @commands.slash_command(name = "latency",description="The bot´s latency")    
    async def latency(self,interaction):
      bot_latency = round(self._bot.latency * 1000,2)
      await interaction.response.send_message(str(bot_latency) + "ms")