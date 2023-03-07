import requests
import pandas as pd
import collections

url = "https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados?modalidade=Lotofácil"
#url = sys.argv[1]

r = requests.get(url, verify=False)

#Tratando elementos HTML da resposta do request
r_text = r.text.replace('\\r\\n', '').replace('"\r\n}', '').replace('{\r\n  "html": "', '')

#Lendo HTML usando Pandas
df = pd.read_html(r_text)

type(df) #lista
type(df[0]) #dataframe

#Fazendo backup da lista original
df_backup = df.copy()

#Pegando dataframe de interesse
df = df[0].copy()

#Removendo linhas nulas usando o fato de que NaN == NaN é sempre falso
df = df[df['Bola1'] == df['Bola1']]

#print(df)

#Definindo listas de números
nr_pop = list(range(0,26))
nr_pares = [i*2 for i in range(1,13)]
nr_impares = [i*2-1 for i in range(1,14)]
nr_primos = [2, 3, 5, 7, 11, 13, 17, 19, 23]

#Variáveis
comb = [] #combinações de pares, ímpares e primos
numbers = {} #key = número sorteado : value = quantidade de vezes que apareceu

lst_campos = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5',
              'Bola6', 'Bola7', 'Bola8', 'Bola9', 'Bola10', 'Bola11', 'Bola12',
              'Bola13', 'Bola14', 'Bola15']

for index, row in df.iterrows():
    v_pares = 0
    v_impares = 0
    v_primos = 0
    for campo in lst_campos:
        if row[campo] in nr_pares:
            v_pares += 1
        if row[campo] in nr_impares:
            v_impares += 1
        if row[campo] in nr_primos:
            v_primos += 1
        if row[campo] in numbers:
            numbers[row[campo]] += 1
        if row[campo] not in numbers:
            numbers[row[campo]] = 1
    comb.append(str(v_pares) + 'p-' + str(v_impares) + 'i-' + str(v_primos) + 'np')

#Sorted list do nosso dict numbers
numbers_sorted = sorted(numbers.items(), key=lambda x: x[1])

#Analisando as combinações de pares, ímpares e primos
counter = collections.Counter(comb)
resultado = pd.DataFrame(counter.items(), columns=['Combinação', 'Frequência'])
resultado['p_freq'] = resultado['Frequência']/resultado['Frequência'].sum()
resultado = resultado.sort_values(by='p_freq')

print(f'''---------------- Loto Fácil ----------------

O número mais frequente é o: {int(numbers_sorted[-1][0])}
O número menos frequente é o: {int(numbers_sorted[0][0])}
A combinação de pares, ímpares e primos mais frequente é {resultado['Combinação'].values[-1]} com a frequência de {round(resultado['p_freq'].values[-1],4)*100}%

''')