-- migrate:up

DROP TABLE IF EXISTS free_appointments;
DROP TABLE IF EXISTS appointment;
DROP TABLE IF EXISTS bloodbank;
DROP TABLE IF EXISTS "user";

-- TODO: add constraints that intervals are positive

CREATE TABLE address (
    id BIGSERIAL PRIMARY KEY,
    street_name TEXT NOT NULL,
    street_number TEXT NOT NULL,
    apt_number TEXT,
    postal_code TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE location (
    id BIGSERIAL PRIMARY KEY,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,

    address_id BIGINT NOT NULL,

    FOREIGN KEY (address_id) REFERENCES address(id)
);

CREATE TABLE bloodbank (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,

    location_id BIGINT NOT NULL,

    FOREIGN KEY (location_id) REFERENCES location(id)
);

-- Needs to be deleted and recreated on change
CREATE TABLE opening_hours (
    id BIGSERIAL PRIMARY KEY,
    bloodbank_id BIGINT NOT NULL,
    opening_cron TEXT NOT NULL,
    open_duration INTERVAL NOT NULL,

    FOREIGN KEY (bloodbank_id) REFERENCES bloodbank(id)
);

CREATE TABLE recurring_holiday (
    id BIGSERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    starting_cron TEXT NOT NULL,
    duration INTERVAL NOT NULL
);

CREATE TABLE bloodbank_recurring_holiday (
    id BIGSERIAL PRIMARY KEY,
    bloodbank_id BIGINT NOT NULL,
    recurring_holiday_id BIGINT NOT NULL,

    FOREIGN KEY (bloodbank_id) REFERENCES bloodbank(id),
    FOREIGN KEY (recurring_holiday_id) REFERENCES recurring_holiday(id)
);

CREATE TABLE bloodbank_holiday (
    id BIGSERIAL PRIMARY KEY,
    bloodbank_id BIGINT NOT NULL,
    holiday_id BIGINT NOT NULL,

    FOREIGN KEY (bloodbank_id) REFERENCES bloodbank(id),
    FOREIGN KEY (holiday_id) REFERENCES recurring_holiday(id)
);

CREATE TABLE holiday (
    id BIGSERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    starting TIMESTAMP WITH TIME ZONE NOT NULL,
    ending TIMESTAMP WITH TIME ZONE NOT NULL
);

-- TODO: validate that it is within opening hours, not within holidays
CREATE TABLE bookingslot (
    id BIGSERIAL PRIMARY KEY,
    bloodbank_id BIGINT NOT NULL,

    time TIMESTAMP WITH TIME ZONE NOT NULL,
    duration INTERVAL NOT NULL,
    capacity BIGINT NOT NULL,

    FOREIGN KEY (bloodbank_id) REFERENCES bloodbank(id)
);

CREATE TABLE admin ( -- TODO: add their blood banks
    id BIGSERIAL PRIMARY KEY
);

CREATE TABLE bloodbank_admin (
    id BIGSERIAL PRIMARY KEY,
    bloodbank_id BIGINT NOT NULL,
    admin_id BIGINT NOT NULL,

    FOREIGN KEY (bloodbank_id) REFERENCES bloodbank(id),
    FOREIGN KEY (admin_id) REFERENCES admin(id)
    -- TODO: make sure you don't delete the last admin from a blood bank
);

CREATE TYPE blood_type AS ENUM ('O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-');
CREATE TABLE donor (
    id BIGSERIAL PRIMARY KEY,
    comment TEXT,
    blood_type blood_type,

    preferred_bloodbank_id BIGINT NOT NULL,
    min_interval INTERVAL,
    slot_preference TEXT,  -- cron spec

    FOREIGN KEY (preferred_bloodbank_id) REFERENCES bloodbank(id)
);

CREATE TABLE "user" (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    home_address_id BIGINT NOT NULL,

    donor_id BIGINT,
    admin_id BIGINT,

    FOREIGN KEY (home_address_id) REFERENCES address(id),
    FOREIGN KEY (donor_id) REFERENCES donor(id),
    FOREIGN KEY (admin_id) REFERENCES admin(id),
    CHECK (
        (donor_id IS NOT NULL AND admin_id IS NULL) OR
        (donor_id IS NULL     AND admin_id IS NOT NULL)
    )
);

CREATE TABLE user_alternative_address (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    address_id BIGINT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (address_id) REFERENCES address(id)
);

CREATE TABLE appointment (
    id BIGSERIAL PRIMARY KEY,
    bookingslot_id BIGINT NOT NULL,
    cancelled BOOLEAN,
    donor_id BIGINT NOT NULL,

    FOREIGN KEY (donor_id) REFERENCES donor(id),
    FOREIGN KEY (bookingslot_id) REFERENCES bookingslot(id)
);

CREATE TABLE appointment_note (
    id BIGSERIAL PRIMARY KEY,
    appointment_id BIGINT NOT NULL,

    time TIMESTAMP WITH TIME ZONE NOT NULL,
    message TEXT NOT NULL,

    FOREIGN KEY (appointment_id) REFERENCES appointment(id)
);

CREATE TABLE donation (
    id BIGSERIAL PRIMARY KEY,
    appointment_id BIGINT NOT NULL,

    amount_ml DOUBLE PRECISION NOT NULL,
    is_blood_not_plasma BOOLEAN NOT NULL,

    FOREIGN KEY (appointment_id) REFERENCES appointment(id)
);

-- TODO: add more information to each of these form types
CREATE TABLE interview (
    id BIGSERIAL PRIMARY KEY,
    interviewer_admin_id BIGINT NOT NULL,

    FOREIGN KEY (interviewer_admin_id) REFERENCES admin(id)
);

CREATE TABLE entry_form (
    id BIGSERIAL PRIMARY KEY
);

CREATE TABLE donation_test (
    id BIGSERIAL PRIMARY KEY,
    donation_id BIGINT NOT NULL,

    FOREIGN KEY (donation_id) REFERENCES donation(id)
);

-- generalized "form" for a test result (entry form, interview, blood sample testing)
CREATE TABLE form (
    id BIGSERIAL PRIMARY KEY,
    ok_to_donate BOOLEAN DEFAULT TRUE,

    interview_id BIGINT,
    entry_form_id BIGINT,
    donation_test_id BIGINT,

    FOREIGN KEY (interview_id) REFERENCES interview(id),
    FOREIGN KEY (entry_form_id) REFERENCES entry_form(id),
    FOREIGN KEY (donation_test_id) REFERENCES donation_test(id),
    CHECK (
        (interview_id IS NOT NULL AND entry_form_id IS     NULL AND donation_test_id IS     NULL) OR
        (interview_id IS     NULL AND entry_form_id IS NOT NULL AND donation_test_id IS     NULL) OR
        (interview_id IS     NULL AND entry_form_id IS     NULL AND donation_test_id IS NOT NULL)
    )
);

CREATE TABLE test_result (
    id BIGSERIAL PRIMARY KEY,
    donor_id BIGINT NOT NULL,
    form_id BIGINT NOT NULL,

    time TIMESTAMP WITH TIME ZONE NOT NULL,
    validity_duration INTERVAL NOT NULL,
    invalidated BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (donor_id) REFERENCES donor(id),
    FOREIGN KEY (form_id) REFERENCES form(id)
);

-- migrate:down
DROP TABLE test_result;
DROP TABLE form;
DROP TABLE donation_test;
DROP TABLE entry_form;
DROP TABLE interview;
DROP TABLE donation;
DROP TABLE appointment_note;
DROP TABLE appointment;
DROP TABLE user_alternative_address;
DROP TABLE "user";
DROP TABLE donor;
DROP TYPE blood_type;
DROP TABLE bloodbank_admin;
DROP TABLE admin;
DROP TABLE bookingslot;
DROP TABLE bloodbank_holiday;
DROP TABLE holiday;
DROP TABLE bloodbank_recurring_holiday;
DROP TABLE recurring_holiday;
DROP TABLE opening_hours;
DROP TABLE bloodbank;
DROP TABLE location;
DROP TABLE address;
