drop table if exists od.ares_raw;
create table if not exists od.ares_raw (
	rejstrik varchar not null,
	ico int not null,
	modified_on timestamp default (now() at time zone 'UTC'),
	xml bytea,
	found boolean
);
alter table od.ares_raw add primary key (rejstrik, ico);
