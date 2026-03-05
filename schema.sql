CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS items (
    id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    type          VARCHAR     NOT NULL CHECK (type IN ('finder', 'loser')),
    item_type     VARCHAR     NOT NULL,
    color         TEXT[]      NOT NULL,
    material      VARCHAR,
    size          VARCHAR,
    features      TEXT[],
    status        VARCHAR     NOT NULL DEFAULT 'active',
    expires_at    TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '30 days'),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    embedding     vector(1024)
);
