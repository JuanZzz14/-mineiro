# 🏠 Ô Mineiro — Sistema de Estoque

Sistema web de gerenciamento de estoque para o Restaurante Ô Mineiro.

## Como rodar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Rodar o sistema
```bash
python app.py
```

### 3. Acessar no navegador
```
http://localhost:5000
```

---

## Usuários padrão

| Usuário       | Senha     | Perfil      |
|---------------|-----------|-------------|
| `admin`       | `admin123`| Gestor      |
| `funcionario` | `func123` | Funcionário |

> ⚠️ **Troque as senhas após o primeiro acesso!**

---

## Estrutura de pastas

```
omineiro/
├── app.py              # Ponto de entrada
├── extensions.py       # SQLAlchemy e LoginManager
├── models.py           # Tabelas do banco de dados
├── requirements.txt    # Dependências
├── routes/
│   ├── auth.py         # Login, cadastro, logout
│   ├── dashboard.py    # Página inicial
│   ├── produtos.py     # Cadastro de produtos
│   ├── movimentacoes.py# Entrada e saída
│   └── alertas.py      # Alertas de estoque baixo
├── templates/
│   ├── base.html       # Layout com sidebar
│   ├── login.html
│   ├── cadastro.html
│   ├── dashboard.html
│   ├── produtos.html
│   ├── produto_form.html
│   ├── movimentacoes.html
│   ├── movimentacao_form.html
│   └── alertas.html
└── static/
    ├── css/style.css   # Visual com identidade do Ô Mineiro
    └── img/mascote.svg # Mascote na sidebar
```

---

## Perfis de acesso

- **Gestor:** acesso total — cadastra/edita/exclui produtos, vê tudo
- **Funcionário:** registra entradas e saídas, vê alertas

---

## Banco de dados

SQLite — arquivo `estoque.db` criado automaticamente na primeira execução.
