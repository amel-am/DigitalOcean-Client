from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from src.ocean_embed import DigitalOceanEmbed


class DiscordCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot = bot

    @commands.slash_command(dm_permission=True, name="digitalocean", description="Info of your digitalocean components")
    async def ocean_info(self, interaction: ApplicationCommandInteraction, option: str = commands.Param(choices=["ssh", "droplets", "account"])):
        ocean_embed = DigitalOceanEmbed(option)
        await ocean_embed.creation()
        await interaction.response.send_message(embed=ocean_embed.get_embed)

    @commands.slash_command(name="latency", description="The bot's latency")
    async def latency(self, interaction: ApplicationCommandInteraction):
        bot_latency = round(self._bot.latency * 1000, 2)
        await interaction.response.send_message(str(bot_latency) + "ms")
