-- name: GetUser :one
SELECT u.id, u.name, u.email, u.password_hash, u.donor_id, u.admin_id
FROM "user" u WHERE u.email = $1;

-- name: AppointmentBelongsTo :one
SELECT TRUE
FROM appointment a
WHERE a.id = sqlc.arg(appointment_id) AND a.donor_id = sqlc.arg(donor_id);