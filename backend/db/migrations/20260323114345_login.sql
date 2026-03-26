-- migrate:up
ALTER TABLE "user" ADD COLUMN password_hash TEXT NULL;
ALTER TABLE "user" ADD CONSTRAINT user_email_unique UNIQUE (email);

-- migrate:down
ALTER TABLE "user" DROP COLUMN password_hash;
ALTER TABLE "user" DROP CONSTRAINT user_email_unique;
