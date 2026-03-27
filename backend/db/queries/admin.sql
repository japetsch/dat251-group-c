-- name: CreateBloodBank :one
WITH addr AS (
    INSERT INTO address (street_name, street_number, postal_code, city, country)
    VALUES ($1, $2, $3, $4, $5)
    RETURNING id
),
loc AS (
    INSERT INTO location (latitude, longitude, address_id)
    VALUES ($6, $7, (SELECT id FROM addr))
    RETURNING id
),
bank AS (
    INSERT INTO bloodbank (name, location_id)
    VALUES ($8, (SELECT id FROM loc))
    RETURNING id
)
INSERT INTO bloodbank_admin (bloodbank_id, admin_id)
VALUES ((SELECT id FROM bank), $9)
RETURNING bloodbank_id;

-- name: AddBloodBankAdmin :exec
INSERT INTO bloodbank_admin (bloodbank_id, admin_id)
VALUES ($1, $2);

-- name: RemoveBloodBankAdmin :one
DELETE FROM bloodbank_admin bba
WHERE bba.bloodbank_id = sqlc.arg(bloodbank_id) AND
    bba.admin_id = sqlc.arg(admin_id) AND
    (SELECT count(id) FROM bloodbank_admin WHERE bloodbank_id = sqlc.arg(bloodbank_id)) > 1
RETURNING bba.admin_id;

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
                'author_user_id', nu.id,
                'author_name', nu.name,
                'message', an.message,
                'time', an.time
            ) ORDER BY an.time DESC), '[]'::json)
            FROM appointment_note an
            INNER JOIN "user" nu ON an.author_id = nu.id
            WHERE an.appointment_id = a.id
        ),
        'donations', (
            SELECT COALESCE(json_agg(json_build_object(
                'donation_id', dn.id,
                'amount_ml', dn.amount_ml,
                'is_blood_not_plasma', dn.is_blood_not_plasma
                -- TODO: testing status
            ) ORDER BY dn.id), '[]'::json)
            FROM donation dn
            WHERE dn.appointment_id = a.id
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

-- name: RegisterDonation :one
INSERT INTO donation (appointment_id, amount_ml, is_blood_not_plasma)
VALUES ($1, $2, $3)
RETURNING id;

-- name: RegisterInterview :exec
WITH iv AS (
    INSERT INTO interview (interviewer_admin_id)
    VALUES ($1) RETURNING id
), f AS (
    INSERT INTO form (ok_to_donate, interview_id)
    VALUES ($3, (SELECT id FROM iv))
    RETURNING id
)
INSERT INTO test_result (donor_id, form_id, time, validity_duration)
VALUES ($2, (SELECT id FROM f), $4, $5);

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
    VALUES ($4, (SELECT id FROM dt))
    RETURNING id
)
INSERT INTO test_result (donor_id, form_id, time, validity_duration)
VALUES ($3, (SELECT id FROM f), $5, $6);
