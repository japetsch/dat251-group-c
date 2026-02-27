\c bloodbank_test

INSERT INTO "user" (name) VALUES
  ('Olav'),
  ('Peter'),
  ('Sigrid');  

INSERT INTO bloodbank (name) VALUES
  ('Haukeland'),
  ('Stavanger'),
  ('Oslo');

INSERT INTO appointment (user_id, location_id, time) VALUES 
  (1, 2, '2026-02-20 16:00:00'),
  (3, 1, '2026-05-11 11:30:00'),
  (2, 3, '2026-12-05 06:00:00');
