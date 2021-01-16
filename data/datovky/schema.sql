drop table if exists datovky;

create table datovky (
	id varchar unique not null,
	type varchar not null,
	subtype smallint not null,
	firstName varchar,
	lastName varchar,
	middleName varchar,
	tradeName varchar,
	ico int,
	address jsonb,
	pdz bool not null,
	ovm bool not null,
	hierarchy jsonb not null,
	idOVM int
);

create index datovky_ico on datovky(ico);
