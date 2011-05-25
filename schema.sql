drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    text text not null,
    author text not null,
    mail text not null,
    time integer not null
);
