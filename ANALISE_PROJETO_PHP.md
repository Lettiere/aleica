# Analise do Projeto PHP Aleica

## Estrutura encontrada

O projeto legado esta em `D:\Aleica\online` e foi usado apenas como referencia. A estrutura principal encontrada foi:

- `index.php`, `login.php`, `logout.php`, `dashboard.php` como entradas publicas e internas.
- `config/config.php` com conexao PDO online para MySQL/MariaDB.
- `config/database.php` com configuracao local antiga.
- `includes/bootstrap.php`, `auth.php`, `helpers.php`, `data.php`, `intelligence.php`.
- `pages/` com telas internas: empresas, clientes, fila, oportunidades, inteligencia, relacionamento, relatorios, importar e radar.
- `database.sql`, `database/schema.sql`, `database/seed.sql`.
- `assets/css/app.css`, `assets/css/style.css`, `assets/js/app.js`.
- `assets/img/carina_banner_inicial.png` e `carine_banner_1.jpeg`.

## Banco e tabelas

O SQL principal define:

- `usuarios`: username, nome, email, senha_hash, perfil, status.
- `empresas`: nome_fantasia, razao_social, cnpj, segmento, cidade, estado, telefone, email, status.
- `clientes`: empresa_id, nome, telefone, whatsapp, email, origem, ultimo_atendimento, valor_total_gasto, quantidade_compras, status, observacoes.
- `oportunidades`: cliente_id, empresa_id, tipo, motivo, prioridade, acao_sugerida, valor_potencial, probabilidade_perda, score_aleica, nivel_risco, status, data_reagendamento.
- `relacionamentos`: cliente_id, empresa_id, oportunidade_id, usuario_id, data_contato, tipo_contato, resultado, observacao, proxima_acao, data_proxima_acao.

Ha uma inconsistencia em `pages/historico.php`, que usa uma tabela `historicos` nao presente no schema principal. O fluxo mais consistente e `relacionamentos`.

## Regras de negocio identificadas

As regras mais importantes estavam em `includes/intelligence.php`:

- Risco por dias sem retorno: ate 90 baixo, ate 180 medio, ate 365 alto, acima de 365 critico.
- Score Aleica usa recencia, valor total gasto, quantidade de compras, relacionamento e penalidade por abandono.
- Probabilidade de perda cresce com dias sem retorno e status, mas recebe protecao por frequencia de compras.
- Cliente VIP com alto gasto e sem retorno aumenta risco.
- Orcamento abandonado aumenta oportunidade e probabilidade.
- Receita potencial usa ticket medio ajustado pela probabilidade de perda.
- A oportunidade e classificada como orcamento abandonado, VIP sem retorno, cliente inativo, cliente em risco, pos-venda pendente, reativacao ou relacionamento saudavel.

## Telas publicas

- Landing page com Aleica Gestao, problema, solucao, papel da Carine, CTA de demonstracao, WhatsApp e login.
- Uma versao anterior em `pages/home.php` ainda chama o produto de Aleica Radar, sinalizando evolucao de marca.

## Telas internas

- Dashboard executivo com KPIs e graficos.
- Empresas: cadastro, edicao, listagem e busca.
- Clientes: cadastro, edicao, filtros e listagem.
- Oportunidades: filtros e prioridades.
- Fila da Carine: operacional, com WhatsApp, marcar contatado, reagendar e historico.
- Relacionamento: registro e historico de contatos.
- Inteligencia: listas de clientes com maior risco, VIPs, inativos e recuperaveis.
- Relatorios: clientes em risco, perdidos, recuperaveis, VIPs, oportunidades abertas e historico.

## Pontos fortes

- Prototipo validou bem o conceito de CRM + relacionamento + inteligencia.
- Regras de score e risco ja tinham boa direcao de negocio.
- Fila da Carine e uma tela operacional clara.
- Uso de prepared statements, PDO, CSRF simples e hash de senha.
- Identidade visual inicial coerente para SaaS.

## Pontos fracos

- Arquitetura procedural e acoplada a arquivos PHP.
- Regras de negocio misturadas a paginas e SQL.
- Rotas por query string, sem separacao real por dominio.
- Inconsistencia entre `historicos` e `relacionamentos`.
- Importacao CSV antiga referencia campos que nao existem mais no schema.
- Credenciais hardcoded no PHP.
- Sem migrations, testes, camada de services ou separacao de ambientes.

## Decisoes para a migracao

- Preservar regras de inteligencia e conceito de fila.
- Descartar arquitetura procedural.
- Recriar entidades como models Django.
- Centralizar regra analitica em `inteligencia/services.py`.
- Usar Django auth, CSRF, templates organizados e views protegidas.
- Preparar settings por `.env` para MySQL agora e PostgreSQL futuramente.
