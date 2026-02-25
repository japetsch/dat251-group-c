-- migrate:up
CREATE TABLE "user" (
	id BIGSERIAL PRIMARY KEY,
	name TEXT NOT NULL
);

CREATE TABLE bloodbank (
	id BIGSERIAL PRIMARY KEY,
	name TEXT NOT NULL
);

CREATE TABLE appointment (
	id BIGSERIAL PRIMARY KEY,
	user_id BIGINT NOT NULL,
	time TIMESTAMP WITH TIME ZONE NOT NULL,
	location_id BIGINT NOT NULL,

	FOREIGN KEY (user_id) REFERENCES "user"(id),
	FOREIGN KEY (location_id) REFERENCES bloodbank(id)
);

-- migrate:down
DROP TABLE appointment;
DROP TABLE "user";
DROP TABLE bloodbank;
