# ETL-API-coinbase
Este é um projeto feito em Python para treinar ETL básico usando dados de criptomoeda (bitcoin).
A API da coinbase é usada para obter dados da cotação do bitcoin a cada 15 segundos. Um banco PostgreSQL foi hospedado no Render e o próprio código foi deployado lá também, já o dashboard (visualização de dados) foi feito usando a lib StreamLit.
Também foi usada a lib Logfire para observabilidade simples das requisições e operações no banco postgre (das libs requests e SQLAlchemy respectivamente). Logs disponíveis em: https://logfire.pydantic.dev/palomiaw/etl-api-coinbase

Resultado dos dados no banco PostgreSQL no client local PgAdmin:

![image](https://github.com/user-attachments/assets/2abc992c-b89a-4023-ad58-0a8f1a1c6a7b)

Resultado final do dashboard:

![dash](https://github.com/user-attachments/assets/e9b7dad2-6844-45f5-b7bb-8c34da868f41)
