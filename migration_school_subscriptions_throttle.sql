-- Add last_notified_at to school_subscriptions
-- Tracks when each subscriber last received a new-item alert.
-- NULL = never notified (eligible immediately).
-- Backend only sends if last_notified_at IS NULL OR < NOW() - INTERVAL '24 hours'.
ALTER TABLE school_subscriptions
    ADD COLUMN IF NOT EXISTS last_notified_at TIMESTAMPTZ;
