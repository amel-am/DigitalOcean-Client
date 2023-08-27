import disnake
from src.ocean_client import DigitalOceanClient

# This class is used to make the digitalocean embed


class DigitalOceanEmbed():
    def __init__(self, option: str):
        self._option = option
        self._ocean_client = DigitalOceanClient()
        self._embed = disnake.Embed(
            title=f"{option} info", description="", color=disnake.Color.blue())
        self._embed.set_image(
            "https://doimages.nyc3.digitaloceanspaces.com/Droplet,Social,Blog,Email.png")

    @property
    def get_embed(self):
        return self._embed

    def _cat(self, k: str, v: str, n: int = 1, marks: str = None) -> None:
        lines = "\n" * n
        if marks != None:
            self._embed.description += f"{k}:{marks}{v}{marks}{lines}"
        else:
            self._embed.description += f"{k}:{v}{lines}"

    async def _acc_emb(self) -> None:
        account_info = await self._ocean_client.get_account()
        self._dict_loop(account_info)

    def _dict_loop(self, dict_: dict) -> None:
        for k, v in dict_.items():
            if isinstance(v, (list, dict)):
                continue
            match k:
                case "fingerprint":
                    self._cat(k, v, 1, "```")
                case  "vpc_uuid":
                    self._cat(k, v, 2)
                case "email":
                    continue
                case _:
                    if v == "":
                        self._cat(k, "None")
                    else:
                        self._cat(k, v)

    def _list_loop(self, list_: list) -> None:
        for e in list_:
            self._dict_loop(e)

    async def _droplets_emb(self) -> None:
        droplets_info = await self._ocean_client.get_droplets()
        self._list_loop(droplets_info)

    async def _ssh_emb(self) -> None:
        ssh_info = await self._ocean_client.get_keys()
        self._list_loop(ssh_info)

    async def creation(self) -> None:
        match self._option:
            case "ssh":
                await self._ssh_emb()
            case "account":
                await self._acc_emb()
            case "droplets":
                await self._droplets_emb()
        self._embed.set_footer(text=self._ocean_client.ratelimit)
        self._embed.timestamp = self._ocean_client._ratelimit_time
