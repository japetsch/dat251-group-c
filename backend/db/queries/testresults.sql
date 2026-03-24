-- name: TestResults :many
SELECT * FROM test_result t WHERE t.donor_id = sqlc.arg(donor_id);

-- name: TestResult :one
SELECT 
	t.id as id,
	t.donor_id as donor_id,
	t.form_id as form_id,
	t.time as time,
	t.validity_duration as validity_duration,
	t.invalidated as invalidated,
	f.ok_to_donate as ok_to_donate,
	f.interview_id as interview_id,
	f.entry_form_id as entry_form_id,
	f.donation_test_id as donation_test_id,
	i.interviewer_admin_id as interviewer_admin_id,
	d.donation_id as donation_id,
	don.appointment_id as appointment_id,
	don.amount_ml as amount_ml,
	don.is_blood_not_plasma as is_blood_not_plasma
 FROM test_result t
	INNER JOIN form f ON t.form_id = f.id
	LEFT JOIN interview i ON f.interview_id = i.id
	LEFT JOIN entry_form e ON f.entry_form_id = e.id
	LEFT JOIN donation_test d ON f.donation_test_id = d.id
	LEFT JOIN donation don ON d.donation_id = don.id
	WHERE t.id = sqlc.arg(testresult_id);
