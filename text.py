import time

from seleniumwire import webdriver

options = {
    'proxy': {
        'http': 'http://5dab7c172c70a8eb:RNW78Fm5@185.130.105.109:10000',
        'https': 'https://5dab7c172c70a8eb:RNW78Fm5@185.130.105.109:10000',
        'no_proxy': 'localhost,127.0.0.1'
    }
}

driver = webdriver.Chrome(seleniumwire_options=options)

# Agora você pode usar o driver para navegar, por exemplo:
driver.get('https://www.kabum.com.br/')

time.sleep(22000)





#0e363224bf31056c
#RNW78Fm5



# Endereço IP	201.1.202.30
# Reverso	201-1-202-30.dsl.telesp.net.br
# Navegador	Chrome
# Plataforma	Win10
# Proxy	Não detectado
# País	Brazil (flag) - Info da CIA
# Cidade	Sao Paulo - ver no mapa