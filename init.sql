create schema users;


create table users.reminders (
    user_id integer not null,
    reminder_txt varchar not null,
    reminder_date timestamp without time zone not null default (current_timestamp at time zone 'utc'),
    created_at timestamp without time zone not null default (current_timestamp at time zone 'utc')
);