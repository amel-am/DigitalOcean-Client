from enum import StrEnum

CHOICES = ["ssh", "droplet", "account"]
MAX_OPTIONS = 25
PICTURE_URL = "https://doimages.nyc3.digitaloceanspaces.com/Droplet,Social,Blog,Email.png"
BASE_API_URL = "https://api.digitalocean.com/v2"


class RequestMethods(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
