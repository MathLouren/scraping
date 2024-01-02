from flask import Flask, render_template, redirect, url_for
import json
import locale
from flask import jsonify

# Defina a formatação de moeda local para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

app = Flask(__name__)

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
    data = read_from_file("./amazon/products.json")

    for item in data:
        for product in item['products']:
            if product['url'] == url:
                item['products'].remove(product)
                break

    # Escreve os dados atualizados de volta no arquivo JSON
    write_to_file("./amazon/products.json", data)

    # Redireciona de volta à página principal
    return redirect(url_for('amazon'))


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/terabyte', methods=['GET', 'POST'])
def terabyte():
    data = read_from_file("./Terabyte/products.json")

    for item in data:
        for info in item['products']:
            # Convertendo o preço atual para float
            info['price'] = float(info['price'].replace('R$', '').replace('.', '').replace(',', '.').strip())

            info['price'] = locale.currency(float(info['price']), grouping=True)

    return render_template('terabyte.html', data=data)


@app.route('/amazon', methods=['GET', 'POST'])
def amazon():
    data = read_from_file("./amazon/products.json")
    for item in data:
        for info in item['products']:
            # Convertendo o preço atual para float
            info['price'] = float(info['price'].replace('R$', '').replace('.', '').replace(',', '.').strip())

            info['price'] = locale.currency(float(info['price']), grouping=True)

    return render_template('amazon.html', data=data)

@app.route('/kabum', methods=['GET', 'POST'])
def kabum():
    data = read_from_file("./kabum/products.json")
    for item in data:
        for info in item['products']:
            # Convertendo o preço atual para float
            info['price'] = float(info['price'].replace('R$', '').replace('.', '').replace(',', '.').strip())

            info['price'] = locale.currency(float(info['price']), grouping=True)

    return render_template('kabum.html', data=data)



if __name__ == '__main__':
    app.run(debug=True)