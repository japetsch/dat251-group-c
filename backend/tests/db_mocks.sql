-- uncomment following line and run: "cat ./tests/db_mocks.sql | docker exec -i postgres psql -h localhost -U postgres -f-" to add the mock data to your local DB
-- \c bloodbank

INSERT INTO "user" (name) VALUES
  ('Olav'),
  ('Peter'),
  ('Sigrid');  

INSERT INTO bloodbank (name) VALUES
  ('Haukeland'),
  ('Stavanger'),
  ('Oslo');

INSERT INTO appointment (user_id, location_id, time) VALUES 
  (1, 2, '2026-02-20T16:00:00Z'),
  (3, 1, '2026-05-11T11:30:00Z'),
  (2, 3, '2026-12-05T06:00:00Z');
