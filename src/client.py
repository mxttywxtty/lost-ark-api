from __future__ import annotations

from util import soup
import json

ENDPOINTS = [
    "server-status",
    "news"
]

LANG = [
    "en-us"
]

TAGS = [
    "academy",
    "events",
    "general",
    "release-notes",
    "showcase",
    "updates"
]

SERVERS = [
    "Thaemine",
    "Brelshaza",
    "Luterra",
    "Balthorr",
    "Nineveh",
    "Inanna",
    "Vairgrys",
    "Ortuus",
    "Elpon",
    "Ratik",
    "Arcturus",
    "Gienah"
]

BASE = "https://www.playlostark.com"


class Client:
    def __init__(self, lang: str = 'en-us') -> None:
        self._url = f"{BASE}/{lang}"

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, val) -> None:
        self._url = val

    def latest(self, tag: str = "") -> json:
        return next(iter(self.news(tag)))

    def news(self, tag: str = "") -> json:
        url = f"{self._url}/news"
        dct = dict()

        if tag not in TAGS:
            raise Exception("Valid tags: ", ', '.join([tag for tag in TAGS]))
        else:
            url += f"?tag={tag}"

        res = soup(url).find_all('div', class_="ags-SlotModule ags-SlotModule--blog ags-SlotModule--threePerRow")

        for x in res:
            url = x.find('a', class_="ags-SlotModule-spacer")['href']
            title = x.find('span', class_="ags-SlotModule-contentContainer-heading").text.strip()
            description = x.find('span', class_="ags-SlotModule-contentContainer-text "
                                                " ags-SlotModule-contentContainer-text--blog "
                                                " ags-SlotModule-contentContainer-text")
            timestamp = x.find('span', class_="ags-SlotModule-contentContainer-date").text.strip()

            if not description:
                description = None
            else:
                description = description.split('\n')[0].text.strip()

            dct[url] = {'title': title,
                        'description': description,
                        'timestamp': timestamp}

        return dct

    def server(self, server: str):
        if server not in SERVERS:
            raise Exception("Valid tags: ", ', '.join([server for server in SERVERS]))

        return self.servers().get(server)

    def servers(self):
        url = f"{self._url}/support/server-status"
        dct = dict()

        servers = soup(url).find_all('div', class_='ags-ServerStatus-content-responses-response-server')

        for s in servers:
            _s = s.find('div', class_='ags-ServerStatus-content-responses-response-server-name').text.strip()

            if s.find('div', class_='ags-ServerStatus-content-responses-response-server-status '
                                    'ags-ServerStatus-content-responses-response-server-status--good'):
                dct[_s] = 'OK'

            if s.find('div', class_='ags-ServerStatus-content-responses-response-server-status '
                                    'ags-ServerStatus-content-responses-response-server-status--busy'):
                dct[_s] = 'BUSY'

            if s.find('div', class_='ags-ServerStatus-content-responses-response-server-status '
                                    'ags-ServerStatus-content-responses-response-server-status--maintenance'):
                dct[_s] = 'MAINTENANCE'

            if s.find('div', class_='ags-ServerStatus-content-responses-response-server-status '
                                    'ags-ServerStatus-content-responses-response-server-status--full'):
                dct[_s] = 'FULL'

        return dct


client = Client()
