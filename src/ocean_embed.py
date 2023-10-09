import disnake
from typing import Union
from .ocean_client import DigitalOceanClient
# This class is used to make the digitalocean embed


class DiscordEmbedDropdown(disnake.ui.StringSelect):
    def __init__(self, option: str):
        super().__init__(
            placeholder="Choose an option",
            min_values=1,
            max_values=1,
            row=1,
        )
        self._option = option
        self._ocean_client = DigitalOceanClient()
        self._index = 0
        self._embed = None
        self._page_length = 1

    @property
    def get_embed(self):
        return self._embed

    async def callback(self, inter: disnake.MessageInteraction):
        self._index = int(self.values[0])
        await self.creation()
        await inter.response.edit_message(embed=self._embed)

    def _itemloop(self, label=None, array: list = None):
        for i in range(len(array)):
            self.append_option(
                disnake.SelectOption(label=f"{label} {i + 1}: {array[i]['name']}", value=str(i)))

    def _add_description(self, k: str, v: str, n: int = 1, marks: str = None) -> None:
        lines = "\n" * n
        if marks == None:
            self._embed.description += f"{k}:{v}{lines}"
        else:
            self._embed.description += f"{k}:{marks}{v}{marks}{lines}"

    def _reassign_embed(self, label: str) -> None:
        self._embed = disnake.Embed(
            title=f"{label} (Page {self._index + 1} of {self._page_length})", description="", color=disnake.Color.blue())
        self._embed.set_image(
            "https://doimages.nyc3.digitaloceanspaces.com/Droplet,Social,Blog,Email.png")

    def _unpack(self, iterable: Union[list, dict] = None, condition: dict = {}, value: str = ""):
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
                    if k in condition:
                        value += f"{k}:{v}{condition[k]}"
                    else:
                        value += f"{k}:{v}\n"
        return value

    async def _acc_emb(self) -> None:
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

    async def _droplets_emb(self) -> None:
        droplets_info = await self._ocean_client.get_droplets()
        self._page_length = len(droplets_info)
        self._reassign_embed("droplet info")
        self._itemloop("droplet", droplets_info)
        for k, v in droplets_info[self._index].items():
            match k:
                case "networks":
                    value = self._unpack(v, {"type": "\n\n"})
                    self._embed.add_field(
                        name=k, value=value, inline=False)
                case "features":
                    value = self._unpack(v)
                    self._embed.add_field(
                        name=k, value=value, inline=False)
                case "image":
                    value = self._unpack(v)
                    self._embed.add_field(
                        name=k, value=value, inline=False)
                case "region":
                    value = self._unpack(v)
                    self._embed.add_field(
                        name=k, value=value, inline=False)
                case _:
                    if not isinstance(v, (list, dict)):
                        self._add_description(k, v)

    async def _ssh_emb(self) -> None:
        ssh_info = await self._ocean_client.get_keys()
        self._page_length = len(ssh_info)
        self._reassign_embed("ssh info")
        self._itemloop("ssh key", ssh_info)
        for k, v in ssh_info[self._index].items():
            if k == "fingerprint":
                self._add_description(k, v, 1, "```")
            else:
                self._add_description(k, v)

    async def creation(self) -> None:
        match self._option:
            case "ssh":
                await self._ssh_emb()
            case "account":
                await self._acc_emb()
            case "droplet":
                await self._droplets_emb()
        self._embed.set_footer(
            text=self._ocean_client._ratelimit_result)
        self._embed.timestamp = self._ocean_client._ratelimit_time
