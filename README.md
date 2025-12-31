
# 🧠 Task Manager Pro
**Advanced Task Management API — FastAPI, Async SQLAlchemy, PostgreSQL, JWT**

---

## 🇺🇸 English

### Overview
**Task Manager Pro** is a production-ready REST API for advanced task management, built with modern Python backend best practices.

It features:
- **Async architecture**
- **JWT authentication with refresh token rotation**
- **Strong data modeling**
- **Filtering, pagination, and search**
- **Rate limiting and CORS**
- **Automated tests with coverage enforcement**
- **Dockerized setup**

This project is designed to demonstrate **real-world backend engineering skills**, not toy examples.

---

### Tech Stack
- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL
- Pydantic v2
- JWT (access + refresh tokens with rotation)
- Alembic (migrations)
- SlowAPI (rate limiting)
- Pytest + Coverage
- Docker & Docker Compose

---

### Core Features
- 🔐 Authentication
  - JWT access tokens
  - Refresh tokens stored hashed in database
  - Refresh token rotation & revocation
- 🗂️ Categories
  - User-scoped categories
  - Unique per user
- ✅ Tasks
  - Full CRUD
  - Status & priority
  - Optional category
- 🔍 Advanced querying
  - Text search
  - Filters (status, priority, category, dates)
  - Pagination
  - Safe sorting (whitelisted fields)
- 🛡️ Security
  - Rate limiting on auth endpoints
  - Configurable CORS
- 🧪 Testing
  - Async test suite
  - Coverage enforced (≥ 80%)

---

### API Endpoints (Summary)

#### Auth
```
POST   /auth/register
POST   /auth/login
POST   /auth/refresh
POST   /auth/logout
```

#### Categories
```
POST   /categories
GET    /categories
PATCH  /categories/{id}
DELETE /categories/{id}
```

#### Tasks
```
POST   /tasks
GET    /tasks
GET    /tasks/{id}
PATCH  /tasks/{id}
DELETE /tasks/{id}
```

---

### Running with Docker
```bash
cp .env.example .env
docker compose up --build
```

API available at:
```
http://localhost:8000
```

Interactive docs:
```
http://localhost:8000/docs
```

---

### Running Tests
```bash
pip install -e ".[dev]"
pytest
coverage run -m pytest
coverage report -m
```

---

### Project Philosophy
This project intentionally includes:
- explicit configuration contracts
- strict ownership checks
- refresh token persistence
- async database patterns
- realistic pagination & filtering

It reflects how **real backend services are built and maintained**.

---

## 🇧🇷 Português

### Visão Geral
**Task Manager Pro** é uma API REST pronta para produção voltada ao gerenciamento avançado de tarefas, construída com boas práticas modernas de backend em Python.

O projeto demonstra:
- **Arquitetura assíncrona**
- **Autenticação JWT com refresh token rotacionado**
- **Modelagem de dados sólida**
- **Filtros, paginação e busca**
- **Rate limiting e CORS**
- **Testes automatizados com cobertura mínima**
- **Ambiente Dockerizado**

Não é um projeto didático — é um **exemplo realista de backend profissional**.

---

### Stack Tecnológica
- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL
- Pydantic v2
- JWT (access + refresh tokens com rotação)
- Alembic
- SlowAPI
- Pytest + Coverage
- Docker & Docker Compose

---

### Funcionalidades
- 🔐 Autenticação
  - Access tokens JWT
  - Refresh tokens persistidos com hash
  - Rotação e revogação de refresh tokens
- 🗂️ Categorias
  - Escopo por usuário
  - Nome único por usuário
- ✅ Tarefas
  - CRUD completo
  - Status e prioridade
  - Categoria opcional
- 🔍 Consultas avançadas
  - Busca textual
  - Filtros por status, prioridade, categoria e datas
  - Paginação
  - Ordenação segura
- 🛡️ Segurança
  - Rate limiting nos endpoints sensíveis
  - CORS configurável
- 🧪 Testes
  - Testes assíncronos
  - Cobertura mínima exigida (≥ 80%)

---

### Executando com Docker
```bash
cp .env.example .env
docker compose up --build
```

API disponível em:
```
http://localhost:8000
```

Swagger:
```
http://localhost:8000/docs
```

---

### Executando os Testes
```bash
pip install -e ".[dev]"
pytest
coverage run -m pytest
coverage report -m
```

---

### Filosofia do Projeto
Este projeto foi pensado para refletir sistemas reais, incluindo:
- contratos explícitos de configuração
- controle de acesso rigoroso
- persistência de refresh tokens
- padrões assíncronos modernos
- consultas robustas e seguras

Ele existe para demonstrar **engenharia de backend de verdade**, não atalhos.
