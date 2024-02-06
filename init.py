import schedule
import time
import json
from amazon.amz import verif_items

def amazon():
    print("Verificando itens na Amazon...")
    while True:
        try:
            verif_items()
            break  # Se a função foi executada com sucesso, saia do loop
        except json.JSONDecodeError:
            print("Erro no JSON. Parando o programa.")
            break
        except Exception as e:
            print(f"Ocorreu um erro: {e}. Tentando novamente em 40 minutos...")
            time.sleep(2400)  # Espera 40 minutos antes de tentar novamente
    print("Fim do scraping da Amazon")

schedule.every(40).minutes.do(amazon)

# O loop abaixo mantém o programa em execução para verificar se as tarefas agendadas devem ser executadas
while True:
    schedule.run_pending()
    time.sleep(1)