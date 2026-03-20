-- LOFO for Schools MVP — run in Supabase SQL editor (additive only)

CREATE TABLE IF NOT EXISTS schools (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    slug VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    pickup_info TEXT,
    admin_passcode_hash VARCHAR,
    admin_notify_email VARCHAR,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS school_subscriptions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    email VARCHAR NOT NULL,
    parent_name VARCHAR,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (school_id, email)
);

CREATE TABLE IF NOT EXISTS school_claims (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    item_id UUID NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    child_name VARCHAR,
    parent_name VARCHAR,
    parent_email VARCHAR NOT NULL,
    claim_note TEXT,
    status VARCHAR NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS school_lost_pending (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    parent_email VARCHAR NOT NULL,
    parent_name VARCHAR,
    child_name VARCHAR,
    loser_item_id UUID NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE items ADD COLUMN IF NOT EXISTS school_id UUID REFERENCES schools(id);

CREATE INDEX IF NOT EXISTS idx_items_school_id ON items (school_id) WHERE school_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_school_claims_school ON school_claims (school_id);
CREATE INDEX IF NOT EXISTS idx_school_lost_pending_school ON school_lost_pending (school_id);
