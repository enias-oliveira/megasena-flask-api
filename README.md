# Sobre
Ester README tem por objetivo fornecer as informações necessárias para instalação e execução da API desenvolvida para o teste backend python para ioasys.

#  Instalação

## Dependências

Esse projeto foi desenvolvido com [Poetry](https://python-poetry.org/), uma alternativa ao Pip para gestão de dependencias. 
 
Dito isso, o arquivo "requirements.txt" dá suporte para o uso do Pip.

### Passo-a-passo para instalação com Pip

*Na linha de comando, usando Bash:*
- 1. Criar um ambiente virtual usando venv : `python -m venv venv`
- 2. Entrar no ambiente virtual: `source venv/bin/activate`
- 3 . Instalar todas as dependencias: `pip install -r requirements.txt`

### Passo-a-passo para instalação com Poetry

*Na linha de comando, usando Bash:*
- 1. Entrar no ambiente virtual: `poetry shell`
- 2. Instalar todas dependencias: `poetry install`


## Banco de Dados

A API salva usuários e megasenas em um banco de dados PostgreSQL atráves do SQLAlchemy.
É necessário criar um Banco de dados local sem nenhuma configuração ou tabela.

## Variaveis de ambiente

Esse projeto necessita de váriaveis de ambiente para ter um contexto de execução e fazer conexão com o Banco de Dados local. 

O arquivo ".env.example" é para ser usado como base para criar o seu próprio arquivo ".env". Segue uma explicação de todas variáveis de ambiente e sua funcionalidade.

*Copie o arquivo .env.example para .env e abra em seu editor e mude as váriaveis em chaves {}:*
```
FLASK_ENV=development # Contexto de execução, precisa ser alterada para "test" quando executar os testes
FLASK_APP=src.app:create_app # Caminho para função "Factory" da aplicação flask
FLASK_RUN_PORT=5001 # Porta em que o servidor estará escutando por requisições
DEBUG=True # Mostrar informações de erro para o cliente (navegador ou Postman)

SECRET_KEY=ioasys # Chave secreta para geração de JWT

DB_USERNAME={username} # Nome do usuário dono do banco de dados local
DB_PASSWORD={password} # Senha do usuário ...
DB_HOST={host} # Host do servidor do banco de dados, geralmente localhost ou http://127.0.0.1 resolve
DB_NAME_DEV={db_name} # Nome do banco de dados local
```


## Configurando o Banco de Dados com Migration

Utilizaremos Migration para que o banco de dados local esteja funcionado como esperado.

*Na linha de comando, usando Bash:*
`flask db upgrade`


## Inicializando o servidor Flask

Feito todos os passos acima, o servidor deve funcionar correntament.

*Na linha de comando, usando Bash:*
`flask run`


