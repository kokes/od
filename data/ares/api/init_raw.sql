drop table if exists ares.raw;
create table if not exists ares.raw (
	rejstrik varchar not null,
	ico int not null,
	modified_on timestamp default (now() at time zone 'UTC'),
	xml bytea,
	found boolean
);
alter table ares.raw add primary key (rejstrik, ico);
