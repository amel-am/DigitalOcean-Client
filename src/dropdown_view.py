import disnake
from .ocean_embed import DiscordEmbedDropdown
from re import search


class DropDownView(disnake.ui.View):
    def __init__(self, embed_dropdown: DiscordEmbedDropdown):
        super().__init__(timeout=None)
        self._embed_dropdown = embed_dropdown
        if self._embed_dropdown.options:
            self.add_item(self._embed_dropdown)

    @disnake.ui.button(label="Update embed contents", emoji="🔃", custom_id="1", row=2)
    async def update_content(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        # Signal to user that the content is being updated.
        await interaction.response.edit_message(content="The content is being updated...", embed=None)

        # Get the original message to access the embed
        message = interaction.message
        embed = message.embeds[0]

        # Extract the title from the embed
        title = embed.title

        # Find the start index of the first digit in the title
        search_page = search("[0-9]+", title)

        # Extract the page number
        self._embed_dropdown.index = int(search_page.group()) - 1

        # Extract the choice part from the title
        self._embed_dropdown.choice = title.split(" ")[0]

        # Create a new embed based on the updated choice and index
        await self._embed_dropdown.create_embed()

        # Edit the original message with the new embed and updated view
        await interaction.edit_original_message(content=None, embed=self._embed_dropdown.embed)
