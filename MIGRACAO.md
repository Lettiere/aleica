# Plano de Migracao

## O que foi aproveitado

- Conceito de Aleica Gestao.
- Papel da Carine como Gestora de Relacionamento.
- Entidades principais: empresas, clientes, oportunidades, contatos e usuarios.
- Regras de risco, score, probabilidade de perda e receita potencial.
- Identidade visual e imagem `carina_banner_inicial.png`.
- Relatorios executivos e fluxo da fila operacional.

## O que foi descartado

- Arquitetura procedural PHP.
- Rotas por `dashboard.php?page=...`.
- SQL manual dentro das paginas.
- Tabela inconsistente `historicos`.
- Importacao CSV antiga acoplada a campos obsoletos.
- Credenciais hardcoded em codigo de aplicacao.

## Importacao futura

O app `clientes` deve receber um modulo futuro `importers.py` para CSV/Excel usando `pandas` e `openpyxl`. O formato recomendado para importacao:

- empresa
- nome
- telefone
- whatsapp
- email
- origem
- ultimo_atendimento
- valor_total_gasto
- quantidade_compras
- status
- observacoes

## Caminho recomendado

1. Validar o MVP Django com seed ficticio.
2. Criar importador CSV/Excel.
3. Mapear dados reais do MySQL legado.
4. Migrar empresas, clientes, oportunidades e relacionamentos.
5. Rodar `atualizar_inteligencia_empresa` para recalcular oportunidades.
6. Revisar UX com a Carine usando a fila real.
