-- name: GetAllBloodBanks :many
SELECT b.id as bloodbank_id, b.name, a.street_name, a.street_number, a.postal_code, a.city, a.country,
    COUNT(bba.admin_id) > 0 AS user_has_admin_access
FROM bloodbank b
INNER JOIN location l ON b.location_id = l.id
INNER JOIN address a ON l.address_id = a.id
LEFT JOIN bloodbank_admin bba ON (b.id = bba.bloodbank_id AND bba.admin_id = $1)
GROUP BY b.id, a.id;
