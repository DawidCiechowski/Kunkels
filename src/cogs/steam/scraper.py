from typing import Any, Union

import requests
import socket
from requests import Session
from collections import OrderedDict
from bs4 import BeautifulSoup as BS

STEAM_URL = "https://steamdb.info/app/"


def scrape(game_id: Union[str, int]) -> Any:
    url = f"{STEAM_URL}{game_id}/patchnotes"
    answers = socket.getaddrinfo(url, 443)
    (family, typ, proto, canonname, (address, port)) = answers[0]

    s = Session()
    headers = OrderedDict(
        {
            "Accept-Encoding": "gzip, deflate, br",
            "Host": "grimaldis.myguestaccount.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        }
    )

    s.headers = headers
    response = s.get()


print(scrape(739630))
