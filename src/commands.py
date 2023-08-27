from disnake import ApplicationCommandInteraction, ActivityType, Activity, Status
from disnake.ext import commands
from src.ocean_embed import DigitalOceanEmbed


class DiscordCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot = bot

    @commands.slash_command(name="digitalocean", description="Info of your digitalocean components")
    async def ocean_info(self, interaction: ApplicationCommandInteraction, option: str = commands.Param(choices=["ssh", "droplets", "account"], description="Choose what to retrieve.")):
        ocean_embed = DigitalOceanEmbed(option)
        await ocean_embed.creation()
        await interaction.response.send_message(embed=ocean_embed.get_embed)

    @commands.slash_command(name="latency", description="The bot's latency")
    async def latency(self, interaction: ApplicationCommandInteraction):
        bot_latency = round(self._bot.latency * 1000, 2)
        await interaction.response.send_message(str(bot_latency) + "ms")

    @commands.slash_command(name="activity", description="Change the bot's activity")
    async def activity(self, interaction: ApplicationCommandInteraction, status: Status, activitytype: ActivityType, activity: str):
        await self._bot.change_presence(activity=Activity(name=activity, type=activitytype), status=status)
        await interaction.response.send_message(f"The bot's activity was changed to {ActivityType(activitytype).name} {activity}")
