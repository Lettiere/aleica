# Aleica Gestao

Plataforma Django para gestao comercial, relacionamento e inteligencia de clientes da Aleica Assessoria Digital.

## Comandos principais

```powershell
cd /d D:\www\Aleica
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 127.0.0.1:7500
```

Tambem existem:

- `start_local.bat`
- `start_local.ps1`

## Funcionalidades implementadas

- Landing page publica.
- Login com Django auth.
- Dashboard executivo com KPIs e Chart.js.
- Empresas.
- Clientes.
- Oportunidades.
- Fila de Relacionamento da Carine.
- Historico de contatos.
- Inteligencia comercial.
- Relatorios.
- Seed demo com 6 empresas e 120 clientes.

## Banco

O `.env` local usa SQLite para facilitar a validacao. O `.env.example` documenta MySQL/MariaDB online e preparo para PostgreSQL futuro. A flag de debug usa `ALEICA_DEBUG` para evitar colisao com variaveis globais do sistema.

## Acesso local

- `http://127.0.0.1:7500/`
- `http://127.0.0.1:7500/login/`
- `http://127.0.0.1:7500/dashboard/`
