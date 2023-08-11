import disnake
import datetime
from src.ocean_client import DigitalOceanClient

#This class is used to make the digitalocean embed
class DigitalOceanEmbed():
    def __init__(self):
        self._ocean_client = DigitalOceanClient()
        self.embed = disnake.Embed(title="",description="",color=disnake.Color.blue())
        self.embed.set_image("https://doimages.nyc3.digitaloceanspaces.com/Droplet,Social,Blog,Email.png")
    
    async def _cat(self,k: str,v: str,n: int = 1,marks: str = None):
        self.embed.description = ""
        lines = "\n" * n
        if marks != None:
            self.embed.description += f"{k}:{marks}{v}{marks}{lines}" 
        else:
            self.embed.description += f"{k}:{v}{lines}" 
            
    async def _acc_emb(self):
        account_info = await self._ocean_client.get_account()
        await self._dict_loop(account_info)
            
    async def _dict_loop(self,dict_:dict):
        for k,v in dict_.items():
            if isinstance(v,list) or isinstance(v,dict):
                continue
            elif k == "fingerprint":
                await self._cat(k,v,1,"```")
            elif k == "vpc_uuid":
                await self._cat(k,v,2)
            elif k == "email":
                continue
            else:
                await self._cat(k,v)
                    
    async def _list_loop(self,list_:list):
        for e in list_:
            await self._dict_loop(e)
                     
    async def _droplets_emb(self):
        droplets_info = await self._ocean_client.get_droplets()
        await self._list_loop(droplets_info)
    
    async def _ssh_emb(self):
        ssh_info = await self._ocean_client.get_keys()
        await self._list_loop(ssh_info)
                    
    async def embed_creation(self,option:str):
        self.embed.title = f"{option} info"
        match option:
            case "ssh":
                await self._ssh_emb()
            case "account":
                await self._acc_emb()
            case "droplets":
                await self._droplets_emb()
        self.embed.remove_footer()
        self.embed.set_footer(text=self._ocean_client._ratelimit)
        return self.embed
                