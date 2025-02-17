import schedule
import time
import json
from amazon.amz import verif_items

def amazon():
    print("Verificando itens na Amazon...")
    while True:
        try:
            verif_items()
            break  
        except json.JSONDecodeError:
            print("Erro no JSON. Parando o programa.")
            break
        except Exception as e:
            print(f"Ocorreu um erro: {e}. Tentando novamente em 40 minutos...")
            time.sleep(2400)  
    print("Fim do scraping da Amazon")

schedule.every(40).minutes.do(amazon)
while True:
    schedule.run_pending()
    time.sleep(1)
