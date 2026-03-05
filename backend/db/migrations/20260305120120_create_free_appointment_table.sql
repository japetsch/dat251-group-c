-- migrate:up
CREATE TABLE free_appointments (
    id BIGSERIAL PRIMARY KEY,
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    location_id BIGINT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES bloodbank(id),
    UNIQUE (location_id, time)
)

-- migrate:down
DROP TABLE free_appointments;