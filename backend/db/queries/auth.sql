-- name: GetUser :one
SELECT u.id, u.name, u.email, u.password_hash, u.donor_id, u.admin_id
FROM "user" u WHERE u.email = $1;
