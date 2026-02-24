-- migrate:up
CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL
);

CREATE TABLE bloodbank (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL
);

CREATE TABLE appointment (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	time TEXT NOT NULL,
	location_id INTEGER NOT NULL,
	FOREIGN KEY (user_id) REFERENCES user(id),
	FOREIGN KEY (location_id) REFERENCES bloodbank(id)
);

-- migrate:down
DROP TABLE appointment;
DROP TABLE user;
DROP TABLE bloodbank;
