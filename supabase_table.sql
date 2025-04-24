-- Create the events table in Supabase
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    location TEXT NOT NULL,
    description TEXT NOT NULL,
    image_url TEXT NOT NULL,
    event_link TEXT NOT NULL,
    tags TEXT NOT NULL,
    is_starred BOOLEAN DEFAULT FALSE
);

-- Create index on start_time for faster queries by date
CREATE INDEX IF NOT EXISTS idx_events_start_time ON events (start_time);

-- Enable Row Level Security
ALTER TABLE events ENABLE ROW LEVEL SECURITY;

-- Clear existing policies if they exist
DROP POLICY IF EXISTS "Allow anonymous read access" ON events;
DROP POLICY IF EXISTS "Allow authenticated insert" ON events;
DROP POLICY IF EXISTS "Allow service role full access" ON events;
DROP POLICY IF EXISTS "Allow anonymous insert" ON events;

-- Create policy to allow anyone to read events
CREATE POLICY "Allow anonymous read access" ON events
    FOR SELECT
    TO anon
    USING (true);

-- Create policy to allow anonymous inserts (anyone can submit an event)
CREATE POLICY "Allow anonymous insert" ON events
    FOR INSERT
    TO anon
    WITH CHECK (true);

-- Create policy to allow authenticated users to create events
CREATE POLICY "Allow authenticated insert" ON events
    FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- Create policy to allow service role to do everything
CREATE POLICY "Allow service role full access" ON events
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true); 