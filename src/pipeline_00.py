"""
Aqui são definidas as funções que devem fazer Extract, Transform e Load dos dados
"""
import time
import requests
from datetime import datetime
from tinydb import TinyDB

def extract_bitcoin_data():
    # endpoint
    url = "https://api.coinbase.com/v2/prices/spot"

    response = requests.get(url)
    dados = response.json() # converte pra uma lista de dicionários
    return dados['data']

def transform_bitcoin_data(data):
    value = data['amount']
    cripto = data['base']
    currency = data['currency']
    timestamp = datetime.now().timestamp()

    transformed_data = {
        "valor": value,
        "criptomoeda": cripto,
        "moeda": currency,
        "timestamp": timestamp
    }

    return transformed_data

# pra salvar os dados obtidos da API em json
def save_data_tinydb(data, db_name='bitcoin.json'):
    # tinydb cria um arquivo local chamando bitcoin.json como banco de dados
    db = TinyDB(db_name)
    db.insert(data)
    print('Dados foram salvos com sucesso!')



if __name__ == "__main__":
    while True: # roda periodicamente a cada 15 segundos para coletar dados
        data_json = extract_bitcoin_data()
        data_treated = transform_bitcoin_data(data_json)
        print(data_treated)
        save_data_tinydb(data_treated)
        time.sleep(15)