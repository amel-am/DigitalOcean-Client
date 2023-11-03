from enum import StrEnum

CHOICES = ["ssh", "droplet", "account"]


class RequestMethods(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
