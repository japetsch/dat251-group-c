-- name: GetAllAppointments :many
SELECT u.name as username, b.name as locationname, a.time FROM appointment a
	INNER JOIN user u on a.user_id = u.id
	INNER JOIN bloodbank b on a.location_id = b.id;
