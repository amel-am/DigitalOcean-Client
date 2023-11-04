import disnake
from typing import Union
from loguru import logger
from .ocean_client import DigitalOceanClient
from .constants import CHOICES, MAX_OPTIONS, PICTURE_URL


class DiscordEmbedDropdown(disnake.ui.StringSelect):
    def __init__(self, choice: str):
        super().__init__(
            placeholder="Choose a choice",
            min_values=1,
            max_values=1,
            row=1,
        )
        self._embed = None
        self._ocean_client = DigitalOceanClient()
        self._index = 0
        self._choice = choice
        self._page_length = 1

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index: int):
        if isinstance(index, int):
            self._index = index
        else:
            logger.error(f"The given arg {index} is not of type int!")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, choice):
        if choice in CHOICES:
            self._choice = choice
        else:
            logger.error("The choice is not available!")

    @property
    def embed(self):
        return self._embed

    async def callback(self, inter: disnake.MessageInteraction):
        self._index = int(self.values[0])
        await self.create_embed()
        await inter.response.edit_message(embed=self._embed)

    def _append_option(self, label=None, array: list = None):
        if not self.options:
            length = len(array)
            if length > MAX_OPTIONS:
                num = MAX_OPTIONS
            else:
                num = length
            for i in range(num):
                self.append_option(
                    disnake.SelectOption(
                        label=f"{label} {i + 1}: {array[i]['name']}", value=str(i))
                )

    def _add_description(self, k: str, v: str, n: int = 1, marks: str = None):
        lines = "\n" * n
        if marks is None:
            self._embed.description += f"{k}:{v}{lines}"
        else:
            self._embed.description += f"{k}:{marks}{v}{marks}{lines}"

    def _reassign_embed(self, label: str):
        self._embed = disnake.Embed(
            title=f"{label} (Page {self._index + 1} of {self._page_length})",
            description="",
            color=disnake.Color.blue()
        )
        self._embed.set_image(
            PICTURE_URL)
        self._embed.set_footer(text=self._ocean_client._ratelimit_result)
        self._embed.timestamp = self._ocean_client._ratelimit_time

    def _unpack_request(self, iterable: Union[list, dict] = None, condition: dict = {}, value: str = ""):
        if isinstance(iterable, list):
            if len(iterable) < 20:
                for e in iterable:
                    if isinstance(e, dict):
                        value = self._unpack(e, condition, value)
                    else:
                        value += f"{e}\n"
        else:
            for k, v in iterable.items():
                if isinstance(v, list):
                    if v and len(v) < 20:
                        value += f"***{k}***\n"
                    value = self._unpack(v, condition, value)
                else:
                    # If key in condition dict use the value to append it to string.
                    value += f"{k}:{v}" + condition.get(k, '\n')
        return value

    async def _add_account(self):
        account_info = await self._ocean_client.get_account()
        self._reassign_embed("account info")
        for k, v in account_info.items():
            if k == "email":
                continue
            elif k == "team":
                value = self._unpack(v)
                self._embed.add_field(k, value)
            else:
                self._add_description(k, v)

    async def _add_droplets(self):
        droplets_info = await self._ocean_client.get_droplets()
        self._page_length = len(droplets_info)
        self._reassign_embed("droplet info")
        self._append_option("droplet", droplets_info)
        for k, v in droplets_info[self._index].items():
            match k:
                case "networks":
                    value = self._unpack(v, {"type": "\n\n"})
                    self._embed.add_field(name=k, value=value, inline=False)
                case "features":
                    value = self._unpack(v)
                    self._embed.add_field(name=k, value=value, inline=False)
                case "image":
                    value = self._unpack(v)
                    self._embed.add_field(name=k, value=value, inline=False)
                case "region":
                    value = self._unpack(v)
                    self._embed.add_field(name=k, value=value, inline=False)
                case _:
                    if not isinstance(v, (list, dict)):
                        self._add_description(k, v)

    async def _add_ssh(self) -> None:
        ssh_info = await self._ocean_client.get_keys()
        self._page_length = len(ssh_info)
        self._reassign_embed("ssh info")
        self._append_option("ssh key", ssh_info)
        for k, v in ssh_info[self._index].items():
            if k == "fingerprint" or k == "public_key":
                self._add_description(k, v, 1, "```")
            else:
                self._add_description(k, v)

    async def create_embed(self) -> None:
        match self._choice:
            case "ssh":
                await self._add_ssh()
            case "account":
                await self._add_account()
            case "droplet":
                await self._add_droplets()
