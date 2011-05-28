drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    text text not null,
    author text not null,
    mail text not null,
    time integer not null,
    comments_num integer not null,
    token text not null
);
drop table if exists comments;
create table comments (
    id integer primary key autoincrement,
    text text not null,
    post_id integer not null,
    author text not null,
    mail text not null,
    time integer not null,
    token text not null
);

drop table if exists receivers;
create table receivers (
    id integer primary key autoincrement,
    mail text not null,
    phone text not null,
    time integer not null,
    token text not null
);
