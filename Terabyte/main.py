import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import uuid

def generate_random_id():
    return str(uuid.uuid4())


def create_items():
    names_products = []
    url = "https://www.terabyteshop.com.br/monitores"  # Substitua pela URL real

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome()

    list_urls = []
    list_urls_json = []
    items_add = []


    try:
        # Acesse a página
        driver.get(url)

        time.sleep(5)

        try:
            time.sleep(1)
            close = driver.find_element(By.XPATH, "/html/body/div[7]/div/div/div/button/span")
            close.click()
            time.sleep(3)
        except:
            pass

        try:
            more_products = driver.find_element(By.CSS_SELECTOR, "#pdmore span")
            more_products.click()
        except:
            pass

        try:
            more_products = driver.find_element(By.CSS_SELECTOR, "#pdmore span")
            more_products.click()
        except:
            pass

        # Encontre todas as divs 'prodarea'
        prodarea_divs = driver.find_elements(By.CSS_SELECTOR, "#body .container .produtos-home #prodarea .pbox")

        item_name_element = driver.find_element(By.CSS_SELECTOR, "h1 strong")
        item_name = item_name_element.text

        # Estrutura para armazenar os dados
        result_data = {
            "file_name": item_name,
            "url": url,
            "products": []
        }

        # Carregue os dados existentes do arquivo JSON
        try:
            with open("terabyte.json", "r", encoding='utf-8') as existing_json_file:
                existing_data = json.load(existing_json_file)

            for item in existing_data:
                names_products.append(item["file_name"])
                list_urls_json.append(item["url"])

            # Verifique se o item já foi salvo anteriormente
            if item_name in names_products:
                print(f"O item '{item_name}' já foi salvo anteriormente. Verificando URLs existentes...")
                save_date = time.strftime("%d/%m/%Y")
                for index, prodarea_div in enumerate(prodarea_divs, start=1):
                    a_element = prodarea_div.find_element(By.TAG_NAME, 'a')
                    try:
                        price_element = prodarea_div.find_element(By.CSS_SELECTOR, ".commerce_columns_item_inner .commerce_columns_item_info .prod-new-price span")
                        title = a_element.get_attribute('title')
                        href = a_element.get_attribute('href')
                        price = price_element.text
                        list_urls.append(href)
                    except:
                        break
            else:
                print(f"O item '{item_name}' não foi encontrado nos dados existentes. Adicionando novo item...")
                # Adicione a data de salvamento
                save_date = time.strftime("%d/%m/%Y")
                for index, prodarea_div in enumerate(prodarea_divs, start=1):
                    a_element = prodarea_div.find_element(By.TAG_NAME, 'a')
                    try:
                        price_element = prodarea_div.find_element(By.CSS_SELECTOR,
                                                                  ".commerce_columns_item_inner .commerce_columns_item_info .prod-new-price span")
                        title = a_element.get_attribute('title')
                        href = a_element.get_attribute('href')
                        price = price_element.text

                        # Adicione os dados à estrutura
                        result_data["products"].append({
                            "id": index,
                            "name": title,
                            "price": price,
                            "url": href,
                            "price_updates": [{"date": save_date, "price": price}]
                        })
                    except:
                        continue

                # Salve os dados em um novo arquivo JSON
                with open("terabyte.json", "w", encoding='utf-8') as json_file:
                    existing_data.append(result_data)
                    json.dump(existing_data, json_file, indent=2, ensure_ascii=False)

            with open('terabyte.json', 'r', encoding='utf-8') as f:
                data_all = json.load(f)

        except:
            # Se o arquivo não existir, crie um novo arquivo JSON
            print(f"Arquivo 'terabyte.json' não encontrado. Criando novo arquivo...")
            save_date = time.strftime("%d/%m/%Y")
            for index, prodarea_div in enumerate(prodarea_divs, start=1):
                a_element = prodarea_div.find_element(By.TAG_NAME, 'a')
                try:
                    price_element = prodarea_div.find_element(By.CSS_SELECTOR, ".commerce_columns_item_inner .commerce_columns_item_info .prod-new-price span")
                    title = a_element.get_attribute('title')
                    href = a_element.get_attribute('href')
                    price = price_element.text

                    # Adicione os dados à estrutura
                    result_data["products"].append({
                        "id": index,
                        "name": title,
                        "price": price,
                        "url": href,
                        "price_updates": [{"date": save_date, "price": price}]
                    })

                    # Imprima os resultados
                    print(f"{index}. Title: {title}, Href: {href}, Price: {price}")

                except:
                    continue

            with open("terabyte.json", "w", encoding='utf-8') as json_file:
                json.dump([result_data], json_file, indent=2, ensure_ascii=False)

    finally:
        # Feche o navegador ao final
        driver.quit()



def update_prices():

    urls_ok = []

    def search_items(title, href, price):
        target_file_name = title

        try:
            with open('terabyte.json', 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            for item in data:
                if item.get('file_name') == target_file_name:
                    for product in item.get('products', []):
                        try:
                            if product['url'] == href:
                                saved_price = product['price']
                                current_price = price
                                if current_price:
                                    if saved_price != current_price:
                                            product['price'] = current_price

                                            print(f'{saved_price} + {current_price}')

                                            # Adicione um novo registro de atualização
                                            update_entry = {
                                                "date": time.strftime("%d/%m/%Y"),
                                                "price": f"{current_price}"
                                            }
                                            product['price_updates'].append(update_entry)

                                            print(f"Preço atualizado para: {product['price']}")

                                            # Salve as alterações de volta no arquivo JSON
                                            with open('terabyte.json', 'w', encoding='utf-8') as json_file:
                                                json.dump(data, json_file, indent=2, ensure_ascii=False)
                                    else:
                                        pass
                                else:
                                    pass
                        except KeyError as e:
                            print(f"Chave não encontrada: {e}")

        except Exception as e:
            print(f"Ocorreu um erro ao abrir o arquivo JSON: {e}")

    # def invalid_links():
    #     for product in item.get('products', []):
    #         if product['url'] in urls_ok:
    #             pass
    #         else:
    #             product['price'] = "R$ 0000"
    #             update_entry = {
    #                 "date": time.strftime("%d/%m/%Y"),
    #                 "price": "R$ 0000"
    #             }
    #             product['price_updates'].append(update_entry)
    #
    #             with open('terabyte.json', 'w', encoding='utf-8') as json_file:
    #                 json.dump(data, json_file, indent=2, ensure_ascii=False)
    #             print(product['url'])


    def check_prices(data):
        new_data = data
        title_items = data['file_name']
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(options=chrome_options)

        driver.get(data['url'])

        time.sleep(10)

        try:
            time.sleep(1)
            close = driver.find_element(By.XPATH, "/html/body/div[7]/div/div/div/button/span")
            close.click()
            time.sleep(3)
        except:
            pass

        try:
            more_products = driver.find_element(By.CSS_SELECTOR, "#pdmore span")
            more_products.click()
        except:
            pass

        try:
            more_products = driver.find_element(By.CSS_SELECTOR, "#pdmore span")
            more_products.click()
        except:
            pass


        prodarea_divs = driver.find_elements(By.CSS_SELECTOR, "#body .container .produtos-home #prodarea .pbox")

        save_date = time.strftime("%d/%m/%Y")
        for index, prodarea_div in enumerate(prodarea_divs, start=1):
            a_element = prodarea_div.find_element(By.TAG_NAME, 'a')
            try:
                price_element = prodarea_div.find_element(By.CSS_SELECTOR, ".commerce_columns_item_inner .commerce_columns_item_info .prod-new-price span")
                title = a_element.get_attribute('title')
                href = a_element.get_attribute('href')
                price = price_element.text
                search_items(title_items, href, price)
            except:
                break




    with open('terabyte.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        check_prices(item)

update_prices()