drop schema if exists tgbot cascade;
create schema if not exists tgbot;

drop table if exists products CASCADE;
create table products
(
    id                  bigserial primary key,
    product_name        varchar(50)  not null,
    product_description varchar(100) not null,
    product_price       decimal(5)   not null,
    product_quantity    integer      not null,
    product_type        varchar(10)  not null,
    product_sex         varchar(6)   not null
);
drop table if exists product_photos CASCADE;
create table product_photos
(
    photo_id      bigserial primary key,
    photo_name    varchar    not null,
    photo_ext     varchar(4) not null,
    photo_content oid        not null,
    is_main       boolean default false,
    product_id    integer    not null references products (id)
        on delete cascade
        on update cascade
);

drop table if exists payment CASCADE;
create table payment
(
    payment_id        bigserial primary key,
    payment_status    bool default false,
    payment_amount    decimal not null,
    payment_check_sum varchar not null

);
