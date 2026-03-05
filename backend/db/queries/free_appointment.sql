-- name: GetAvailableAppointments :many
SELECT
    fa.id,
    fa.time,
    fa.location_id,
    b.name AS locationname
FROM free_appointments fa
JOIN bloodbank b ON b.id = fa.location_id
ORDER BY fa.time ASC;
