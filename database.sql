DROP TABLE IF EXISTS urls;


CREATE TABLE urls (
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) UNIQUE,
    created_at TIMESTAMP
);