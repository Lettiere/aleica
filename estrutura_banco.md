# Estrutura de Banco Aleica SaaS

Banco alvo: PostgreSQL `aleica`.

Schemas criados:

- `core`: empresas, usuarios, perfis e permissoes.
- `crm`: oportunidades e historico operacional.
- `cliente`: dados de clientes das empresas contratantes.
- `contrato`: modulo futuro de contratos.
- `financeiro`: modulo futuro financeiro.
- `documento`: modulo futuro de documentos.
- `relatorio`: snapshots e estruturas analiticas.
- `auditoria`: trilhas de auditoria futuras.

Padrao adotado:

- Tabelas: `schema.nome_tb`.
- Primary key: `nome_id`.
- Foreign key: `outra_tabela_id_fk`.
- Constraints: `nome_tabela_pk` e `nome_tabela_fk`.
- Campos obrigatorios de ciclo de vida: `ativo`, `created_at`, `updated_at`, `deleted_at`.
- Atualizacao automatica: `core.fn_set_updated_at()`.

Tabelas iniciais:

- `core.empresa_tb`
- `core.usuario_tb`
- `core.perfil_tb`
- `core.permissao_tb`
- `core.usuario_permissao_tb`
- `cliente.cliente_tb`
- `crm.oportunidade_tb`
- `crm.historico_contato_tb`
- `relatorio.snapshot_inteligencia_tb`

RBAC:

- `ROOT`
- `ADMIN_ASSESSORIA`
- `GESTOR`
- `OPERADOR`
- `CLIENTE_ADMIN`
- `CLIENTE_USUARIO`

Isolamento multiempresa:

- Toda tabela de negocio possui `empresa_id_fk`.
- O middleware `core.middleware.EmpresaContextMiddleware` popula `request.empresa` e `request.perfil_codigo`.
- Managers em `core.managers` filtram automaticamente registros por empresa para perfis de cliente.
- Perfis internos da assessoria acessam visao consolidada do backoffice.
