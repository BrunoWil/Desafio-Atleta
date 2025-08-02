# Workout API

Uma API REST desenvolvida com FastAPI para gerenciamento de atletas, centros de treinamento e categorias esportivas.

## 🚀 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido para construção de APIs
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Banco de dados relacional
- **Alembic** - Ferramenta de migração de banco de dados
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI
- **FastAPI Pagination** - Biblioteca para paginação

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL
- Docker (opcional, para PostgreSQL containerizado)
- uv (gerenciador de pacotes Python)

## 🛠️ Configuração do Ambiente

### 1. Preparação do Ambiente Virtual

```bash
# Inicializar projeto com uv
uv init

# Criar ambiente virtual
uv venv .venv

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source .venv/bin/activate
```

### 2. Instalação das Dependências

```bash
# Instalar dependências principais
uv add fastapi uvicorn sqlalchemy psycopg2-binary fastapi-pagination

# Instalar dependências de migração
uv add alembic asyncpg

# Instalar configurações
uv add pydantic_settings
```

### 3. Configuração do PostgreSQL

#### Desativar PostgreSQL Local (se necessário)
```bash
# Windows - Parar serviço PostgreSQL local
net stop postgresql-x64-17
```

#### Usar PostgreSQL via Docker Compose
```bash
# Subir os serviços (PostgreSQL + aplicação)
docker-compose up -d

# Ver logs dos containers
docker-compose logs -f

# Parar os serviços
docker-compose down
```

#### Alternativa: PostgreSQL via Docker (manual)
```bash
# Executar PostgreSQL em container Docker
docker run --name desafioatleta-db-1 \
  -e POSTGRES_DB=Atleta_db \
  -e POSTGRES_USER=Atleta \
  -e POSTGRES_PASSWORD=Atleta \
  -p 5432:5432 \
  -d postgres:17
```

### 4. Configuração do Banco de Dados

```bash
# Executar com Docker Compose (recomendado)
docker-compose up -d

# Criar migração inicial
make create-migration d="init"

# Executar migrações
make run-migration
```

## 🏗️ Estrutura do Projeto

```
workout_api/
├── alembic/
│   ├── README
│   ├── env.py
│   └── script.py.mako
├── atleta/
│   ├── __init__.py
│   ├── controller.py
│   ├── models.py
│   └── schemas.py
├── categorias/
│   ├── __init__.py
│   ├── controller.py
│   ├── models.py
│   └── schemas.py
├── centro_treinamento/
│   ├── __init__.py
│   ├── controller.py
│   ├── models.py
│   └── schemas.py
├── configs/
│   ├── __init__.py
│   ├── database.py
│   ├── dependencies.py
│   └── settings.py
├── contrib/
│   ├── repository/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── __init__.py
│   ├── models.py
│   └── schemas.py
├── init-db/
│   └── 00-config.sh
├── .gitignore
├── .python-version
├── Makefile
├── README.md
├── __init__.py
├── alembic.ini
├── docker-compose.yml
├── main.py
└── pg_hba.conf
```

## 🚀 Executando a Aplicação

### Desenvolvimento Local
```bash
# Executar a aplicação diretamente
uvicorn main:app --reload

# Ou usando o Makefile (se configurado)
make run
```

### Docker Compose (Recomendado)
```bash
# Subir toda a stack (aplicação + banco)
docker-compose up -d

# Executar apenas o banco
docker-compose up -d db

# Ver logs em tempo real
docker-compose logs -f app

# Desligar o banco
docker-compose down -v

```

A API estará disponível em: `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

## 📝 Funcionalidades Implementadas

### ✅ Melhorias Realizadas

#### 1. Query Parameters nos Endpoints de Atleta
- **Nome**: Filtrar atletas por nome
- **CPF**: Buscar atleta específico por CPF

```http
GET /atletas?nome=João
GET /atletas?cpf=12345678901
```

#### 2. Response Customizada para GET ALL
Retorna informações resumidas incluindo:
- Nome do atleta
- Centro de treinamento
- Categoria

```json
{
  "atletas": [
    {
      "nome": "João Silva",
      "centro_treinamento": "CT Sesi",
      "categoria": "Scale"
    }
  ]
}
```

#### 3. Tratamento de Exceções de Integridade
- Captura `SQLAlchemy.exc.IntegrityError`
- Retorna mensagem personalizada para CPF duplicado
- Status code: `303`

```json
{
  "detail": "Já existe um atleta cadastrado com o cpf: 12345678901"
}
```

#### 4. Paginação com FastAPI-Pagination
- Implementação de `limit` e `offset`
- Controle de quantidade de registros por página

```http
GET /atletas?limit=10&offset=20
```

## 🏛️ Arquitetura do Projeto

### Organização Modular
O projeto segue uma arquitetura modular onde cada entidade possui sua própria estrutura:

- **`atleta/`**, **`categorias/`**, **`centro_treinamento/`**: Módulos principais da aplicação
  - `controller.py` - Lógica de controle e endpoints
  - `models.py` - Modelos do banco de dados (SQLAlchemy)
  - `schemas.py` - Schemas de validação (Pydantic)

### Configurações Centralizadas
- **`configs/`**: Configurações da aplicação
  - `database.py` - Configuração do banco de dados
  - `dependencies.py` - Dependências da aplicação
  - `settings.py` - Configurações gerais

### Componentes Auxiliares
- **`contrib/`**: Componentes reutilizáveis
  - `repository/` - Padrões de repositório
  - `models.py` - Modelos base
  - `schemas.py` - Schemas base

### Banco de Dados
- **`alembic/`**: Migrations do banco de dados
  - `versions/` - Arquivos de migração versionados
  - **Migrações existentes**:
    - `1ef5fc894328_init.py` - Migração inicial
    - `0745975c87f3_updata.py` - Primeira atualização
    - `ec19ee0c9fbf_updata2.py` - Segunda atualização

### Docker e Deploy
- **`docker-compose.yml`** - Orquestração de containers
- **`init-db/`** - Scripts de inicialização do banco
- **`pg_hba.conf`** - Configuração de autenticação PostgreSQL

## 🛡️ Tratamento de Erros

A API implementa tratamento robusto de erros incluindo:

- **Integridade de Dados**: Validação de CPF único
- **Validação de Entrada**: Campos obrigatórios e formatos
- **Erros de Banco**: Conexão e transações
- **Recursos Não Encontrados**: Status 404 apropriado

## 📊 Endpoints Principais

### Atletas (`/atletas`)
- `GET /atletas` - Listar atletas (com paginação e filtros)
- `POST /atletas` - Criar novo atleta
- `GET /atletas/{id}` - Buscar atleta por ID
- `PATCH /atletas/{id}` - Atualizar atleta
- `DELETE /atletas/{id}` - Remover atleta

### Categorias (`/categorias`)
- `GET /categorias` - Listar categorias
- `POST /categorias` - Criar nova categoria
- `GET /categorias/{id}` - Buscar categoria por ID

### Centros de Treinamento (`/centros-treinamento`)
- `GET /centros-treinamento` - Listar centros
- `POST /centros-treinamento` - Criar novo centro
- `GET /centros-treinamento/{id}` - Buscar centro por ID

## 🔧 Comandos Úteis (Makefile)

```bash
# Criar nova migração
make create-migration d="descrição_da_migração"

# Executar migrações
make run-migration

# Executar aplicação
make run

# Comandos Docker
docker-compose up -d        # Subir todos os serviços
docker-compose down         # Parar todos os serviços
docker-compose logs -f app  # Ver logs da aplicação
docker-compose logs -f db   # Ver logs do banco
```

## 🗄️ Gerenciamento de Migrações

O projeto utiliza Alembic para controle de versão do banco de dados:

```bash
# Ver histórico de migrações
alembic history

# Ver migração atual
alembic current

# Aplicar migração específica
alembic upgrade head

# Reverter migração
alembic downgrade -1

# Gerar migração automática
alembic revision --autogenerate -m "descrição"
```

### Migrações Existentes
- **`1ef5fc894328_init.py`** - Estrutura inicial do banco
- **`0745975c87f3_updata.py`** - Primeira atualização 
- **`ec19ee0c9fbf_updata2.py`** - Segunda atualização

## 📚 Repositórios

### Este Projeto
- **Repositório**: https://github.com/BrunoWil/Desafio-Atleta

### Referência Original
- **Repositório Original DIO**: https://github.com/digitalinnovationone/workout_api

## 🤝 Contribuições

Sinta-se à vontade para contribuir com melhorias! Algumas ideias:

- [ ] Implementar autenticação JWT
- [ ] Adicionar testes unitários
- [ ] Implementar cache com Redis
- [ ] Adicionar logging estruturado
- [ ] Dockerizar a aplicação completa

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Desenvolvedor

**Bruno Wilson** - [BrunoWil](https://github.com/BrunoWil)

**digitalinnovationone** -[digitalinnovationone](https://github.com/digitalinnovationone/workout_api/)

Desenvolvido como parte do desafio da Digital Innovation One (DIO) para demonstração de habilidades em:
- Desenvolvimento de APIs REST
- FastAPI e Python
- Banco de dados PostgreSQL
- Práticas de desenvolvimento moderno
- Arquitetura modular e clean code

---

⭐ **Dica**: Este projeto pode ser um diferencial em suas entrevistas técnicas! Demonstra conhecimento em tecnologias modernas e boas práticas de desenvolvimento.
