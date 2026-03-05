-- name: GetAllAppointments :many
SELECT a.id as id, u.name as username, b.name as locationname, a.time FROM appointment a
	INNER JOIN "user" u on a.user_id = u.id
	INNER JOIN bloodbank b on a.location_id = b.id;

-- name: DeleteAppointmentById :one
DELETE FROM appointment a WHERE a.id=sqlc.arg('id') RETURNING *;

-- name: UpdateAppointment :one
UPDATE appointment
SET time=sqlc.arg('time')
WHERE id=sqlc.arg('id')
RETURNING *;

-- name: BookAppointment :one
WITH slot AS (
    DELETE FROM free_appointments fa
    WHERE fa.id = sqlc.arg('free_appointment_id')
    RETURNING fa.time, fa.location_id
)
INSERT INTO appointment (user_id, time, location_id)
SELECT sqlc.arg('user_id'), slot.time, slot.location_id
FROM slot
RETURNING id, user_id, time, location_id;

