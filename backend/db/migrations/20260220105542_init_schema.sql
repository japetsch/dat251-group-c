-- migrate:up
CREATE TABLE first_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    a TEXT
);

-- migrate:down
DROP TABLE first_table;

