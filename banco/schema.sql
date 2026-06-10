
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200),
    cpf VARCHAR(14) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notas (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    chave_danfe VARCHAR(44) UNIQUE NOT NULL,
    tipo VARCHAR(20) NOT NULL, -- 'PRODUTO' ou 'SERVICO'
    valor DECIMAL(10,2),
    data_emissao TIMESTAMP,
    processada BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cupons (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    nota_id INTEGER REFERENCES notas(id),
    numero_cupom BIGINT UNIQUE NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
