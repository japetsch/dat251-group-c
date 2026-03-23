-- name: GetBookingSlots :many
SELECT
    s.id,
    s.time,
    s.duration,
    s.capacity,
    s.bloodbank_id,
    b.name AS bloodbank_name,
	b.location_id
FROM bookingslot s
  INNER JOIN bloodbank b ON b.id = s.bloodbank_id
  ORDER BY s.time ASC;

-- name: BookBookingslot :one
WITH slot AS (
    UPDATE bookingslot 
    SET capacity = capacity - 1
    WHERE bookingslot.id = sqlc.arg(bookingslot_id) AND bookingslot.capacity > 0
    RETURNING id as bookingslot_id
)
INSERT INTO appointment (donor_id, bookingslot_id, cancelled)
SELECT sqlc.arg(donor_id), slot.bookingslot_id, FALSE
FROM slot
RETURNING id, donor_id, bookingslot_id, cancelled;
