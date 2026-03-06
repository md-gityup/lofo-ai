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

-- Phase 7: tip flow
-- Run these ALTER statements if the table already exists:
--   ALTER TABLE items ADD COLUMN IF NOT EXISTS finder_email VARCHAR;
ALTER TABLE items ADD COLUMN IF NOT EXISTS finder_email VARCHAR;

CREATE TABLE IF NOT EXISTS tips (
    id                        UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    finder_item_id            UUID        NOT NULL REFERENCES items(id),
    loser_item_id             UUID        NOT NULL REFERENCES items(id),
    amount_cents              INTEGER     NOT NULL,
    stripe_payment_intent_id  VARCHAR     UNIQUE,
    status                    VARCHAR     NOT NULL DEFAULT 'pending',
    created_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
