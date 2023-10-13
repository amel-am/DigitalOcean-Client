import disnake
from .ocean_embed import DiscordEmbedDropdown


class DropDownView(disnake.ui.View):
    def __init__(self, item: DiscordEmbedDropdown):
        super().__init__(timeout=None)
        self._item = item
        if self._item.options:
            self.add_item(self._item)

    @disnake.ui.button(label="Refresh embed", emoji="🔃", custom_id="1", row=2)
    async def refresh_button(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
        await self._item.create_embed()
        await interaction.response.edit_message(embed=self._item.embed)
