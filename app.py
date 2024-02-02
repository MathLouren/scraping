import time
from flask import Flask, request, render_template, redirect, url_for
import json
import locale
from flask import jsonify
from urllib.parse import urlparse, urlunparse
from amazon.amz import create_items, verif_items

# Defina a formatação de moeda local para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

app = Flask(__name__)

def is_product_cheap(product):
    # Obtém a lista de preços do histórico
    prices = [float(update["price"]) for update in product["price_updates"]]

    # Calcula a média dos preços
    average_price = sum(prices) / len(prices) if prices else 0

    # Obtém o preço mais baixo
    lowest_price = min(prices) if prices else 0

    # Define um fator de desconto (ajuste conforme necessário)
    discount_factor = 0.8

    # Calcula o preço considerado "barato" (80% do preço mais baixo)
    cheap_threshold = lowest_price * discount_factor

    # Verifica se o preço atual está abaixo da média e abaixo do limiar considerado "barato"
    current_price = float(product["price"])
    return current_price < average_price and current_price < cheap_threshold

def clean_url_amazon(url):
    parsed_url = urlparse(url)
    cleaned_path = parsed_url.path.split('/ref', 1)[0]
    cleaned_url = urlunparse((parsed_url.scheme, parsed_url.netloc, cleaned_path, '', '', ''))
    return cleaned_url

def read_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Função para escrever dados no arquivo JSON
def write_to_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

@app.route('/delete_product/<path:url>', methods=['POST'])
def delete_product(url):
    # Lê os dados do arquivo JSON
    data = read_from_file("amazon.json")

    for item in data:
        for product in item['products']:
            if product['url'] == url:
                item['products'].remove(product)
                break

    # Escreve os dados atualizados de volta no arquivo JSON
    write_to_file("amazon.json", data)

    # Redireciona de volta à página principal
    return redirect(url_for('amazon'))

@app.route('/add_price_info/<path:url>', methods=['GET', 'POST'])
def add_price_info(url):
    if request.method == 'POST':
        # Get the price value from the form
        new_price = request.form.get('price')

        # Read data from the file
        data = read_from_file("kabum.json")

        # Update the 'low_price' field for the specified product URL
        for item in data:
            for product in item['products']:
                if product['url'] == url:
                    product['low_price'] = new_price

        # Write the updated data back to the file
        write_to_file("kabum.json", data)

        # Redirect to the home page or wherever you want
        return redirect(url_for('home'))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        products_url = request.form.get('products_url')
        title = request.form.get('name')


        # Your existing logic to print the product name based on the URL
        if "kabum.com" in products_url:
            print('Kabum')
            data = read_from_file(r"C:\Users\admin\PycharmProjects\pythonProject1\kabum.json")
        elif "amazon.com":
            create_items(products_url, title)

    return render_template('create.html')

@app.route('/update')
def update():
    verif_items()
    return render_template('update.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    product_not_found = False
    if request.method == 'POST':
        url_produto = request.form.get('link_produto')
        cleaned_url = clean_url_amazon(url_produto)
        print(cleaned_url)
        if "amazon.com" in cleaned_url:
            data = read_from_file(r"C:\Users\Matheus Lourenço\PycharmProjects\scraping\amazon.json")
            for item in data:
                for info in item['products']:
                    if cleaned_url == info['url']:
                        return render_template('template_products.html', data=info)
                    else:
                        product_not_found = True
        else:
            product_not_found = True

    return render_template('home.html', product_not_found=product_not_found)


@app.route('/terabyte', methods=['GET', 'POST'])
def terabyte():
    data = read_from_file("terabyte.json")
    for item in data:
        for info in item['products']:
            # Convertendo o preço atual para float
            info['price'] = float(info['price'].replace('R$', '').replace('.', '').replace(',', '.').strip())
            info['price'] = locale.currency(float(info['price']), grouping=True)

    return render_template('template.html', data=data)


@app.route('/amazon', methods=['GET', 'POST'])
def amazon():
    data = read_from_file("amazon.json")
    for item in data:
        for info in item['products']:
            # Convertendo o preço atual para float
            info['price'] = float(info['price'].replace('R$', '').replace('.', '').replace(',', '.').strip())
            info['price'] = locale.currency(float(info['price']), grouping=True)

    return render_template('template.html', data=data)

@app.route('/kabum', methods=['GET', 'POST'])
def kabum():
    data = read_from_file("kabum.json")
    for item in data:
        for info in item['products']:
            # Convertendo o preço atual para float
            info['price'] = float(info['price'].replace('R$', '').replace('.', '').replace(',', '.').strip())
            info['price'] = locale.currency(float(info['price']), grouping=True)

    return render_template('template.html', data=data)

@app.route('/product_cheap', methods=['GET', 'POST'])
def product_cheap():
    data = read_from_file(r"C:\Users\Matheus Lourenço\PycharmProjects\scraping\amazon.json")
    cheap_products = []

    for info in data:
        for product in info['products']:
            current_price = float(product['price'].replace('R$', '').replace('.', '').replace(',', '.').strip())
            price_updates = product['price_updates'][:-1]  # Ignorando o último histórico (preço atual)


            # Considerar apenas produtos com pelo menos 5 alterações no preço
            if len(price_updates) >= 3:
                historical_prices = [float(item['price'].replace('R$', '').replace('.', '').replace(',', '.').strip()) for item in price_updates]

                # Calcula a média de preço
                average_price = sum(historical_prices) / len(historical_prices)
                low_price = average_price - average_price * 0.25
                if current_price < low_price:
                    cheap_products.append({
                        'name': product['name'],
                        'url': product['url'],
                        'current_price': current_price,
                        'average_price': average_price
                    })
                    print(product['name'])
                    print(f'Preço atual: {current_price}')
                    print(f'Média do preço: {average_price}')
                    print(f'Preço barato: {average_price - average_price * 0.25}')
                    print('__________')

    return render_template('product_cheap.html', cheap_products=cheap_products)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)