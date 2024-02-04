from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import json
import uuid
import time

proxy_options = {
    'http': 'http://0bbe3ea206e21e7e:RNW78Fm5@185.130.105.109:10000',
    'https': 'http://0bbe3ea206e21e7e:RNW78Fm5@185.130.105.109:10000',
    'no_proxy': 'localhost,127.0.0.1'
}

options = {
    'proxy': {
        'http': proxy_options['http'],
        'https': proxy_options['https'],
        'no_proxy': proxy_options['no_proxy']
    }
}

def generate_random_id():
    return str(uuid.uuid4())

url = "https://www.kabum.com.br/computadores/notebooks/notebook-gigabyte"

try:
    with open(r"C:\Users\admin\PycharmProjects\pythonProject\scraping\kabum.json", "r", encoding='utf-8') as json_file:
        existing_data = json.load(json_file)
except FileNotFoundError:
    # Se o arquivo não existir, inicialize com uma lista vazia
    existing_data = []

def create_item():


    urls_in_json = []

    for item in existing_data:
        urls_in_json.append(item['url'])


    if url in urls_in_json:
        init_check()
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)

        penultimo_li = driver.find_element(By.CSS_SELECTOR, '.pagination li:nth-last-child(2)')
        penultimo_li = int(penultimo_li.text)

        contador = 0
        id = 0

        title = driver.find_element(By.CSS_SELECTOR, '#headerName h1').text
        data_atual = time.localtime()

        # Formata apenas a data usando strftime
        formato_data = "%d/%m/%Y"
        save_date = time.strftime(formato_data, data_atual)

        # Crie um novo dicionário para cada item
        result_data = {
            "file_name": title,
            "url": url,
            "products": []
        }
        try:
            while contador <= penultimo_li:
                itens = driver.find_elements(By.CSS_SELECTOR, 'main .productCard')
                for item in itens:
                    title_item = item.find_element(By.CSS_SELECTOR, 'main .nameCard').text
                    url_item = item.find_element(By.CSS_SELECTOR, 'main .productLink').get_attribute('href')
                    price_item = item.find_element(By.CSS_SELECTOR, 'main .priceCard').text
                    if price_item != "R$ ----":
                        id += 1

                        result_data["products"].append({
                            "id": id,
                            "name": title_item,
                            "price": price_item,
                            "url": url_item,
                            "price_updates": [{"date": save_date, "price": price_item}]
                        })

                next_btn = driver.find_element(By.CSS_SELECTOR, '.nextLink')
                next_btn.click()
                time.sleep(3)
                contador += 1

        except:
            print('Fim do loop')

        # Salve os dados atualizados no arquivo JSON (fora do loop)
        existing_data.append(result_data)
        with open(r"C:\Users\admin\PycharmProjects\pythonProject\scraping\kabum.json", "w", encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, indent=2, ensure_ascii=False)

def init_check():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(chrome_options=chrome_options, seleniumwire_options=options)

    def check_itens():
        print("Executando Kabum Scraping...")
        urls_json = []
        urls_now = []
        for item in existing_data:
            if item["url"] == url:
                for url_item in item['products']:
                    urls_json.append(url_item['url'])

        driver.get(url)

        try:
            penultimo_li = driver.find_element(By.CSS_SELECTOR, '.pagination li:nth-last-child(2)')
            penultimo_li = int(penultimo_li.text)
        except:
            penultimo_li = int(1)

        contador = 0

        data_atual = time.localtime()
        # Formata apenas a data usando strftime
        formato_data = "%d/%m/%Y"
        save_date = time.strftime(formato_data, data_atual)

        try:
            while contador <= penultimo_li:
                itens = driver.find_elements(By.CSS_SELECTOR, 'main .productCard')
                for item in itens:
                    title_item = item.find_element(By.CSS_SELECTOR, 'main .nameCard').text
                    url_item = item.find_element(By.CSS_SELECTOR, 'main .productLink').get_attribute('href')
                    price_item = item.find_element(By.CSS_SELECTOR, 'main .priceCard').text
                    urls_now.append(url_item)
                    if price_item != "R$ ----":
                        if url_item in urls_json:
                            for product in existing_data:
                                if product["url"] == url:
                                    for itn in product['products']:
                                        if itn['url'] == url_item:
                                            if itn['price'] != price_item:
                                                print(f'Preço antigo {itn["price"]} : Preço Novo {price_item} ')
                                                itn['price'] = price_item
                                                update_entry = {
                                                    "date": time.strftime("%d/%m/%Y"),
                                                    "price": f"{price_item}"
                                                }
                                                itn['price_updates'].append(update_entry)

                                                with open(r"C:\Users\admin\PycharmProjects\pythonProject\scraping\kabum.json", "w", encoding='utf-8') as json_file:
                                                    json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

                        if url_item not in urls_json:
                            for product in existing_data:
                                random_id = generate_random_id()
                                if product["url"] == url:
                                    product["products"].append({
                                        "id": random_id,
                                        "name": title_item,
                                        "price": price_item,
                                        "url": url_item,
                                        "price_updates": [{"date": save_date, "price": price_item}]
                                    })

                                    with open(r"C:\Users\admin\PycharmProjects\pythonProject\scraping\kabum.json", "w", encoding='utf-8') as json_file:
                                        json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

                                    print(f'O item com url: {url_item} foi adicionado')


                    else:
                        driver.find_element(By.CSS_SELECTOR, '.FJIDSFIUSHF').click()

                next_btn = driver.find_element(By.CSS_SELECTOR, '.nextLink')
                next_btn.click()
                time.sleep(3)
                contador += 1
        except:
            time.sleep(10)
            pass

    for item in existing_data:
        url = item['url']
        try:
            print(item['file_name'])
        except:
            pass
        try:
            check_itens()
        except:
            pass

init_check()