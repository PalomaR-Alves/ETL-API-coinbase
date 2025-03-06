import os
import time
import requests
import logfire
import logging
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, BitcoinPreco
from logging import basicConfig, getLogger

# configuração do logfire
logfire.configure() # config padrão do logfire
basicConfig(handlers=[logfire.LogfireLoggingHandler()]) # define como handler o do logfire
logger = getLogger(__name__) # cria um obj Logger associado ao nome do modulo atual (pipeline)
logger.setLevel(logging.INFO) # define o nível do log pra INFO, mas ele tbm pode gerar msgs mais críticas
logfire.instrument_requests() # integra o logfire com a lib requests, assim as requests vão ser monitoradas
logfire.instrument_sqlalchemy() # integra também com a sqlalchemy, assim as operações de banco tbm são monitoradas


# carregar variáveis de ambiente do .env
load_dotenv()

# ler as vars do .env
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

# com as vars ambiente concatenadas obtemos a URL do banco
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# representa a conexão com o banco de dados. Também é possível usar comandos SQL
# diretamente no banco através dele
engine = create_engine(DATABASE_URL)
# a session gerencia a comunicação entre o código e o banco. Permite modificar/excluir/adicionar
# registros (linhas) de uma forma orientada a objetos, sendo que essas operações são tratadas como
# transações, sendo necessário dar explicitamente comandos de commits ou rollbacks
Session = sessionmaker(bind=engine)



def criar_tabela():
    # para criar as tabelas no banco
    Base.metadata.create_all(engine)
    logger.info('Tabela(s) criada(s) com sucesso!')

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
    timestamp = datetime.now()

    transformed_data = {
        "valor": value,
        "criptomoeda": cripto,
        "moeda": currency,
        "timestamp": timestamp
    }

    return transformed_data

def salvar_dados_postgres(dados):
    session = Session()
    novo_registro = BitcoinPreco(**dados)
    session.add(novo_registro)
    session.commit()
    session.close()
    logger.info(f"{dados['timestamp']} Dados salvos no banco!")



if __name__ == "__main__":
    criar_tabela()
    while True: # roda periodicamente a cada 15 segundos para coletar dados
        data_json = extract_bitcoin_data()
        if data_json:
            data_treated = transform_bitcoin_data(data_json)
            logger.info(data_treated)
            salvar_dados_postgres(data_treated)

        time.sleep(15) # roda a cada 15 segundos