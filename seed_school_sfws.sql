-- Seed San Francisco Waldorf School for LOFO for Schools MVP.
-- Run AFTER migration_school_mvp.sql
--
-- Default passcode: sfws-change-me  (CHANGE IMMEDIATELY in production)
-- To generate a new hash locally:
--   cd ~/Desktop/lofo-ai && source .venv/bin/activate && python3 -c "from security import hash_secret; print(hash_secret('YOUR_NEW_PASSCODE'))"
-- Then UPDATE schools SET admin_passcode_hash = '...' WHERE slug = 'sfws';

INSERT INTO schools (slug, name, pickup_info, admin_passcode_hash, admin_notify_email)
VALUES (
    'sfws',
    'San Francisco Waldorf School',
    'Main office — weekdays 8am–3pm. Ask at the front desk for lost & found.',
    '$argon2id$v=19$m=65536,t=2,p=2$LPEmnArc27Kn6Rx4HgmTZw$aua/pajhZYNd6WHY3ikdQKxoOdI/RLiONNTl0O9tLbU',
    NULL
)
ON CONFLICT (slug) DO NOTHING;
