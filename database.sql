DROP TABLE IF EXISTS urls CASCADE;
DROP TABLE IF EXISTS url_checks CASCADE;

CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255),
    created_at timestamp
);

CREATE TABLE url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id bigint,
    status_code integer,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at timestamp
);
