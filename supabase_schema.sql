-- Create events table
CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  date DATE NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  location TEXT NOT NULL,
  description TEXT NOT NULL,
  image_url TEXT,
  tags TEXT[] DEFAULT '{}',
  is_featured BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create a trigger to update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_events_updated_at
BEFORE UPDATE ON events
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Create simple RLS (Row Level Security) policies
-- This allows anyone to read and create events, but no one can update or delete them
-- You can implement admin functionality later when needed

-- Enable RLS on the events table
ALTER TABLE events ENABLE ROW LEVEL SECURITY;

-- Create a policy to allow anyone to read events
CREATE POLICY "Allow public read access" ON events
FOR SELECT
USING (true);

-- Create a policy to allow anyone to insert events
CREATE POLICY "Allow public insert access" ON events
FOR INSERT
WITH CHECK (true);

-- Add indexes for performance
CREATE INDEX idx_events_date ON events(date);
CREATE INDEX idx_events_tags ON events USING GIN(tags);

-- Create a function to get events filtered by tag
CREATE OR REPLACE FUNCTION get_events_by_tag(tag_filter TEXT)
RETURNS SETOF events AS $$
BEGIN
  IF tag_filter = 'all' THEN
    RETURN QUERY 
    SELECT * FROM events 
    WHERE date >= CURRENT_DATE
    ORDER BY date ASC, start_time ASC;
  ELSE
    RETURN QUERY 
    SELECT * FROM events 
    WHERE date >= CURRENT_DATE AND tag_filter = ANY(tags)
    ORDER BY date ASC, start_time ASC;
  END IF;
END;
$$ LANGUAGE plpgsql;

-- Create a helper function to get current server time (for connection testing)
CREATE OR REPLACE FUNCTION now()
RETURNS TIMESTAMP WITH TIME ZONE
LANGUAGE SQL
AS $$
  SELECT NOW();
$$; 