import disnake

class DiscordButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
