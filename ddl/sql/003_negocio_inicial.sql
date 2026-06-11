CREATE TABLE IF NOT EXISTS cliente.cliente_tb (
    cliente_id bigserial NOT NULL,
    empresa_id_fk bigint NOT NULL,
    nome varchar(160) NOT NULL,
    telefone varchar(30) NULL,
    whatsapp varchar(30) NULL,
    email varchar(180) NULL,
    origem varchar(80) NULL,
    ultimo_atendimento date NULL,
    valor_total_gasto numeric(12,2) NOT NULL DEFAULT 0,
    quantidade_compras integer NOT NULL DEFAULT 0,
    status varchar(40) NOT NULL DEFAULT 'ativo',
    observacoes text NULL,
    ativo boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz NULL,
    CONSTRAINT cliente_tb_pk PRIMARY KEY (cliente_id),
    CONSTRAINT cliente_tb_empresa_fk FOREIGN KEY (empresa_id_fk) REFERENCES core.empresa_tb (empresa_id)
);

DROP TRIGGER IF EXISTS cliente_tb_set_updated_at_trg ON cliente.cliente_tb;
CREATE TRIGGER cliente_tb_set_updated_at_trg
BEFORE UPDATE ON cliente.cliente_tb
FOR EACH ROW EXECUTE FUNCTION core.fn_set_updated_at();

CREATE TABLE IF NOT EXISTS crm.oportunidade_tb (
    oportunidade_id bigserial NOT NULL,
    cliente_id_fk bigint NOT NULL,
    empresa_id_fk bigint NOT NULL,
    tipo varchar(90) NOT NULL,
    prioridade varchar(20) NOT NULL DEFAULT 'baixo',
    score integer NOT NULL DEFAULT 0,
    probabilidade_perda integer NOT NULL DEFAULT 0,
    valor_potencial numeric(12,2) NOT NULL DEFAULT 0,
    motivo varchar(255) NOT NULL,
    descricao text NULL,
    acao_sugerida varchar(255) NOT NULL,
    risco varchar(20) NOT NULL DEFAULT 'baixo',
    status varchar(20) NOT NULL DEFAULT 'aberta',
    data_reagendamento date NULL,
    ativo boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz NULL,
    CONSTRAINT oportunidade_tb_pk PRIMARY KEY (oportunidade_id),
    CONSTRAINT oportunidade_tb_cliente_fk FOREIGN KEY (cliente_id_fk) REFERENCES cliente.cliente_tb (cliente_id),
    CONSTRAINT oportunidade_tb_empresa_fk FOREIGN KEY (empresa_id_fk) REFERENCES core.empresa_tb (empresa_id)
);

DROP TRIGGER IF EXISTS oportunidade_tb_set_updated_at_trg ON crm.oportunidade_tb;
CREATE TRIGGER oportunidade_tb_set_updated_at_trg
BEFORE UPDATE ON crm.oportunidade_tb
FOR EACH ROW EXECUTE FUNCTION core.fn_set_updated_at();

CREATE TABLE IF NOT EXISTS crm.historico_contato_tb (
    historico_contato_id bigserial NOT NULL,
    empresa_id_fk bigint NOT NULL,
    cliente_id_fk bigint NOT NULL,
    oportunidade_id_fk bigint NULL,
    usuario_id integer NULL,
    data_contato timestamptz NOT NULL,
    tipo_contato varchar(80) NOT NULL,
    resultado varchar(160) NOT NULL,
    observacao text NULL,
    proxima_acao varchar(160) NULL,
    data_proxima_acao date NULL,
    ativo boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz NULL,
    CONSTRAINT historico_contato_tb_pk PRIMARY KEY (historico_contato_id),
    CONSTRAINT historico_contato_tb_empresa_fk FOREIGN KEY (empresa_id_fk) REFERENCES core.empresa_tb (empresa_id),
    CONSTRAINT historico_contato_tb_cliente_fk FOREIGN KEY (cliente_id_fk) REFERENCES cliente.cliente_tb (cliente_id),
    CONSTRAINT historico_contato_tb_oportunidade_fk FOREIGN KEY (oportunidade_id_fk) REFERENCES crm.oportunidade_tb (oportunidade_id)
);

DROP TRIGGER IF EXISTS historico_contato_tb_set_updated_at_trg ON crm.historico_contato_tb;
CREATE TRIGGER historico_contato_tb_set_updated_at_trg
BEFORE UPDATE ON crm.historico_contato_tb
FOR EACH ROW EXECUTE FUNCTION core.fn_set_updated_at();

CREATE TABLE IF NOT EXISTS relatorio.snapshot_inteligencia_tb (
    snapshot_inteligencia_id bigserial NOT NULL,
    empresa_id_fk bigint NOT NULL,
    cliente_id_fk bigint NOT NULL,
    score_aleica integer NOT NULL DEFAULT 0,
    risco varchar(20) NOT NULL,
    probabilidade_perda integer NOT NULL DEFAULT 0,
    dias_sem_retorno integer NOT NULL DEFAULT 0,
    valor_potencial numeric(12,2) NOT NULL DEFAULT 0,
    motivo_alerta varchar(255) NOT NULL,
    ativo boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz NULL,
    CONSTRAINT snapshot_inteligencia_tb_pk PRIMARY KEY (snapshot_inteligencia_id),
    CONSTRAINT snapshot_inteligencia_tb_empresa_fk FOREIGN KEY (empresa_id_fk) REFERENCES core.empresa_tb (empresa_id),
    CONSTRAINT snapshot_inteligencia_tb_cliente_fk FOREIGN KEY (cliente_id_fk) REFERENCES cliente.cliente_tb (cliente_id)
);

DROP TRIGGER IF EXISTS snapshot_inteligencia_tb_set_updated_at_trg ON relatorio.snapshot_inteligencia_tb;
CREATE TRIGGER snapshot_inteligencia_tb_set_updated_at_trg
BEFORE UPDATE ON relatorio.snapshot_inteligencia_tb
FOR EACH ROW EXECUTE FUNCTION core.fn_set_updated_at();

