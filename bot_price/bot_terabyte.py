import json

try:
    with open(r"C:\Users\Matheus Lourenço\PycharmProjects\scraping\Terabyte\products.json", "r", encoding='utf-8') as json_file:
        existing_data = json.load(json_file)
except FileNotFoundError:
    # Se o arquivo não existir, inicialize com uma lista vazia
    existing_data = []

current_price = 0
url_item = ""
name_item = ""

for data in existing_data:
    for prices_info in data['products']:
        current_price = float(prices_info['price'].replace(',', "").replace('R$ ', ''))
        number_prices = len(prices_info['price_updates'])
        url_item = prices_info['url']
        name_item = prices_info['name']
        num_price_updates = len(str(current_price).replace(',', '').replace('R$', '').strip())
        all_prices = [float(price['price'].replace('R$', '').replace('.', '').replace(',', '.').replace(' ', '')) for price in prices_info['price_updates']]
        min_price = min(all_prices)
        if number_prices >= 5:
            if current_price != 0.0 and current_price <= min_price:
                print(name_item)
                print(current_price)
                print(url_item)
