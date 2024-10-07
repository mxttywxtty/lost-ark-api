import httpx
import json
from bs4 import BeautifulSoup


def status(url: str) -> int:
    return httpx.get(url).status_code


def content(url: str) -> bytes:
    return httpx.get(url).content


def soup(url: str) -> BeautifulSoup:
    if status(url) == 404:
        raise Exception

    return BeautifulSoup(content(url), 'html.parser')


def to_json(dct: dict, indent: int = 4) -> json:
    return json.dumps(dct, indent=indent)
