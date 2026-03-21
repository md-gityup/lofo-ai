-- Phase: School URL token security
-- Replaces human-readable slug in public URLs with an unguessable 18-char hex token.
-- Run in Supabase SQL editor BEFORE deploying the updated main.py.

ALTER TABLE schools ADD COLUMN IF NOT EXISTS url_token VARCHAR(24) UNIQUE;

-- Generate a random 9-byte (18 hex char) token for any school that doesn't have one yet.
UPDATE schools
SET url_token = encode(gen_random_bytes(9), 'hex')
WHERE url_token IS NULL;

ALTER TABLE schools ALTER COLUMN url_token SET NOT NULL;
