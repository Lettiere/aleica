# Instalacao Local

## Requisitos

- Python 3.12+
- pip
- Ambiente virtual recomendado

## Passos

```powershell
cd /d D:\www\Aleica
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 127.0.0.1:7500
```

## URLs

- `http://127.0.0.1:7500/`
- `http://127.0.0.1:7500/login/`
- `http://127.0.0.1:7500/dashboard/`

## Usuarios demo

- `aleixa.master` / `eunaosei`
- `carina.fernandes` / `aleica2026`

O login Django aceita username. Os emails foram cadastrados nos respectivos usuarios.
