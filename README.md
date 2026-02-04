# 🔐 SecurePass Dashboard

Um dashboard de análise de senhas com detecção de vazamentos - projeto portfólio full-stack.

## 🎯 O que faz

- ✅ Usuário cadastra (hashes de) senhas
- ✅ Verifica se apareceram em data breaches (Have I Been Pwned API)
- ✅ Mostra força da senha com visual interativo
- ✅ Dashboard com estatísticas de segurança

## 🛠️ Stack

| Camada | Tecnologia |
|--------|------------|
| Frontend | React + Vite + Chart.js + TailwindCSS |
| Backend | Django + Django REST Framework |
| Auth | JWT (SimpleJWT) |
| API Externa | Have I Been Pwned |
| Database | SQLite (dev) / PostgreSQL (prod) |

## 📁 Estrutura

```
securepass-dashboard/
├── backend/          # Django REST API
│   ├── securepass/   # Django project
│   ├── api/          # REST API app
│   └── manage.py
├── frontend/         # React app
│   ├── src/
│   └── package.json
└── docs/             # Documentação
```

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🔑 Features

1. **Password Strength Analyzer** - Analisa força com critérios visuais
2. **Breach Detection** - Verifica contra Have I Been Pwned
3. **Security Dashboard** - Gráficos e estatísticas
4. **User Auth** - Login/registro com JWT

## 🎨 Screenshots

*Em breve*

## 📊 API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | /api/auth/register/ | Registrar usuário |
| POST | /api/auth/login/ | Login (retorna JWT) |
| POST | /api/passwords/check/ | Verificar senha |
| GET | /api/passwords/stats/ | Estatísticas do usuário |
| GET | /api/breach/check/ | Verificar vazamento |

## 🔒 Segurança

- Senhas NUNCA são armazenadas em texto plano
- Usamos k-anonymity com HIBP API (apenas 5 primeiros chars do hash)
- JWT com refresh tokens
- HTTPS obrigatório em produção

## 👨‍💻 Autor

**Kelson Brito**
- LinkedIn: [seu-linkedin]
- GitHub: [@kelsonbrito50](https://github.com/kelsonbrito50)

## 📄 License

MIT
