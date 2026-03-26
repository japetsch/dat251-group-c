-- name: InterviewResult :many
SELECT 
	t.id as id,
	t.donor_id as donor_id,
	t.form_id as form_id,
	t.time as time,
	t.validity_duration as validity_duration,
	t.invalidated as invalidated,
	f.interview_id as interview_id,
	a.name as admin_name
FROM test_result t
INNER JOIN form f ON t.form_id = f.id
INNER JOIN interview i ON f.interview_id = i.id
INNER JOIN "user" a ON i.interviewer_admin_id = a.admin_id 
WHERE t.donor_id = sqlc.arg(donor_id) AND f.interview_id IS NOT NULL;

-- name: EntryFormResult :many
SELECT 
	t.id as id,
	t.donor_id as donor_id,
	t.form_id as form_id,
	t.time as time,
	t.validity_duration as validity_duration,
	t.invalidated as invalidated,
	f.entry_form_id as entry_form_id
FROM test_result t
INNER JOIN form f ON t.form_id = f.id
WHERE t.donor_id = sqlc.arg(donor_id) AND f.entry_form_id IS NOT NULL;

-- name: DonationTestResult :many
SELECT 
	t.id as id,
	t.donor_id as donor_id,
	t.form_id as form_id,
	t.time as time,
	t.validity_duration as validity_duration,
	t.invalidated as invalidated,
	f.donation_test_id as donation_test_id,
	a.name as admin_name
FROM test_result t
INNER JOIN form f ON t.form_id = f.id
INNER JOIN donation_test d ON f.donation_test_id = d.id
INNER JOIN "user" a ON d.tester_admin_id = a.admin_id 
WHERE t.donor_id = sqlc.arg(donor_id) AND f.donation_test_id IS NOT NULL;

-- name: InterviewDetails :one
SELECT 
	t.id as id,
	t.donor_id as donor_id,
	t.form_id as form_id,
	t.time as time,
	t.validity_duration as validity_duration,
	t.invalidated as invalidated,
	f.ok_to_donate as ok_to_donate,
	f.interview_id as interview_id,
	i.interviewer_admin_id as interviewer_admin_id,
	a.name as interviewer_admin_name
 FROM test_result t
	INNER JOIN form f ON t.form_id = f.id
	INNER JOIN interview i ON f.interview_id = i.id
	INNER JOIN "user" a ON i.interviewer_admin_id = a.admin_id 
	WHERE t.id = sqlc.arg(testresult_id) AND f.interview_id IS NOT NULL;

-- name: EntryFormDetails :one
SELECT 
	t.id as id,
	t.donor_id as donor_id,
	t.form_id as form_id,
	t.time as time,
	t.validity_duration as validity_duration,
	t.invalidated as invalidated,
	f.ok_to_donate as ok_to_donate,
	f.entry_form_id as entry_form_id
 FROM test_result t
	INNER JOIN form f ON t.form_id = f.id
	INNER JOIN entry_form e ON f.entry_form_id = e.id
	WHERE t.id = sqlc.arg(testresult_id) AND f.entry_form_id IS NOT NULL;

-- name: DonationTestDetails :one
SELECT 
	t.id as id,
	t.donor_id as donor_id,
	t.form_id as form_id,
	t.time as time,
	t.validity_duration as validity_duration,
	t.invalidated as invalidated,
	f.ok_to_donate as ok_to_donate,
	f.donation_test_id as donation_test_id,
	d.donation_id as donation_id,
	d.tester_admin_id as tester_admin_id,
	don.appointment_id as appointment_id,
	don.amount_ml as amount_ml,
	don.is_blood_not_plasma as is_blood_not_plasma,
	a.name as tester_admin_name
 FROM test_result t
	INNER JOIN form f ON t.form_id = f.id
	INNER JOIN donation_test d ON f.donation_test_id = d.id
	INNER JOIN donation don ON d.donation_id = don.id
	INNER JOIN "user" a ON d.tester_admin_id = a.admin_id 
	WHERE t.id = sqlc.arg(testresult_id) AND f.donation_test_id IS NOT NULL;
