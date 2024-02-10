import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import uuid
import requests

bot_token = '6258576123:AAF8IBLPcOsBlEatsD5-RElTfoLiJLBvVm0'
chat_id = '5980301890'


def send_telegram_message(product_name, current_price, url, img):
    api_url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    message = f'**{product_name}**\n\nR$ {current_price}\n\n{url}'

    params = {
        'chat_id': chat_id,
        'photo': img,
        'caption': message,
        'parse_mode': 'Markdown'
    }

    response = requests.post(api_url, params=params)

    if response.status_code != 200:
        print(f'Erro ao enviar mensagem para o Telegram. Status Code: {response.status_code}')




def generate_random_id():
    return str(uuid.uuid4())

def create_items(url, name):
    url = url

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(1)
    error = None
    max_attempts = 10

    for attempt in range(max_attempts):
        try:
            error = driver.find_element(By.XPATH, '//*[@id="h"]/div/a/img').text
        except:
            break

        driver.refresh()
        time.sleep(2)

    title = name


    # Carregar dados existentes do arquivo JSON
    try:
        with open(r"C:\Users\admin\PycharmProjects\pythonProject\scraping\amazon.json", "r", encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        # Se o arquivo não existir, inicialize com uma lista vazia
        existing_data = []

    result_data = {
        "file_name": title.replace('"', ''),
        "url": url,
        "products": []
    }

    index_item = 0
    while True:
        itens = driver.find_elements(By.CSS_SELECTOR, '[data-asin]')
        save_date = time.strftime("%d/%m/%Y")
        for index, item in enumerate(itens, start=1):
            try:
                title_item = item.find_element(By.CSS_SELECTOR, "h2").text
                price_item = item.find_element(By.CLASS_NAME, 'a-price-whole').text
                url_item = item.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")

                parsed_url = urlparse(url_item)
                base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                base_url = url_item.rsplit('/', 1)[0]

                # Verifique se o file_name já existe no JSON
                existing_file = next((file for file in existing_data if file["file_name"] == result_data["file_name"]), None)

                if existing_file:
                    # Verifique se a URL do item já está salva
                    if not any(product["url"] == base_url for product in existing_file["products"]):
                        existing_file["products"].append({
                            "id": index_item,
                            "name": title_item,
                            "price": price_item,
                            "url": base_url,
                            "price_updates": [{"date": save_date, "price": price_item}]
                        })
                else:
                    # Crie um novo file_name
                    result_data["products"].append({
                        "id": index_item,
                        "name": title_item,
                        "price": price_item,
                        "url": base_url,
                        "price_updates": [{"date": save_date, "price": price_item}]
                    })
                    existing_data.append(result_data)

                index_item += 1
            except Exception:
                pass

        # Salve os dados atualizados no arquivo JSON
        with open(r"C:\Users\admin\PycharmProjects\pythonProject\scraping\amazon.json", "w", encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, indent=2, ensure_ascii=False)

        try:
            next_button = driver.find_element(By.CLASS_NAME, 's-pagination-next')
            if 's-pagination-disabled' in next_button.get_attribute('class'):
                print('Chegou no final')
                break
            else:
                print('Indo para próxima pag')
                next_btn = driver.find_element(By.CSS_SELECTOR, ".s-pagination-next")
                next_btn.click()
                time.sleep(5)
        except Exception as e:
            print("Error:", str(e))
            break

        time.sleep(5)

    driver.quit()


def verif_items():
    urls_json = []
    urls_now = []
    try:
        with open(r"C:\Users\admin\PycharmProjects\pythonProject\scraping\amazon.json", "r", encoding='utf-8') as json_file:
            existing_data = json.load(json_file)

    except FileNotFoundError:
        print("Arquivo JSON não encontrado.")

    # Configuração do Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    itens = driver.find_elements(By.CSS_SELECTOR, '[data-asin]')

    error = None
    max_attempts = 10

    for product in existing_data:
        for item in product['products']:
            urls_json.append(item['url'])
        print(product['file_name'])
        driver.get(product['url'])
        for attempt in range(max_attempts):
            try:
                error = driver.find_element(By.XPATH, '//*[@id="h"]/div/a/img').text
            except:
                break

            driver.refresh()
            time.sleep(2)

        time.sleep(1)
        while True:
            itens = driver.find_elements(By.CSS_SELECTOR, '[data-asin]')
            save_date = time.strftime("%d/%m/%Y")
            index_item = 0
            for item in itens:
                index_item += 1
                try:
                    img_url_container = item.find_element(By.CLASS_NAME, 's-image')
                    img_url = img_url_container.get_attribute("src")
                    title_item = item.find_element(By.CSS_SELECTOR, "h2").text
                    price_item = item.find_element(By.CLASS_NAME, 'a-price-whole').text
                    price_fraction = item.find_element(By.CLASS_NAME, 'a-price-fraction').text
                    price_total = f'{price_item},{price_fraction}'
                    url_item = item.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
                    parsed_url = urlparse(url_item)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                    base_url = url_item.rsplit('/', 1)[0]
                    urls_now.append(base_url)
                    if base_url in urls_json:
                        for pdr in product['products']:
                            if pdr['url'] == base_url:
                                if price_item != pdr['price']:
                                    print(f"O preço mudou de {pdr['price']} para {price_item}")
                                    prices_total = []
                                    data_total = []
                                    for data in pdr['price_updates']:
                                        data_total.append(data['date'])
                                        prices_total.append(data['price'])
                                    total_dates = len(data_total)
                                    numeric_prices = [float(price) for price in prices_total]
                                    average_price = sum(numeric_prices) / len(numeric_prices) if numeric_prices else 0
                                    price_now = float(price_item)
                                    low_price = average_price - average_price * 0.25
                                    if price_now < low_price and total_dates > 5:
                                        send_telegram_message(pdr['name'], price_total, pdr['url'], img_url)
                                    pdr['price'] = price_item
                                    update_entry = {
                                        "date": time.strftime("%d/%m/%Y"),
                                        "price": f"{price_item}"
                                    }
                                    pdr['price_updates'].append(update_entry)
                                    with open(r"C:\Users\admin\PycharmProjects\pythonProject\scraping\amazon.json", "w",encoding='utf-8') as json_file:
                                        json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
                                else:
                                    pass
                    else:
                        print(title_item)
                        random_id = generate_random_id()
                        product['products'].append({
                            "id": random_id,
                            "name": title_item,
                            "price": price_item,
                            "url": base_url,
                            "price_updates": [{"date": save_date, "price": price_item}]
                        })
                        urls_json.append(base_url)
                except:
                    pass

            try:
                next_button = driver.find_element(By.CLASS_NAME, 's-pagination-next')
                if 's-pagination-disabled' in next_button.get_attribute('class'):
                    break
                else:
                    # Indo para próxima pag
                    next_btn = driver.find_element(By.CSS_SELECTOR, ".s-pagination-next")
                    next_btn.click()
                    time.sleep(3)
            except:
                break

        with open(r"C:\Users\admin\PycharmProjects\pythonProject\scraping\amazon.json", "w", encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

    driver.quit()