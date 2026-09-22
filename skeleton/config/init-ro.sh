#!/bin/bash
# 최초 기동 시 1회 실행: 샘플 테이블 + 조회 전용 계정. 보안 협의에서 "최소 권한" 근거가 된다.
set -e
psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<SQL
CREATE TABLE IF NOT EXISTS sample_records (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    amount NUMERIC(14,2),
    created_at TIMESTAMPTZ DEFAULT now()
);
INSERT INTO sample_records (title, amount) VALUES
    ('샘플 계약 A', 1200000), ('샘플 계약 B', 830000), ('샘플 계약 C', 45000000);

CREATE USER ro_user WITH PASSWORD '${RO_DB_PASSWORD:-ro_pass}';
GRANT CONNECT ON DATABASE appdb TO ro_user;
GRANT USAGE ON SCHEMA public TO ro_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ro_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO ro_user;
SQL
