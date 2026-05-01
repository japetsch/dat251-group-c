-- uncomment following line and run: "cat ./tests/db_mocks.sql | docker exec -i postgres psql -h localhost -U postgres -f-" to add the mock data to your local DB
\c bloodbank

INSERT INTO address (street_name, street_number, postal_code, city, country) VALUES
  ('Strangebakken', '8', '5011', 'Bergen', 'Norway'),
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
  ('B-', 1),
  ('B-', 1);

INSERT INTO admin DEFAULT VALUES;
INSERT INTO admin DEFAULT VALUES;

INSERT INTO "user" (name, email, phone_number, home_address_id, donor_id, password_hash) VALUES
  ('Jannis', 'jannis@uib.no', '+47 12 43 35 64', 1, 1,
  '$argon2id$v=19$m=65536,t=3,p=4$llmunGw2K2kWx9Vhv/7OZQ$e4nkzeV3j1dRshEHsuNIsYp+FF6UwMyb6lDu04ecISQ'), -- hunter2
  ('Olav', 'olav@uib.no', '1558', 1, 2,
  '$argon2id$v=19$m=65536,t=3,p=4$lkskS9KtvekaU2KS/hu/gQ$aisdna1C+MKgGbrWkSX7KiXsPpmxw7qhyTQpSautURk'), -- correct horse battery staple
  ('Peter', 'peter@hvl.no', '5087', 1, 3,
  '$argon2id$v=19$m=65536,t=3,p=4$9bAwJofIZtg7Fg9IH8uaRA$JfLTCeW8e/pNiXpRKj4A18Niz02XzuMbu1bnPcbUJ4M'), -- password123
  ('Sigrid', 'sigrid@gmain.com', '5571', 1, 4,
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
  (1, '2026-01-01T09:00:00Z', '00:30:00', 10);

-- Haukeland
INSERT INTO bookingslot (bloodbank_id, time, duration, capacity)
SELECT
    1,
    day + slot_offset AS time,
    INTERVAL '30 minutes',
    capacity
FROM (
    -- Generate all days in range
    SELECT generate_series(
        TIMESTAMP '2026-04-30',
        TIMESTAMP '2026-05-21',  -- ~3 weeks
        INTERVAL '1 day'
    ) AS day
) d
JOIN (
    -- Define 4 slots per day with different times + capacities
    VALUES
        (INTERVAL '08:00', 8),
        (INTERVAL '10:00', 10),
        (INTERVAL '12:00', 6),
        (INTERVAL '14:00', 12)
) AS slots(slot_offset, capacity)
ON TRUE
WHERE EXTRACT(ISODOW FROM day) IN (2, 3, 5); -- Tue=2, Wed=3, Fri=5
-- The same in 4 months
INSERT INTO bookingslot (bloodbank_id, time, duration, capacity)
SELECT
    1,
    day + slot_offset AS time,
    INTERVAL '30 minutes',
    capacity
FROM (
    -- Generate all days in range
    SELECT generate_series(
        TIMESTAMP '2026-08-30',
        TIMESTAMP '2026-09-21',  -- ~3 weeks
        INTERVAL '1 day'
    ) AS day
) d
JOIN (
    -- Define 4 slots per day with different times + capacities
    VALUES
        (INTERVAL '08:00', 8),
        (INTERVAL '10:00', 10),
        (INTERVAL '12:00', 6),
        (INTERVAL '14:00', 12)
) AS slots(slot_offset, capacity)
ON TRUE
WHERE EXTRACT(ISODOW FROM day) IN (2, 3, 5); -- Tue=2, Wed=3, Fri=5

-- Blodbus
INSERT INTO bookingslot (bloodbank_id, time, duration, capacity)
SELECT
    2,
    day + slot_offset AS time,
    INTERVAL '30 minutes',
    capacity
FROM (
    -- Generate all days in range
    SELECT generate_series(
        TIMESTAMP '2026-04-30',
        TIMESTAMP '2026-05-21',  -- ~3 weeks
        INTERVAL '1 day'
    ) AS day
) d
JOIN (
    -- Define 4 slots per day with different times + capacities
    VALUES
        (INTERVAL '09:00', 8),
        (INTERVAL '12:00', 10),
        (INTERVAL '16:00', 6)
) AS slots(slot_offset, capacity)
ON TRUE
WHERE EXTRACT(ISODOW FROM day) IN (1, 2, 3, 4);

INSERT into appointment (bookingslot_id, cancelled, donor_id) VALUES
  (1, false, 1),
  (5, false, 1),
  (4, true, 2),
  (7, false, 3);

-- NOTE: author_id is user.id, not admin.id or donor.id
INSERT INTO appointment_note (appointment_id, author_id, message, time) VALUES
  (1, 5, 'Your blood results are there!', '2026-01-18T10:00:00Z'),
  (2, 5, 'Please remember bringing the documents', '2026-02-18T10:00:00Z'),
  (2, 1, 'Yes, I will bring them', '2026-02-19T10:00:00Z');

INSERT INTO interview (interviewer_admin_id) VALUES
	(1),
	(1);

INSERT INTO entry_form DEFAULT VALUES;

INSERT INTO entry_form DEFAULT VALUES;

INSERT INTO donation (appointment_id, amount_ml, is_blood_not_plasma) VALUES
	(1, 20, true);

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
	(1, 5, '2026-01-18T10:00:00Z', '6 months', false), -- TODO: make sure donor id fits to appointment
	(2, 6, '2026-02-20T16:00:00Z', '6 months', false);
