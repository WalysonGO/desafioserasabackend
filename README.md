# Debt Management API

Esta aplicação foi desenvolvida para gerenciar dívidas pessoais, utilizando **FastAPI** e seguindo boas práticas de **Clean Code** e **Design Patterns**. A API oferece suporte a autenticação JWT, registro de usuários, cadastro, edição e exclusão de dívidas, além de fornecer um resumo financeiro.

## Tecnologias Usadas

- **FastAPI**: Framework principal para a API.
- **SQLAlchemy**: ORM para gerenciar o banco de dados.
- **PostgreSQL**: Banco de dados relacional utilizado no projeto.
- **python-dotenv**: Gerenciamento de variáveis de ambiente.
- **Passlib**: Para hashing de senhas.
- **Python-Jose**: Para geração e validação de tokens JWT.
- **Docker** e **Docker Compose**: Configuração do banco de dados PostgreSQL e Adminer.

## Estrutura do Projeto

```
.
├── alembic.ini
├── app
│   ├── controllers
│   │   ├── debt_controller.py
│   │   └── user_controller.py
│   ├── database.py
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── debt.py
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas.py
│   ├── services
│   │   ├── auth_service.py
│   │   ├── debt_service.py
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── utils
│       ├── env_loader.py
│       ├── __init__.py
│       └── jwt_handler.py
├── docker-compose.yml
├── Dockerfile
├── insomnia_doc.json
├── migrations
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       └── 345e5fd4f6ac_initial_migration.py
├── README.md
└── requirements.txt

```

## Variáveis do `.env`

### Variáveis relacionadas ao banco de dados

- **`DATABASE_URL`**: URL de conexão do banco de dados. Exemplo:
  ```
  postgresql://DB_USER:DB_PASS@localhost:5432/DB_NAME
  ```

- **`DB_USER`**: Nome do usuário para acessar o banco de dados.
- **`DB_PASS`**: Senha do usuário do banco de dados.
- **`DB_NAME`**: Nome do banco de dados.

### Variáveis relacionadas à aplicação

- **`SECRET_KEY`**: Chave usada para assinar os tokens JWT.

## Pacotes Instalados

### Dependências principais

- **`fastapi`**: Framework principal para a API.
- **`sqlalchemy`**: ORM para lidar com o banco de dados.
- **`psycopg2-binary`**: Driver para integração com PostgreSQL.
- **`python-dotenv`**: Gerenciamento de variáveis de ambiente.
- **`passlib`**: Utilitário para hashing seguro de senhas.
- **`python-jose`**: Para geração e validação de tokens JWT.
- **`pydantic`**: Para validação e serialização de dados.

### Ferramentas de desenvolvimento

- **`uvicorn`**: Servidor ASGI para rodar o FastAPI.

## Configuração do Ambiente Virtual

1. **Criação do Ambiente Virtual**:
   ```bash
   python -m venv venv
   ```

2. **Ativação do Ambiente Virtual**:
   - Windows:
     ```bash
     venv\\Scripts\\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Instalação das Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuração do Banco de Dados**:
   - Inicie o Docker:
     ```bash
     docker-compose up -d --build
     ```

5. **Criação do Arquivo `.env`**:
   Crie um arquivo `.env` no diretório raiz com o seguinte conteúdo:
   ```dotenv
   # Application Configuration
   DATABASE_URL=postgresql://DB_USER:DB_PASS@localhost:5432/DB_NAME
   SECRET_KEY=your-secret-key

   # Database Configuration
   DB_USER=user
   DB_PASS=password
   DB_NAME=debts_db

   # Redis
   REDIS_HOST=redis
   REDIS_PORT=6379
   ```

6. **Inicie o Servidor**:
Após configurar o `.env`, você pode iniciar o servidor, mas ele já está está ativo na rota: http://localhost:8000:

Se quiser rodar sem se pelo Container Docker, rode o comando:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8009 --reload
```

## Funcionalidades

### Usuários

- **Registrar Usuário**: Rota `POST /users/`
- **Login**: Rota `POST /users/login`
- **Perfil**: Rota `GET /users/me`

### Dívidas

- **Adicionar Dívida**: Rota `POST /debts/`
- **Listar Dívidas**: Rota `GET /debts/`
- **Editar Dívida**: Rota `PUT /debts/{debt_id}`
- **Remover Dívida**: Rota `DELETE /debts/{debt_id}`
- **Resumo Financeiro**: Rota `GET /debts/summary`

## Resumo Financeiro

A rota `GET /debts/summary` exibe as seguintes informações:

- Total de Dívidas Cadastradas.
- Valor Total das Dívidas Pendentes.
- Quantidade de Dívidas Pagas.
- Quantidade de Dívidas Atrasadas.
- Valor Total das Dívidas Pagas.
- Valor Total das Dívidas Atrasadas.
- Valor Médio das Dívidas.
- Percentual de Dívidas Pagas, Pendentes e Atrasadas.

### Estrutura do Retorno

O retorno da rota será um objeto JSON com a seguinte estrutura:

```json
{
    "total_debts": 10,
    "total_overdue": 2,
    "total_pending": 5,
    "total_paid": 3,
    "percentage_paid": 0.3,
    "percentage_pending": 0.5,
    "percentage_overdue": 0.2,
    "total_debt_value": 1000.00,
    "total_pending_value": 500.00,
    "total_paid_value": 300.00,
    "total_overdue_value": 200.00,
    "average_debt_value": 100.00
}
```

### Descrição dos Campos

- **total_debts**: Total de dívidas cadastradas.
- **total_overdue**: Total de dívidas atrasadas.
- **total_pending**: Total de dívidas pendentes.
- **total_paid**: Total de dívidas pagas.
- **percentage_paid**, **percentage_pending**, e **percentage_overdue**: Percentuais correspondentes em relação ao total cadastrado.
- Valores totais e médios das dívidas.