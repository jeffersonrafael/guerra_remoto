import requests
from bs4 import BeautifulSoup as bs
from pandas import DataFrame, set_option, merge
set_option('max_columns', None)

def criar_tabela(tr_inicio, tr_fim):
    """
    tr_inicio: valor do 1º tr da tabela
    tr_fim: valor do último tr da tabela
    """
    tabela = {'Guerra':[], 'Mortes':[], 'Ano':[], 'Localizacao':[], 'Notas':[]}
    for i in range(tr_inicio, tr_fim+1): # Os tr's são linhas

        for j in range(0, 5): # Os th's são colunas
            elemento = pagina.find_all("tr")[i].find_all("td")[j].text
            if j == 0: tabela['Guerra'].append(elemento)
            if j == 1: tabela['Mortes'].append(elemento)
            if j == 2: tabela['Ano'].append(elemento)
            if j == 3: tabela['Localizacao'].append(elemento)
            if j == 4: tabela['Notas'].append(elemento)
    return tabela



url = 'https://pt.wikipedia.org/wiki/Lista_de_guerras_por_n%C3%BAmero_de_mortos'

solicitacao = requests.get(url).content

# print(solicitacao.status_code)


pagina = bs(solicitacao, 'html.parser')

# print(pagina.prettify())

# 1) Buscando as tags tr
# Anotações: As tabelas >10 milhões de mortes e >1 milhão de mortes,
# começam nas tags <tr> nº 3 e 14, respectivamente. E cada um possui 11 e 20 tr's, respectivamente

# tabela = pagina.find_all("tr")[10].find_all("td")[4].text
# print(tabela)
# tabela = pagina.find_all("tr")
# for num, cont in enumerate(tabela):
#     print(f'{cont.text}\n')


dados1 = DataFrame(criar_tabela(2, 11), columns=['Guerra', 'Mortes', 'Ano', 'Localizacao', 'Notas'])
dados2 = DataFrame(criar_tabela(13, 31), columns=['Guerra', 'Mortes', 'Ano', 'Localizacao', 'Notas'])

# 2) fazer o merge entre os dados
dados = merge(dados1, dados2, how = 'outer') # Isso aqui faz a UNIÃO entre os dadaframes ou junta um debaixo do outro.
# print(dados)

# 3) Transformar num arquivo .csv
dados.to_csv('guerra_numero_mortos.csv')