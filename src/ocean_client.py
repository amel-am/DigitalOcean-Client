from aiohttp import ClientSession
from src.yaml import ocean_token
from src.constants import RequestMethods

class DigitalOceanClient(object):
  def __init__(self):
    self._headers = {'Content-Type': 'application/json','Authorization': f'Bearer {ocean_token}'}
    self._api_url = "https://api.digitalocean.com/v2/"
    self._ratelimit = ""
  
  @property
  def ratelimit(self):
    return self._ratelimit
    
  async def _request(self,method:str, link:str) -> dict:
      async with ClientSession() as session:
          async with session.request(method=method,url=link,headers=self._headers) as response:
            await self._set_ratelimits(response.headers)
            return await response.json()
          
  async def get_keys(self) -> list:
      response = await self._request(RequestMethods.GET.value,f"{self._api_url}account/keys")
      return response["ssh_keys"]
  
  async def get_droplets(self) -> list:
      response= await self._request(RequestMethods.GET.value,f"{self._api_url}droplets")
      return response["droplets"]
    
  async def get_account(self) -> dict:
    response = await self._request(RequestMethods.GET.value,f"{self._api_url}account")
    return response["account"]
  
  async def _set_ratelimits(self,dict_:dict) -> None:
    self._ratelimit = "\n".join([f"ratelimit:{dict_['ratelimit-limit']}",
                                  f"ratelimit-remaining:{dict_['ratelimit-remaining']}",
                                  f"ratelimit-reset:{dict_['ratelimit-reset']}"])
     
    
    