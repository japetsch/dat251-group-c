-- uncomment following line and run: "cat ./tests/db_mocks.sql | docker exec -i postgres psql -h localhost -U postgres -f-" to add the mock data to your local DB
-- \c bloodbank

INSERT INTO address (street_name, street_number, postal_code, city, country) VALUES
  ('Bryggen', '5', '5003', 'Bergen', 'Norway'),
  ('Haukelandsveien', '22', '5009', 'Bergen', 'Norway'),
  ('Nonnesetergaten', '4', '5015', 'Bergen', 'Norway');

INSERT INTO location (latitude, longitude, address_id) VALUES
  (60.388937, 5.334812, 3),
  (60.373312, 5.359187, 2);

INSERT INTO bloodbank (name, location_id) VALUES 
  ('Haukeland universitetssjukehus', 2),
  ('Blodbussen Nonneseter', 1);

INSERT INTO donor (blood_type, preferred_bloodbank_id) VALUES
  ('O+', 1),
  ('O-', 2),
  ('AB+', 2),
  ('B-', 1);

INSERT INTO "user" (name, email, phone_number, home_address_id, donor_id) VALUES
  ('Olav', 'olav@uib.no', '1558', 1, 1),
  ('Peter', 'peter@hvl.no', '5087', 1, 2),
  ('Sigrid', 'sigrid@gmain.com', '5571', 1, 3);  

INSERT into bookingslot (bloodbank_id, time, duration, capacity) VALUES
  (1, '2026-02-20T16:00:00Z', '00:30:00', 10),
  (1, '2026-05-11T11:30:00Z', '00:30:00', 10),
  (1, '2026-12-05T06:00:00Z', '00:30:00', 10),
  (1, '2026-12-05T06:00:00Z', '00:30:00', 0);

INSERT into appointment (bookingslot_id, cancelled, donor_id) VALUES
  (1, false, 1),
  (2, true, 2),
  (3, false, 3);

