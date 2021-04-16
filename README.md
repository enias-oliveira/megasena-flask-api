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

Também é preciso de um Banco de dados local separado para os testes.

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
DB_NAME_TEST={test_db_name} # Nome do banco de dados local para teste
```


## Configurando o Banco de Dados com Migration

Utilizaremos Migration para que o banco de dados local esteja funcionado como esperado.

*Na linha de comando, usando Bash:*
`flask db upgrade`


## Inicializando o servidor Flask

Feito todos os passos acima, o servidor deve funcionar correntament.

*Na linha de comando, usando Bash:*
`flask run`


##  Postman e Variáveis

A collection de requisições estão configuradas de tal forma que algumas rotas usam token de acesso de 2 usuários: user_ioasys e user_megasena.

Para poder fazer todas as requisições, é recomendado criar esses 2 usúarios primeiro antes de executar as outras requisições. 

*Ou simplesmente criar os usuários e manualmente pegar o token de acesso a partir do login para as outras requisições.* 


## Endpoints

Segue uma lista de todos os endpoints com exemplos de requisições e respostas.

### Users

- Criação de usuário
``` http
POST: api/users/signup
Token : No
body : {
	"name" : "ioasys",
	"email": "ioasys@mail.com",
	"password" : "b4ckEnd"
}

Response: {
    "id" : 1,
    "name" : "ioasys",
    "email" : "ioasys@mail.com"
}
```

- Logar usúario
``` http
POST: api/users/login
Token : No
body : {
	"email": "ioasys@mail.com",
	"password" : "b4ckEnd"
}

Response: {
"user_id" : 1,
"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxODU1ODg1NiwianRpIjoiZDI4YWY5ZGUtZjZlOS00MGRkLWFlNGQtMjE3NTY4MzJkMjE0IiwibmJmIjoxNjE4NTU4ODU2LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJleHAiOjE2MTkxNjM2NTZ9.Nfa5CMv3tOWT3S_zIJk59OXZ07uB5afUiiiPZW6e7E4"}
```

- Editar nome do usuário
``` http
PATCH: api/users/{user_id}:1
Token : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxODU1ODg1NiwianRpIjoiZDI4YWY5ZGUtZjZlOS00MGRkLWFlNGQtMjE3NTY4MzJkMjE0IiwibmJmIjoxNjE4NTU4ODU2LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJleHAiOjE2MTkxNjM2NTZ9.Nfa5CMv3tOWT3S_zIJk59OXZ07uB5afUiiiPZW6e7E4
body : {
    "name" : "Python"
}

Response: NO CONTENT, 204
```

- Editar email do usuário
``` http
PATCH: api/users/{user_id}:1
Token : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxODU1ODg1NiwianRpIjoiZDI4YWY5ZGUtZjZlOS00MGRkLWFlNGQtMjE3NTY4MzJkMjE0IiwibmJmIjoxNjE4NTU4ODU2LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJleHAiOjE2MTkxNjM2NTZ9.Nfa5CMv3tOWT3S_zIJk59OXZ07uB5afUiiiPZW6e7E4
body : {
    "email" : "python@mail.com"
}

Response: NO CONTENT, 204
```

- Editar senha do usuário
``` http
PATCH: api/users/{user_id}:1
Token : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxODU1ODg1NiwianRpIjoiZDI4YWY5ZGUtZjZlOS00MGRkLWFlNGQtMjE3NTY4MzJkMjE0IiwibmJmIjoxNjE4NTU4ODU2LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJleHAiOjE2MTkxNjM2NTZ9.Nfa5CMv3tOWT3S_zIJk59OXZ07uB5afUiiiPZW6e7E4
body : {
    "password" : "PythonNoobMaster"
}

Response: NO CONTENT, 204
```

- Editar todos os dados do usuário
``` http
PUT: api/users/{user_id}:1
Token : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxODU1ODg1NiwianRpIjoiZDI4YWY5ZGUtZjZlOS00MGRkLWFlNGQtMjE3NTY4MzJkMjE0IiwibmJmIjoxNjE4NTU4ODU2LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJleHAiOjE2MTkxNjM2NTZ9.Nfa5CMv3tOWT3S_zIJk59OXZ07uB5afUiiiPZW6e7E4
body : {
	"name" : "Potato",
	"password" : "BigPotato",
	"email" : "potato@mail.com"
}

Response: NO CONTENT, 204
```

- Deletar usuário
``` http
DELETE: api/users/{user_id}:1
Token : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxODU1ODg1NiwianRpIjoiZDI4YWY5ZGUtZjZlOS00MGRkLWFlNGQtMjE3NTY4MzJkMjE0IiwibmJmIjoxNjE4NTU4ODU2LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJleHAiOjE2MTkxNjM2NTZ9.Nfa5CMv3tOWT3S_zIJk59OXZ07uB5afUiiiPZW6e7E4
body : No

Response: NO CONTENT, 204
```


### Megasena

- Criar novo jogo
``` http
POST: api/megasenas
Token : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxODUyMTU1MiwianRpIjoiMmI5OTM5ZTEtZDkzMS00ZTMzLWE1NGItNDY4OTM3YzBjNmNlIiwibmJmIjoxNjE4NTIxNTUyLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoyLCJleHAiOjE2MTkxMjYzNTJ9.tFTmEjcBe63arR-6ZJQggZk8Cy-Z7wKIdlhgHtGrPys
body : {
	"numbers": 8,
}

Response: {
 "megasena_ticket_id": 3,
    "ticket_numbers": [
        11,
        7,
        24,
        8,
        15,
        12,
        2,
        51
    ]
} 
```


- Listar jogos do usuário
``` http
GET: api/megasenas
Token : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxODUyMTU1MiwianRpIjoiMmI5OTM5ZTEtZDkzMS00ZTMzLWE1NGItNDY4OTM3YzBjNmNlIiwibmJmIjoxNjE4NTIxNTUyLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoyLCJleHAiOjE2MTkxMjYzNTJ9.tFTmEjcBe63arR-6ZJQggZk8Cy-Z7wKIdlhgHtGrPys
body : No
Response: {
    "user_id": 2,
    "megasena_tickets": [
        {
            "megasena_ticket_id": 3,
            "ticket_numbers": [
                11,
                7,
                24,
                8,
                15,
                12,
                2,
                51
            ]
        },
        {
            "megasena_ticket_id": 2,
            "ticket_numbers": [
                29,
                9,
                27,
                37,
                55,
                49,
                29,
                38,
                11,
                5
            ]
        }
    ]
}
```


- Números sorteados no último sorteio da Megasena
``` http
GET: api/megasenas/draws
Token : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxODUyMTU1MiwianRpIjoiMmI5OTM5ZTEtZDkzMS00ZTMzLWE1NGItNDY4OTM3YzBjNmNlIiwibmJmIjoxNjE4NTIxNTUyLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoyLCJleHAiOjE2MTkxMjYzNTJ9.tFTmEjcBe63arR-6ZJQggZk8Cy-Z7wKIdlhgHtGrPys
body : No
Response: {
    "latest_draw": [
        3,
        20,
        22,
        32,
        35,
        50
    ]
}
```


- Resultados do último jogo do usuário
``` http
GET: api/megasenas/results
Token : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxODUyMTU1MiwianRpIjoiMmI5OTM5ZTEtZDkzMS00ZTMzLWE1NGItNDY4OTM3YzBjNmNlIiwibmJmIjoxNjE4NTIxNTUyLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoyLCJleHAiOjE2MTkxMjYzNTJ9.tFTmEjcBe63arR-6ZJQggZk8Cy-Z7wKIdlhgHtGrPys
body : No
Response: {
    "user_id": 2,
    "last_ticket": {
        "ticket_id": 5,
        "ticket_numbers": [
            56,
            55,
            21,
            55,
            42,
            22,
            41,
            47
        ]
    },
    "last_megasena_draw": [
        3,
        20,
        22,
        32,
        35,
        50
    ],
    "correct_count": 1,
    "correct_numbers": [
        22
    ]
}
```


## Testes

Para executar os testes, é preciso alter duas variáveis de ambientes no arquivo ".env".

``` 
FLASK_ENV=test # Para que o flask use a configuração de testes
DB_NAME_TEST={test_db_name} # Para usar o banco de dados teste
```

Feitos os ajustes é só rodar os testes usando o pytest do ambiente virtual.

*Na linha de comando, usando Bash:*
`python -m pytest`


