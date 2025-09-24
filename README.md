# 🚗 Controle de Veículos - Projeto Integrador UNIVESP 2025

Aplicação web para **registro de acessos de veículos e pedestres**. 

---

## 📌 Funcionalidades

- Cadastro de veículos e pedestres
- Registro de entrada e saída
- Interface web intuitiva e responsiva
- Histórico completo de acessos

---

## 🧰 Tecnologias Utilizadas

- [Django 5.2](https://docs.djangoproject.com/)
- [MySQL](https://www.mysql.com/)
- HTML, CSS e JavaScript
- Django REST Framework

---

## ⚙️ Instalação

### 1. Clone o repositório
```bash

# Clone o repositório
git clone https://github.com/lucasjponce/controleVeiculos.git
cd .\controleVeiculos\ 

# Crie um ambiente virtual
python -m venv env
source env/bin/activate  # Linux/Mac
source env\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Crie o banco de dados MySQL
CREATE DATABASE controleveiculos;

# Execute as migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver
