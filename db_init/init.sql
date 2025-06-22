-- db_init/init.sql

-- Create the resources table if it doesn't exist
CREATE TABLE IF NOT EXISTS resources (
    id SERIAL PRIMARY KEY,      -- Auto-incrementing primary key
    title VARCHAR(255) NOT NULL,
    type VARCHAR(255),
    date DATE,
    authors JSONB,              -- Store list of authors as JSONB for flexibility
    abstract TEXT,
    doi VARCHAR(255) UNIQUE,    -- Assuming DOI should be unique
    url TEXT,                   -- Store URL as plain text (VARCHAR is also fine)
    keywords JSONB,             -- Store list of keywords as JSONB
    provider VARCHAR(255),
    fulltext TEXT
);

CREATE TABLE IF NOT EXISTS exhibits (
    id SERIAL PRIMARY KEY,      -- Auto-incrementing primary key
    slug VARCHAR(255) UNIQUE NOT NULL, -- Unique slug for the exhibit
    title VARCHAR(255) NOT NULL,
    descritpion TEXT,
    narrative TEXT,
    content TEXT,
    resources JSONB,          -- Store resources as JSONB for flexibility
    date DATE
);

-- Add any other tables or initial data here if needed
-- For example, if you have other tables like 'users', 'topics', etc., define them here as well.