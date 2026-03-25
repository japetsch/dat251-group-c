-- name: GetAllBloodBanks :many
SELECT b.name, a.street_name, a.street_number, a.postal_code, a.city, a.country,
    COUNT(bba.admin_id) > 0 AS user_has_admin_access
FROM bloodbank b
INNER JOIN location l ON b.location_id = l.id
INNER JOIN address a ON l.address_id = a.id
LEFT JOIN bloodbank_admin bba ON (b.id = bba.bloodbank_id AND bba.admin_id = $1)
GROUP BY b.id;

-- name: CreateBloodBank :one
WITH addr AS (
    INSERT INTO address (street_name, street_number, postal_code, city, country)
    VALUES ($1, $2, $3, $4, $5)
    RETURNING id
),
loc AS (
    INSERT INTO location (latitude, longitude, address_id)
    VALUES ($6, $7, addr.id)
    RETURNING id
),
bank AS (
    INSERT INTO bloodbank (name, location_id)
    VALUES ($8, loc.id)
    RETURNING id
)
INSERT INTO bloodbank_admin (bloodbank_id, admin_id)
VALUES (bank.id, $9)
RETURNING bloodbank_id;

-- name: AddBloodBankAdmin :exec
INSERT INTO bloodbank_admin (bloodbank_id, admin_id)
VALUES ($1, $2);

-- name: RemoveBloodBankAdmin :exec
WITH admin_ct AS (
    SELECT count(id) FROM bloodbank_admin
    WHERE bloodbank_id = sqlc.arg(bloodbank_id)
)
DELETE FROM bloodbank_admin bba
WHERE bba.bloodbank_id = sqlc.arg(bloodbank_id) AND
    bba.admin_id = sqlc.arg(admin_id) AND admin_ct > 1;

-- name: GetAppointmentsAtBloodBank :many
SELECT bs.id as bookingslot_id, bs.time as bookingslot_time,
    bs.duration as bookingslot_duration,
    bs.capacity as bookingslot_remaining_capacity,
    json_agg(json_build_object(
        'appointment_id', a.id,
        'appointment_cancelled', a.cancelled,
        'donor_id', d.id,
        'donor_blood_type', d.blood_type,
        'donor_name', u.name,
        'donor_email', u.email,
        'donor_phone', u.phone_number,
        'notes', (
            SELECT COALESCE(json_agg(json_build_object(
                'author_name', u.name,
                'message', an.message,
                'time', an.time
            )), '[]'::json)
            FROM appointment_note an
            INNER JOIN "user" u ON an.author_id = u.id
            WHERE an.appointment_id = a.id
            ORDER BY an.time DESC
        )
    )) as appointments
FROM bookingslot bs
INNER JOIN appointment a ON a.bookingslot_id = bs.id
INNER JOIN donor d ON a.donor_id = d.id
INNER JOIN "user" u ON u.donor_id = d.id
WHERE bs.bloodbank_id = $1 AND bs.time >= sqlc.arg(after)
    AND (sqlc.narg(before)::TIMESTAMP WITH TIME ZONE IS NULL
        OR sqlc.narg(before) >= bs.time)
    AND (sqlc.arg(show_cancelled)::BOOLEAN OR NOT a.cancelled)
GROUP BY bs.id;

-- name: AddAppointmentNote :exec
INSERT INTO appointment_note (appointment_id, author_id, message, time)
VALUES ($1, $2, $3, NOW());

-- name: RegisterDonation :exec
INSERT INTO donation (appointment_id, amount_ml, is_blood_not_plasma)
VALUES ($1, $2, $3);

-- name: RegisterInterview :exec
WITH iv AS (
    INSERT INTO interview (interviewer_admin_id)
    VALUES ($1) RETURNING id
), f AS (
    INSERT INTO form (ok_to_donate, interview_id)
    VALUES ($3, iv)
    RETURNING id
)
INSERT INTO test_result (donor_id, form_id, time, validity_duration)
VALUES ($2, f, $4, $5);

-- name: GetDonationInfo :one
SELECT a.donor_id, b.id as bloodbank_id
FROM donation d
INNER JOIN appointment a ON d.appointment_id = a.id
INNER JOIN bookingslot bs ON a.bookingslot_id = bs.id
INNER JOIN bloodbank b ON bs.bloodbank_id = b.id
WHERE d.id = sqlc.arg(donation_id);

-- name: RegisterDonationTest :exec
WITH dt AS (
    INSERT INTO donation_test (donation_id, tester_admin_id)
    VALUES ($1, $2)
    RETURNING id
), f AS (
    INSERT INTO form (ok_to_donate, donation_test_id)
    VALUES ($4, dt)
    RETURNING id
)
INSERT INTO test_result (donor_id, form_id, time, validity_duration)
VALUES ($3, f, $5, $6);
