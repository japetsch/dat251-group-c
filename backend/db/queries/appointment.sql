-- name: GetAppointmentsByUserId :many
SELECT a.id as id, u.name as username, b.time as time, b.duration as duration, ba.name as bloodbank_name, a.cancelled FROM appointment a
  INNER JOIN "user" u on a.donor_id = u.id
  INNER JOIN bookingslot b on a.bookingslot_id = b.id
  INNER JOIN bloodbank ba on b.bloodbank_id = ba.id
  WHERE a.donor_id = sqlc.arg('donor_id');

-- name: UpdateAppointment :one
WITH current AS (
    SELECT bookingslot_id AS old_slot
    FROM appointment
    WHERE appointment.id = sqlc.arg(id)
),
updated_appointment AS (
    UPDATE appointment
    SET 
        cancelled = sqlc.arg(cancelled),
        bookingslot_id = sqlc.arg(bookingslot_id)
    WHERE appointment.id = sqlc.arg(id)
      AND (
          -- allow if same slot
          (SELECT old_slot FROM current) = sqlc.arg(bookingslot_id)
          OR
          -- or new slot has capacity
          EXISTS (
              SELECT 1
              FROM bookingslot
              WHERE bookingslot.id = sqlc.arg(bookingslot_id)
                AND bookingslot.capacity > 0
          )
      )
    RETURNING *
),
decrease_new AS (
    UPDATE bookingslot
    SET capacity = capacity - 1
    WHERE bookingslot.id = sqlc.arg(bookingslot_id)
      AND bookingslot.id <> (SELECT old_slot FROM current)
      AND EXISTS (SELECT 1 FROM updated_appointment)
),
increase_old AS (
    UPDATE bookingslot
    SET capacity = capacity + 1
    WHERE bookingslot.id = (SELECT old_slot FROM current)
      AND bookingslot.id <> sqlc.arg(bookingslot_id)
      AND EXISTS (SELECT 1 FROM updated_appointment)
)
SELECT * FROM updated_appointment;

