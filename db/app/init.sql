\c db;

CREATE TABLE IF NOT EXISTS matches (
    id SERIAL NOT NULL,
    team_1 VARCHAR(20),
    team_2 VARCHAR(20),
    goals_1 VARCHAR(20),
    goals_2 VARCHAR(20),
    datetime TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    cpf VARCHAR(20) NOT NULL,
    name VARCHAR(20) NOT NULL,
    admin_access BOOLEAN NOT NULL,
    payment_status BOOLEAN NOT NULL,
    guesses JSON,
    score SERIAL NOT NULL
);

INSERT INTO 
    users (cpf, name, admin_access, payment_status, score) 
VALUES 
    ('42431892859', 'Leonardo Godói', true, true, 0),
    ('00000000000', 'Fulano de Tal', false, false, 0);

INSERT INTO 
    matches (id, team_1, team_2, datetime) 
VALUES 
    (1, 'Catar', 'Equador', '2022-11-20 13:00:00'),
    (2, 'Inglaterra', 'Irã', '2022-11-21 10:00:00'),
    (3, 'Senegal', 'Holanda', '2022-11-21 13:00:00'),
    (4, 'Estados Unidos', 'País de Gales', '2022-11-21 16:00:00'),
    (5, 'Argentina', 'Arábia Saudita', '2022-11-22 07:00:00'),
    (6, 'Dinamarca', 'Tunísia', '2022-11-22 10:00:00'),
    (7, 'México', 'Polônia', '2022-11-22 13:00:00'),
    (8, 'França', 'Austrália', '2022-11-22 16:00:00'),
    (9, 'Marrocos', 'Croácia', '2022-11-23 07:00:00'),
    (10, 'Alemanha', 'Japão', '2022-11-23 10:00:00'),
    (11, 'Espanha', 'Costa Rica', '2022-11-23 13:00:00'),
    (12, 'Bélgica', 'Canadá', '2022-11-23 16:00:00'),
    (13, 'Suíça', 'Camarões', '2022-11-24 07:00:00'),
    (14, 'Uruguai', 'Coreia do Sul', '2022-11-24 10:00:00'),
    (15, 'Portugal', 'Gana', '2022-11-24 13:00:00'),
    (16, 'Brasil', 'Sérvia', '2022-11-24 16:00:00'),
    (17, 'País de Gales', 'Irã', '2022-11-25 07:00:00'),
    (18, 'Catar', 'Senegal', '2022-11-25 10:00:00'),
    (19, 'Holanda', 'Equador', '2022-11-25 13:00:00'),
    (20, 'Inglaterra', 'Estados Unidos', '2022-11-25 16:00:00'),
    (21, 'Tunísia', 'Austrália', '2022-11-26 07:00:00'),
    (22, 'Polônia', 'Arábia Saudita', '2022-11-26 10:00:00'),
    (23, 'França', 'Dinamarca', '2022-11-26 13:00:00'),
    (24, 'Argentina', 'México', '2022-11-26 16:00:00'),
    (25, 'Japão', 'Costa Rica', '2022-11-27 07:00:00'),
    (26, 'Bélgica', 'Marrocos', '2022-11-27 10:00:00'),
    (27, 'Croácia', 'Canadá', '2022-11-27 13:00:00'),
    (28, 'Espanha', 'Alemanha', '2022-11-27 16:00:00'),
    (29, 'Camarões', 'Sérvia', '2022-11-28 07:00:00'),
    (30, 'Coreia do Sul', 'Gana', '2022-11-28 10:00:00'),
    (31, 'Brasil', 'Sérvia', '2022-11-28 13:00:00'),
    (32, 'Portugal', 'Uruguai', '2022-11-28 16:00:00'),
    (33, 'Equador', 'Senegal', '2022-11-29 12:00:00'),
    (34, 'Holanda', 'Catar', '2022-11-29 12:00:00'),
    (35, 'Irã', 'Estados Unidos', '2022-11-29 16:00:00'),
    (36, 'País de Gales', 'Inglaterra', '2022-11-29 16:00:00'),
    (37, 'Tunísia', 'França', '2022-11-30 12:00:00'),
    (38, 'Austrália', 'Dinamarca', '2022-11-30 12:00:00'),
    (39, 'Polônia', 'Argentina', '2022-11-30 16:00:00'),
    (40, 'Arábia Saudita', 'México', '2022-11-30 16:00:00'),
    (41, 'Croácia', 'Bélgica', '2022-11-30 12:00:00'),
    (42, 'Canadá', 'Marrocos', '2022-12-01 12:00:00'),
    (43, 'Japão', 'Espanha', '2022-12-01 16:00:00'),
    (44, 'Alemanha', 'Costa Rica', '2022-12-01 16:00:00'),
    (45, 'Coreia do Sul', 'Portugal', '2022-12-01 12:00:00'),
    (46, 'Gana', 'Uruguai', '2022-12-02 12:00:00'),
    (47, 'Sérvia', 'Suíça', '2022-12-02 16:00:00'),
    (48, 'Camarões', 'Brasil', '2022-12-02 16:00:00');


