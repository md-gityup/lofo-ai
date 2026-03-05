-- Enable pgvector extension (safe to re-run)
CREATE EXTENSION IF NOT EXISTS vector;

-- Add embedding column to items table
ALTER TABLE items
    ADD COLUMN IF NOT EXISTS embedding vector(1024);
