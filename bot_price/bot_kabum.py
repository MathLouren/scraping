import json
import time
import re
import locale
from telegram import Bot
from telegram.constants import ParseMode
import asyncio



def init_bot():
    def convert_price(price_str):
        match = re.search(r'[\d.,]+', price_str)
        if match:
            return locale.atof(match.group())
        return None

    # Defina a localidade para o Brasil
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    bot = Bot(token='6258576123:AAF8IBLPcOsBlEatsD5-RElTfoLiJLBvVm0')

    async def send_telegram_message(name_item, url, current_price):
        print('AUII')
        print(name_item)
        message = (
            f"*{name_item}*\n"
            f"\n*Preço: R$ {current_price}*\n\n"
            f"[{name_item}]({url})\n"
        )
        await bot.send_message(chat_id='5980301890', text=message, parse_mode=ParseMode.MARKDOWN)

    async def main():
        try:
            with open(r"C:\Users\Matheus Lourenço\PycharmProjects\scraping\amazon.json", "r", encoding='utf-8') as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            existing_data = []

        for data in existing_data:
            for prices_info in data['products']:
                price = prices_info['price']
                name_item = prices_info['name']
                url = prices_info['url']
                try:
                    if prices_info['low_price']:
                        current_price = convert_price(prices_info['price'])
                        low_price = convert_price(prices_info['low_price'])
                        if low_price > current_price:
                            await send_telegram_message(name_item, url, price)
                except:
                    continue


                # name_item = prices_info['name']
                # url = prices_info['url']
                # current_price_str = prices_info['price'].replace('R$', '').replace('.', '').replace(',', '').strip()
                # current_price = float(current_price_str)
                # num_price_updates = len(prices_info['price_updates'])
                #
                # print(current_price)
                #
                # time.sleep(2000)
                #
                # if num_price_updates > 6:
                #     all_prices = [float(price['price'].replace('R$', '').replace('.', '').replace(',', '').strip()) for price in prices_info['price_updates']]
                #     min_price = min(all_prices)
                #
                #     if min_price >= current_price:
                #         await send_telegram_message(name_item, url, current_price)

    # Chame asyncio.run() no ponto de entrada do programa
    if __name__ == "__main__":
        asyncio.run(main())

init_bot()