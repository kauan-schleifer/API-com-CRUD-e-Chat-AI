## 📚Projeto FastAPI - CRUD de Usuários + Integração com IA Gemini

---

## 🛠️  Tecnologias Utilizadas

- Pycharm
- Python
- FastAPI
- Uvicorn
- SQLite
- Pydantic

---


## 📦 Instalação e Execução
### 1. Clonar o Repositório
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
### 2. Criar Ambiente Virtual (opcional, mas recomendado)
python -m venv venv

source venv/bin/activate  # Linux/Mac

venv\Scripts\activate     # Windows
### 3. Instalar Dependências
pip install fastapi uvicorn sqlalchemy pydantic

pip install google-generativeai

### 4. Rodar o Projeto
uvicorn main:app --reload

---

## 📑 Como Acessar
+ Swagger UI: ➔ http://127.0.0.1:8000/docs
+ Redoc: ➔ http://127.0.0.1:8000/redoc

---

## 🚀 Funcionalidades
CRUD de Usuários (``/usuarios``)

+ ``POST /usuarios`` ➔ Criar novo usuário.

+ ``GET /usuarios/{usuario_id}`` ➔ Buscar usuário pelo ID.

+ ``PUT /usuarios/{usuario_id}`` ➔ Atualizar dados do usuário.

+ ``DELETE /usuarios/{usuario_id}`` ➔ Deletar usuário pelo ID.


---

## 💬Chat com IA (``/chat``)
+ ``POST /chat`` ➔ Envia uma pergunta ou comando para a IA responder.

Exemplos:

+ ```"Quantos usuários existem?"```

+ ``"Listar usuários"``

+ ``"Apagar usuário 2"``

+ ``Criar usuário Kauan com email test@gmail.com e idade 20``

+  ``Qual a capital do Brasil?`` (Resposta no terminal)

+  ``O que é IA?`` (Resposta no terminal)


---

## ⭐ Extras (Plus)
+ Integração entre o Chat e o CRUD: o endpoint /chat pode interpretar comandos para criar, ler ou atualizar usuários diretamente via IA.

---

## 📄 Observações

+ O banco de dados utilizado é SQLite, salvo localmente no projeto.

+ A integração AI usa a API do Gemini (Google Generative AI).

+ As rotas estão documentadas automaticamente pelo FastAPI.
