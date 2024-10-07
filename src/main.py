from client import Client
from util import to_json


if __name__ == '__main__':
    client = Client()

    news = client.news(tag='events')
    latest = client.latest(tag='academy')

    print(to_json(news), to_json(latest))

    servers = client.servers()
    server = client.server('Thaemine')

    print(to_json(servers), to_json(server))
