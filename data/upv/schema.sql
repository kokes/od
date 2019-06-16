create schema if not exists upv;

drop table if exists upv.deletes;
create table upv.deletes (
	application_number int not null,
	application_date date not null
);

drop table if exists upv.inserts;
create table upv.inserts (
	application_number int not null,
	application_date date not null,
	registration_number int,
	registration_date date,
	expiry_date date,
	current_status_code varchar not null,
	kind_mark varchar not null,
	mark_feature varchar,
	mark_verbal_element varchar,
	class_description jsonb	 
);

CREATE INDEX trgm_verbal_idx ON upv.inserts USING gist (mark_verbal_element gist_trgm_ops);
