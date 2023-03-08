# %% Importing dependencies
import requests
import json

# %%
url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
r = requests.get(url)

'''
Tipos de requisições:
- GET - consultar uma informação (ex. dados de clima)
- POST - passar uma informação (ex. guardar dados em um banco)
- PUT - alterar uma informação (ex. atualizar dados cadastrais)
'''
# %% Visualizar código de status
print(r.status_code)
'''
Códigos de status:
- 1XX - informação
- 2XX - sucesso
- 3XX - redirecionar
- 4XX - erro de cliente (você cometeu um erro)
- 5XX - erro de servidos (eles cometeram um erro)
'''

# %% Visualizar dados em formato de texto
if r:
    print(r.text)
else:
    print('Falhou')
# %%
dolar = json.loads(r.text)['USDBRL']

# %% Output
print(f"20 dólares hoje custam R$ {float(dolar['bid'])*20}")

# %% Transformando tudo acima em uma função

def cotacao(valor, moeda):
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}"
    r = requests.get(url)
    dolar = json.loads(r.text)[moeda.replace('-', '')]
    print(f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")
# %%
cotacao(20,'USD-BRL')
# %%Fluxo de tratamento de erro pontual - olhando pra uma linha/lógica
try:
    cotacao(20, 'Luan')
except Exception as e:
    print(e)
else:
    print("ok")
# %%Podemos usar a mesma lógica pra uma função
def multi_moeda(valor):
    lst_currency = [
        'USD-BRL',
        'EUR-BRL',
        'BTC-BRL',
        'R9L-BRL', #essa é a errada
        'JPY-BRL'
    ]
    for moeda in lst_currency:
        try:
            url = f"https://economia.awesomeapi.com.br/json/last/{moeda}"
            r = requests.get(url)
            dolar = json.loads(r.text)[moeda.replace('-', '')]
            print(f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")
        except:
            print(f"Erro na moeda {moeda}")
# %%
multi_moeda(20)
# %%Usando um decorador
def error_check(func):
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except:
            print(f"{func.__name__} falhou")
    return inner_func

@error_check
def cotacao_dec(valor, moeda):
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}"
    r = requests.get(url)
    dolar = json.loads(r.text)[moeda.replace('-', '')]
    print(f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")

# %%
cotacao_dec(20, 'USD-BRL')
cotacao_dec(20, 'EUR-BRL')
cotacao_dec(20, 'BTC-BRL')
cotacao_dec(20, 'R9L-BRL')
cotacao_dec(20, 'JPY-BRL')
# %%Usando o pacote backoff
import backoff
import random

# %%
@backoff.on_exception(
    backoff.expo, 
    (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), 
    max_tries=5)
def test_func(*args, **kargs):
    rnd = random.random()
    print(f'''
        RND: {rnd}
        args: {args if args else 'sem args'}
        kargs: {kargs if kargs else 'sem kargs'}
    ''')
    if rnd < .2:
        raise ConnectionAbortedError('Conexão foi finalizada')
    elif rnd < .4:
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        raise TimeoutError('Tempo de espera excedido')
    else:
        return 'Ok!'
# %%
test_func()
# %%
test_func(42)
# %%
test_func(42, 51, nome='Luan')

# %%
import logging

# %%
log = logging.getLogger()
log.setLevel(logging.DEBUG) #NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)
# %%
@backoff.on_exception(
    backoff.expo, 
    (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), 
    max_tries=5)
def test_func(*args, **kargs):
    rnd = random.random()
    log.debug(f"RND: {rnd}")
    log.info(f"args: {args if args else 'sem args'}")   
    log.info(f"kargs: {kargs if kargs else 'sem kargs'}")
    if rnd < .2:
        log.error('Conexão foi finalizada')
        raise ConnectionAbortedError('Conexão foi finalizada')
    elif rnd < .4:
        log.error('Conexão foi recusada')
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        log.error('Tempo de espera excedido')
        raise TimeoutError('Tempo de espera excedido')
    else:
        return 'Ok!'
# %%
test_func()
# %%
