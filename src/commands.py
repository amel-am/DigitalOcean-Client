from disnake.ext import commands
from src.ocean_embed import DigitalOceanEmbed

class DiscordCommands(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self._bot = bot
  
    @commands.slash_command(name="digitalocean",description= "Info of your digitalocean components")
    async def ocean_info(interaction,option = commands.Param(autocomplete=["ssh","droplets","account"])):
        ocean_embed = DigitalOceanEmbed(option)
        await ocean_embed.creation()
        await interaction.response.send_message(embed=ocean_embed.get_embed)
     
    @commands.slash_command(name = "latency",description="The bot´s latency")    
    async def latency(self,interaction):
        bot_latency = round(self._bot.latency * 1000,2)
        await interaction.response.send_message(str(bot_latency) + "ms")
        
    @commands.slash_command(name="activity", description="The activity of your bot")
    async def activity(self,interaction,option=commands.Param(autocomplete=[""])):
        dict_object = {}
      

        
        