-- name: GetUser :one
SELECT u.id, u.name, u.email, u.password_hash, u.donor_id, u.admin_id
FROM "user" u WHERE u.email = $1;

-- name: AppointmentBelongsTo :one
SELECT TRUE
FROM appointment a
WHERE a.id = sqlc.arg(appointment_id) AND a.donor_id = sqlc.arg(donor_id);

-- name: TestResultBelongsTo :one
SELECT TRUE
FROM test_result t
	INNER JOIN form f ON t.form_id = f.id
	LEFT JOIN donation_test d ON f.donation_test_id = d.id
	LEFT JOIN donation don ON d.donation_id = don.id
	LEFT JOIN appointment a ON don.appointment_id = a.id
WHERE t.id = sqlc.arg(testresult_id) AND t.donor_id = sqlc.arg(donor_id) AND (a.donor_id = sqlc.arg(donor_id) OR a.donor_id IS NULL);
