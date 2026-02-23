CREATE TABLE IF NOT EXISTS "schema_migrations" (version varchar(128) primary key);
CREATE TABLE first_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    a TEXT
);
-- Dbmate schema migrations
INSERT INTO "schema_migrations" (version) VALUES
  ('20260220105542');
