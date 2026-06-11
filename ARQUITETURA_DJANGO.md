# Arquitetura Django Aleica Gestao

## Visao geral

O novo projeto foi criado em `D:\Aleica\python` com projeto Django `aleica_core` e apps separados por dominio. A proposta e tratar Aleica Gestao como produto SaaS real, nao como conversao linha a linha do PHP.

## Apps

- `accounts`: perfis de usuario e papéis operacionais.
- `empresas`: empresas clientes da plataforma.
- `clientes`: carteira de clientes, status, origem e dados comerciais.
- `relacionamento`: historico de contatos e Fila da Carine.
- `oportunidades`: oportunidades priorizadas e status operacional.
- `inteligencia`: snapshots, score, risco, probabilidade, receita potencial e services.
- `dashboards`: KPIs, graficos e relatorios executivos.
- `website`: landing page publica.
- `core`: helpers, template tags, utilitarios e base visual.

## Models principais

- `Empresa`
- `Cliente`
- `Oportunidade`
- `HistoricoContato`
- `SnapshotInteligencia`
- `PerfilUsuario`

## Services

As regras ficam em `inteligencia/services.py`:

- `calcular_dias_sem_retorno`
- `calcular_score_aleica`
- `calcular_probabilidade_perda`
- `calcular_risco`
- `calcular_valor_potencial`
- `gerar_motivo_alerta`
- `gerar_acao_sugerida`
- `gerar_oportunidades`
- `atualizar_inteligencia_empresa`

## Banco

O projeto aceita `DB_ENGINE` por ambiente:

- SQLite para desenvolvimento local rapido.
- MySQL/MariaDB para o banco online atual.
- PostgreSQL futuramente com troca de engine e driver.

## UX/UI

A interface usa Bootstrap 5, Bootstrap Icons, Chart.js e CSS proprio. O produto possui:

- Landing page publica.
- Login separado.
- Sidebar interna.
- Header com breadcrumb.
- Cards KPI.
- Tabelas limpas.
- Filtros.
- Empty states.
- Graficos Chart.js.
- Layout responsivo.

## Rotas principais

- `/`
- `/login/`
- `/dashboard/`
- `/empresas/`
- `/clientes/`
- `/oportunidades/`
- `/relacionamento/fila/`
- `/relacionamento/historico/`
- `/inteligencia/`
- `/relatorios/`

## Seguranca

- Django auth.
- Senhas com hash.
- Views internas com `login_required`.
- CSRF em formularios.
- `SECRET_KEY`, `DEBUG`, hosts e banco por `.env`.
- Credenciais reais fora do settings.
