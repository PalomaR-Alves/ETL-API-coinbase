from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Float, String, Integer, DateTime
from datetime import datetime

# classe Base no sqlalchemy
Base = declarative_base()

# criamos a classe BitcoinPreco herdando da classe Base. Toda classe criada possuindo herança
# com a Base será mapeada para uma nova tabela no banco de dados, e os atributos dessa classe
# são mapeados para colunas. 
# Cada novo objeto será uma nova linha na tabela.
class BitcoinPreco(Base):
    __tablename__ = "bitcoin_preco"
    # define a tabela no banco de dados - postgre
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float, nullable=False)
    criptomoeda = Column(String(50), nullable=False)
    moeda = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)