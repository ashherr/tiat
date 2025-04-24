-- Create the events table with updated fields for Google Calendar integration
CREATE TABLE IF NOT EXISTS events (
    id bigint primary key generated always as identity,
    title varchar(200) not null,
    start_time timestamptz not null,
    end_time timestamptz not null,
    location varchar(200) not null,
    description text not null,
    image_url varchar(500) not null,
    event_link varchar(500) not null,
    tags varchar(500) not null,
    is_starred boolean default false,
    organizer_email varchar(200) not null,
    calendar_event_id varchar(200),
    created_at timestamptz default now()
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

-- Allow anyone to select (read) events
CREATE POLICY "Anyone can view events"
    ON events FOR SELECT
    TO anon, authenticated
    USING (true);

-- Only allow authenticated admin users to insert, update, or delete events
CREATE POLICY "Only admins can modify events"
    ON events FOR ALL
    TO authenticated
    USING (auth.uid() IN (SELECT auth.uid() FROM admin_users))
    WITH CHECK (auth.uid() IN (SELECT auth.uid() FROM admin_users));

-- In production, you would also need to create the admin_users table
-- and add your admin users to it 