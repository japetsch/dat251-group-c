-- migrate:up
ALTER TABLE donation_test
ADD COLUMN tester_admin_id BIGINT NOT NULL,
ADD CONSTRAINT donation_test_fk_tester_admin_id
    FOREIGN KEY (tester_admin_id) REFERENCES admin(id);

-- migrate:down
ALTER TABLE donation_test
DROP CONSTRAINT donation_test_fk_tester_admin_id
DROP COLUMN tester_admin_id;
