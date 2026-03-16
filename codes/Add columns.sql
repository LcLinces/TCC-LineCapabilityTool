-- SQLite
ALTER TABLE maquinas ADD COLUMN tipo                TEXT;
ALTER TABLE maquinas ADD COLUMN tensao_v            INTEGER;
ALTER TABLE maquinas ADD COLUMN frequencia_hz       INTEGER;
ALTER TABLE maquinas ADD COLUMN potencia            FLOAT;
ALTER TABLE maquinas ADD COLUMN unidade_potencia    TEXT;
