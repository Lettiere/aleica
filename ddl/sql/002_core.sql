CREATE OR REPLACE FUNCTION core.fn_set_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

CREATE TABLE IF NOT EXISTS core.empresa_tb (
    empresa_id bigserial NOT NULL,
    razao_social varchar(190) NOT NULL,
    nome_fantasia varchar(160) NOT NULL,
    cnpj varchar(24) NULL,
    email varchar(180) NULL,
    telefone varchar(30) NULL,
    status varchar(20) NOT NULL DEFAULT 'ativa',
    segmento varchar(100) NULL,
    cidade varchar(100) NULL,
    estado varchar(2) NULL,
    ativo boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz NULL,
    CONSTRAINT empresa_tb_pk PRIMARY KEY (empresa_id)
);

DROP TRIGGER IF EXISTS empresa_tb_set_updated_at_trg ON core.empresa_tb;
CREATE TRIGGER empresa_tb_set_updated_at_trg
BEFORE UPDATE ON core.empresa_tb
FOR EACH ROW EXECUTE FUNCTION core.fn_set_updated_at();

CREATE TABLE IF NOT EXISTS core.perfil_tb (
    perfil_id bigserial NOT NULL,
    nome_perfil varchar(40) NOT NULL,
    descricao varchar(255) NULL,
    ativo boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz NULL,
    CONSTRAINT perfil_tb_pk PRIMARY KEY (perfil_id),
    CONSTRAINT perfil_tb_nome_perfil_uk UNIQUE (nome_perfil)
);

DROP TRIGGER IF EXISTS perfil_tb_set_updated_at_trg ON core.perfil_tb;
CREATE TRIGGER perfil_tb_set_updated_at_trg
BEFORE UPDATE ON core.perfil_tb
FOR EACH ROW EXECUTE FUNCTION core.fn_set_updated_at();

CREATE TABLE IF NOT EXISTS core.permissao_tb (
    permissao_id bigserial NOT NULL,
    codigo varchar(80) NOT NULL,
    descricao varchar(255) NULL,
    ativo boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz NULL,
    CONSTRAINT permissao_tb_pk PRIMARY KEY (permissao_id),
    CONSTRAINT permissao_tb_codigo_uk UNIQUE (codigo)
);

DROP TRIGGER IF EXISTS permissao_tb_set_updated_at_trg ON core.permissao_tb;
CREATE TRIGGER permissao_tb_set_updated_at_trg
BEFORE UPDATE ON core.permissao_tb
FOR EACH ROW EXECUTE FUNCTION core.fn_set_updated_at();

CREATE TABLE IF NOT EXISTS core.usuario_tb (
    usuario_id bigserial NOT NULL,
    auth_user_id integer NULL,
    empresa_id_fk bigint NULL,
    perfil_id_fk bigint NOT NULL,
    nome varchar(160) NOT NULL,
    email varchar(180) NOT NULL,
    senha_hash varchar(255) NOT NULL,
    ultimo_login timestamptz NULL,
    ativo boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz NULL,
    CONSTRAINT usuario_tb_pk PRIMARY KEY (usuario_id),
    CONSTRAINT usuario_tb_email_uk UNIQUE (email),
    CONSTRAINT usuario_tb_empresa_fk FOREIGN KEY (empresa_id_fk) REFERENCES core.empresa_tb (empresa_id),
    CONSTRAINT usuario_tb_perfil_fk FOREIGN KEY (perfil_id_fk) REFERENCES core.perfil_tb (perfil_id)
);

DROP TRIGGER IF EXISTS usuario_tb_set_updated_at_trg ON core.usuario_tb;
CREATE TRIGGER usuario_tb_set_updated_at_trg
BEFORE UPDATE ON core.usuario_tb
FOR EACH ROW EXECUTE FUNCTION core.fn_set_updated_at();

CREATE TABLE IF NOT EXISTS core.usuario_permissao_tb (
    usuario_permissao_id bigserial NOT NULL,
    usuario_id_fk bigint NOT NULL,
    permissao_id_fk bigint NOT NULL,
    ativo boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz NULL,
    CONSTRAINT usuario_permissao_tb_pk PRIMARY KEY (usuario_permissao_id),
    CONSTRAINT usuario_permissao_tb_usuario_fk FOREIGN KEY (usuario_id_fk) REFERENCES core.usuario_tb (usuario_id),
    CONSTRAINT usuario_permissao_tb_permissao_fk FOREIGN KEY (permissao_id_fk) REFERENCES core.permissao_tb (permissao_id),
    CONSTRAINT usuario_permissao_tb_uk UNIQUE (usuario_id_fk, permissao_id_fk)
);

DROP TRIGGER IF EXISTS usuario_permissao_tb_set_updated_at_trg ON core.usuario_permissao_tb;
CREATE TRIGGER usuario_permissao_tb_set_updated_at_trg
BEFORE UPDATE ON core.usuario_permissao_tb
FOR EACH ROW EXECUTE FUNCTION core.fn_set_updated_at();

INSERT INTO core.perfil_tb (nome_perfil, descricao)
VALUES
    ('ROOT', 'Acesso total da plataforma'),
    ('ADMIN_ASSESSORIA', 'Administrador do portal da assessoria'),
    ('GESTOR', 'Gestor interno da assessoria'),
    ('OPERADOR', 'Operador interno da assessoria'),
    ('CLIENTE_ADMIN', 'Administrador do portal do cliente'),
    ('CLIENTE_USUARIO', 'Usuario do portal do cliente')
ON CONFLICT (nome_perfil) DO NOTHING;

