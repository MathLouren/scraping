import schedule
import time
from amazon.amz import verif_items

def amazon():
    print("Verificando itens na Amazon...")
    try:
        verif_items()
    except:
        verif_items()
    print("Fim do scraping da Amazon")

schedule.every(40).minutes.do(amazon)

# O loop abaixo mantém o programa em execução para verificar se as tarefas agendadas devem ser executadas
while True:
    schedule.run_pending()
    time.sleep(1)
