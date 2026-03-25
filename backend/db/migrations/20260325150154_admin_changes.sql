-- migrate:up
ALTER TABLE bloodbank ADD CONSTRAINT bloodbank_unique_name UNIQUE (name);
ALTER TABLE bloodbank_admin ADD CONSTRAINT bloodbank_admin_unique_pair
    UNIQUE (bloodbank_id, admin_id);
ALTER TABLE "user" ADD CONSTRAINT donor_id_unique UNIQUE (donor_id);
ALTER TABLE "user" ADD CONSTRAINT admin_id_unique UNIQUE (admin_id);
ALTER TABLE form ALTER COLUMN ok_to_donate SET NOT NULL;

ALTER TABLE appointment
ALTER COLUMN cancelled SET NOT NULL,
ALTER COLUMN cancelled SET DEFAULT false;

ALTER TABLE appointment_note
ADD COLUMN author_id BIGINT NOT NULL,
ADD CONSTRAINT appointment_note_fk_author_id FOREIGN KEY (author_id) REFERENCES "user"(id);

-- migrate:down
ALTER TABLE bloodbank DROP CONSTRAINT bloodbank_unique_name;
ALTER TABLE bloodbank_admin DROP CONSTRAINT bloodbank_admin_unique_pair;
ALTER TABLE "user" DROP CONSTRAINT donor_id_unique;
ALTER TABLE "user" DROP CONSTRAINT admin_id_unique;
ALTER TABLE form ALTER COLUMN ok_to_donate DROP NOT NULL;

ALTER TABLE appointment
ALTER COLUMN cancelled DROP NOT NULL,
ALTER COLUMN cancelled DROP DEFAULT;

ALTER TABLE appointment_note
DROP CONSTRAINT appointment_note_fk_author_id,
DROP COLUMN author_id;
