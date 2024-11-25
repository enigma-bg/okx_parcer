import aiohttp
import asyncio
import json
import time

async def get_price(session, inst_id):
    url = f"https://www.okx.com/api/v5/market/ticker?instId={inst_id}"
    async with session.get(url) as response:
        data = await response.json()
        if data['code'] == '0':
            price = data['data'][0]['last']
            return float(price)
        else:
            print(f"Ошибка при получении данных {inst_id}: {data['msg']}")
            return None

async def main():
    coins = ['BTC-USDT', 'ETH-USDT', 'BNB-USDT']
    start_time = time.perf_counter()
    async with aiohttp.ClientSession() as session:
        tasks = [get_price(session, coin) for coin in coins]
        prices = await asyncio.gather(*tasks)
        for coin, price in zip(coins, prices):
            if price:
                print(f"Текушая цена {coin.split('-')[0]}: {price} USDT")

    with open('prices.json', 'w') as json_file:
        json.dump(prices, json_file, indent=4)

    elapsed_time = time.perf_counter() - start_time
    print("Цены сохранены в prices.json")
    print(f"Общее время выполнения запроса: {elapsed_time:.2f} секунд")


asyncio.run(main())

