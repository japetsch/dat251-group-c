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

INSERT INTO admin DEFAULT VALUES;
INSERT INTO admin DEFAULT VALUES;

INSERT INTO "user" (name, email, phone_number, home_address_id, donor_id, password_hash) VALUES
  ('Olav', 'olav@uib.no', '1558', 1, 1,
  '$argon2id$v=19$m=65536,t=3,p=4$lkskS9KtvekaU2KS/hu/gQ$aisdna1C+MKgGbrWkSX7KiXsPpmxw7qhyTQpSautURk'), -- correct horse battery staple
  ('Peter', 'peter@hvl.no', '5087', 1, 2,
  '$argon2id$v=19$m=65536,t=3,p=4$9bAwJofIZtg7Fg9IH8uaRA$JfLTCeW8e/pNiXpRKj4A18Niz02XzuMbu1bnPcbUJ4M'), -- password123
  ('Sigrid', 'sigrid@gmain.com', '5571', 1, 3,
  '$argon2id$v=19$m=65536,t=3,p=4$llmunGw2K2kWx9Vhv/7OZQ$e4nkzeV3j1dRshEHsuNIsYp+FF6UwMyb6lDu04ecISQ'); -- hunter2

INSERT INTO "user" (name, email, phone_number, home_address_id, admin_id, password_hash) VALUES
  ('AdminHaukeland', 'admin@haukeland.no', '911', 2, 1, '$argon2id$v=19$m=65536,t=3,p=4$llmunGw2K2kWx9Vhv/7OZQ$e4nkzeV3j1dRshEHsuNIsYp+FF6UwMyb6lDu04ecISQ'), -- hunter2
  ('AdminBlodbuss', 'admin@blodbuss.no', '112', 3, 2, '$argon2id$v=19$m=65536,t=3,p=4$llmunGw2K2kWx9Vhv/7OZQ$e4nkzeV3j1dRshEHsuNIsYp+FF6UwMyb6lDu04ecISQ'); -- hunter2

-- admin_id 1 (AdminHaukeland) -> bloodbank_id 1 (Haukeland)
-- admin_id 2 (AdminBlodbuss) -> bloodbank_id 2 (Blodbussen)
INSERT INTO bloodbank_admin (bloodbank_id, admin_id) VALUES
  (1, 1),
  (2, 2);

INSERT into bookingslot (bloodbank_id, time, duration, capacity) VALUES
  (1, '2026-02-20T16:00:00Z', '00:30:00', 10),
  (1, '2026-05-11T11:30:00Z', '00:30:00', 10),
  (1, '2026-12-05T06:00:00Z', '00:30:00', 10),
  (1, '2026-12-05T06:00:00Z', '00:30:00', 0),
  (1, '2026-6-21T06:00:00Z', '00:30:00', 10);

INSERT into appointment (bookingslot_id, cancelled, donor_id) VALUES
  (1, false, 1),
  (2, true, 2),
  (3, false, 3);

-- NOTE: author_id is user.id, not admin.id or donor.id
INSERT INTO appointment_note (appointment_id, author_id, message, time) VALUES
  (1, 1, 'Hi my name is Olav!', '2026-02-18T10:00:00Z'),
  (1, 4, 'Hi, I am AdminHaukeland!', '2026-02-18T14:30:00Z'),
  (3, 3, 'My name is Sigrid, and I''m secretly a time traveller', '2026-12-01T09:00:00Z');

INSERT INTO interview (interviewer_admin_id) VALUES
	(1),
	(1);

INSERT INTO entry_form DEFAULT VALUES;

INSERT INTO entry_form DEFAULT VALUES;

INSERT INTO donation (appointment_id, amount_ml, is_blood_not_plasma) VALUES
	(1, 20, true),
	(2, 10, false);

INSERT INTO donation_test (donation_id, tester_admin_id) VALUES
	(1, 1),
	(2, 2);

INSERT INTO form (ok_to_donate, interview_id) VALUES
	(false, 1),
	(true, 2);

INSERT INTO form (ok_to_donate, entry_form_id) VALUES
	(true, 1),
	(true, 2);

INSERT INTO form (ok_to_donate, donation_test_id) VALUES
	(true, 1),
	(true, 2);

INSERT INTO test_result (donor_id, form_id, time, validity_duration, invalidated) VALUES
	(1, 1, '2025-04-30T10:00:00Z', '6 months', true),
	(2, 2, '2025-06-13T12:00:00Z', '6 months', false),
	(2, 3, '2026-01-02T09:00:00Z', '6 months', false),
	(2, 4, '2025-09-09T15:00:00Z', '6 months', false),
	(1, 5, '2026-02-20T16:00:00Z', '6 months', false), -- TODO: make sure donor id fits to appointment
	(2, 6, '2026-02-20T16:00:00Z', '6 months', false);
