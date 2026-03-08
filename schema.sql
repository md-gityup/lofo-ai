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
ALTER TABLE items ADD COLUMN IF NOT EXISTS finder_email VARCHAR;

-- Phase 10b: SMS notifications
ALTER TABLE items ADD COLUMN IF NOT EXISTS phone VARCHAR;

-- Phase 11: Stripe Connect payouts (deprecated — kept for rollback)
ALTER TABLE items ADD COLUMN IF NOT EXISTS stripe_connect_account_id VARCHAR;

-- Phase 11b: Simple payout handle (Venmo / PayPal / Cash App / Zelle)
ALTER TABLE items ADD COLUMN IF NOT EXISTS finder_payout_app VARCHAR;
ALTER TABLE items ADD COLUMN IF NOT EXISTS finder_payout_handle VARCHAR;

-- Phase 12: Reunion relay — maps verified matches to a two-way SMS relay
CREATE TABLE IF NOT EXISTS reunions (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    finder_item_id   UUID        NOT NULL REFERENCES items(id),
    loser_item_id    UUID        NOT NULL REFERENCES items(id),
    finder_phone     VARCHAR     NOT NULL,
    loser_phone      VARCHAR     NOT NULL,
    status           VARCHAR     NOT NULL DEFAULT 'active',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at       TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '7 days')
);

CREATE INDEX IF NOT EXISTS reunions_finder_phone_idx ON reunions(finder_phone);
CREATE INDEX IF NOT EXISTS reunions_loser_phone_idx  ON reunions(loser_phone);

CREATE TABLE IF NOT EXISTS tips (
    id                        UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    finder_item_id            UUID        NOT NULL REFERENCES items(id),
    loser_item_id             UUID        NOT NULL REFERENCES items(id),
    amount_cents              INTEGER     NOT NULL,
    stripe_payment_intent_id  VARCHAR     UNIQUE,
    status                    VARCHAR     NOT NULL DEFAULT 'pending',
    created_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
