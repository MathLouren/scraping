from amazon import amz
from kabum import kabum
from Terabyte import main


try:
    print('Kabum')
    kabum()
except Exception as e:
    print(f'ALGUM ERRO OCORREU NO SCRAPING DA KABUM: {e}')

try:
    print('Amazon')
    amz()
except Exception as e:
    print(f'ALGUM ERRO OCORREU NO SCRAPING DA AMAZON: {e}')

try:
    print('Terabyte')
    main()
except Exception as e:
    print(f'ALGUM ERRO OCORREU NO SCRAPING DA TERABYTE: {e}')