import requests
from fake_useragent import UserAgent
import random
from telegram import ForceReply, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters


def request():
    user_agent = UserAgent().chrome
    version = user_agent.split('Chrome/')[1].split('.')[0]
    platform = ['macOS', 'Windows', 'Linux']
    headers = {
        'authority': 'api-marketplace.edgevana.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-EN,en;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
        'origin': 'https://srv.edgevana.com',
        'referer': 'https://srv.edgevana.com/',
        'sec-ch-ua': f'"Google Chrome";v="{version}", "Chromium";v="{version}", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': f'"{random.choice(platform)}"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': user_agent
    }

    response = requests.get(
        url='https://api-marketplace.edgevana.com/core-wrapper/prod/solana/getSolanaServerStockV2.1',
        headers=headers,
    )
    resulsts = response.json()
    avalible_server = []
    # print(len(resulsts))
    for res in resulsts:
        if res['description'] == 'Solana Testnet Server':
            server = [location for location in res['location'] if location['remaining'] == 1]
            count_server = len(server)
            for i in range(count_server):
                if server:
                    # print(server)
                    name = server[i]['name']
                    cost = server[i]['cost'][0]['amount']
                    order_link = server[i]['order_link']
                    # rt = f"{name}, price: {cost} | Link: {order_link} "
                    rt = f'{name}, price: {cost} | Order: <a href="{order_link}">server</a>'
                    avalible_server.append(rt)
                else:
                    avalible_server = 'No server for TdS'
    return avalible_server


if __name__ == '__main__':
    avalible_server = request()
    for server in avalible_server:
        print(server)

"""
curl 'https://api-marketplace.edgevana.com/core-wrapper/prod/solana/getSolanaServerStockV2.1' \
  -H 'authority: api-marketplace.edgevana.com' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'dnt: 1' \
  -H 'origin: https://srv.edgevana.com' \
  -H 'referer: https://srv.edgevana.com/' \
  -H 'sec-ch-ua: "Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'sec-gpc: 1' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' \
  --compressed
  """
