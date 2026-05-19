# Projeto QTS — Qualidade e Testes de Software

API REST desenvolvida com Flask, com testes automatizados e pipeline CI/CD.

---

## Requisitos

- Python 3.12+
- Google Chrome (para testes E2E)

---

## Instalação

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

---

## Executar a API

```bash
python run.py
```

Acesse em: `http://localhost:5000`

---

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /status | Verifica se a API está no ar |
| GET | /hello | Retorna Hello World |
| GET | /users | Lista todos os usuários |
| GET | /users/{id} | Busca usuário por ID |
| GET | /users/search?name= | Busca usuários por nome |
| POST | /users | Cria um usuário |
| PUT | /users/{id} | Atualiza um usuário |
| DELETE | /users/{id} | Remove um usuário |

---

## Testes

### Rodar todos os testes (exceto E2E)

```bash
pytest
```

### Rodar por tipo

```bash
pytest tests/unit/
pytest tests/integration/
pytest tests/functional/
```

### Rodar testes E2E (requer Chrome instalado)

```bash
pytest tests/e2e/ -v
```

---

## Qualidade de código

```bash
black .
flake8 .
```

---

## Estrutura do projeto

```
projeto_qts/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   └── user_routes.py
│   ├── services/
│   │   └── user_service.py
│   └── templates/
│       └── users.html
├── tests/
│   ├── unit/
│   │   ├── test_user_service.py
│   │   └── test_search_tdd.py
│   ├── integration/
│   │   ├── test_user_routes.py
│   │   └── test_search_routes.py
│   ├── functional/
│   │   ├── test_users_functional.py
│   │   └── test_search_functional.py
│   └── e2e/
│       └── test_user_e2e.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── conftest.py
├── run.py
├── requirements.txt
├── setup.cfg
└── pytest.ini
```

---

## TDD — Evidência do ciclo RED → GREEN → REFACTOR

A funcionalidade de busca de usuários por nome (`/users/search`) foi implementada utilizando TDD.

**RED** — Os testes em `tests/unit/test_search_tdd.py` foram escritos antes da implementação. Ao rodar `pytest` nesse momento, todos falhavam pois `search_users_by_name` ainda não existia.

**GREEN** — A função `search_users_by_name` foi implementada em `app/services/user_service.py` com o mínimo necessário para os testes passarem.

**REFACTOR** — O código foi revisado para garantir clareza e sem duplicação, mantendo todos os testes passando.

Os commits no repositório evidenciam esse ciclo:
- `RED: testes de busca por nome (TDD)`
- `GREEN: implementa search_users_by_name`
- `REFACTOR: melhora legibilidade do search_users_by_name`

---

## CI/CD

O projeto utiliza GitHub Actions. A pipeline executa automaticamente a cada push na branch `main`:

1. `black --check .`
2. `flake8 .`
3. `pytest tests/unit tests/integration tests/functional`
