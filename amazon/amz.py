import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import uuid



def generate_random_id():
    return str(uuid.uuid4())

def create_items():
    url = "https://www.amazon.com.br/s?k=ps5&i=videogames&rh=n%3A7791985011%2Cp_89%3APlayStation%2Cp_n_condition-type%3A13862762011&dc&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2W0RK2D2RX4ID&qid=1703759679&rnid=13862761011&sprefix=ps%2Caps%2C170&ref=sr_pg_1"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(2)
    driver.refresh()
    time.sleep(2)

    try:
        title = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[1]/h1').text
    except:
        title = driver.find_element(By.CSS_SELECTOR, 'span .a-color-state.a-text-bold').text

    # Carregar dados existentes do arquivo JSON
    try:
        with open("amazon.json", "r", encoding='utf-8') as json_file:
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
        with open("amazon.json", "w", encoding='utf-8') as json_file:
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
        with open("amazon.json", "r", encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
            for product in existing_data:
                for pdr in product.get('products', []):
                    url = pdr.get('url')
                    if url:
                        urls_json.append(url)
    except FileNotFoundError:
        print("Arquivo JSON não encontrado.")

    # Configuração do Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)

    itens = driver.find_elements(By.CSS_SELECTOR, '[data-asin]')

    for product in existing_data:
        driver.get(product['url'])
        time.sleep(5)
        driver.refresh()
        time.sleep(1)
        while True:
            itens = driver.find_elements(By.CSS_SELECTOR, '[data-asin]')
            save_date = time.strftime("%d/%m/%Y")
            index_item = 0
            for item in itens:
                index_item += 1
                try:
                    title_item = item.find_element(By.CSS_SELECTOR, "h2").text
                    price_item = item.find_element(By.CLASS_NAME, 'a-price-whole').text
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
                                    pdr['price'] = price_item
                                    update_entry = {
                                        "date": time.strftime("%d/%m/%Y"),
                                        "price": f"{price_item}"
                                    }
                                    pdr['price_updates'].append(update_entry)

                                    with open("amazon.json", "w", encoding='utf-8') as json_file:
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
                    time.sleep(5)
            except:
                break

        with open("amazon.json", "w", encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

    driver.quit()

# url_new = []
#
# def new_items():
#     with open("amazon.json", "r", encoding='utf-8') as json_file:
#         existing_data = json.load(json_file)
#         for product in existing_data:
#             for pdr in product.get('products', []):
#                 url = pdr.get('url')
#                 if url:
#                     url_new.append(url)
#
#     for it in url_new:
#         print(it)
#
#
#
#
# new_items()

verif_items()