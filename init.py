import schedule
import time
from amazon.amz import verif_items
from kabum.kabum import init_check

def amazon():
    print("Verificando itens na Amazon...")
    verif_items()

def kabum():
    init_check()

schedule.every(30).minutes.do(amazon)
schedule.every(120).minutes.do(kabum)

# O loop abaixo mantém o programa em execução para verificar se as tarefas agendadas devem ser executadas
while True:
    schedule.run_pending()
    time.sleep(1)
