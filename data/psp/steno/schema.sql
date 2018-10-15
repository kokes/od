DROP TABLE IF EXISTS psp.steno_psp;
CREATE TABLE IF NOT EXISTS psp.steno_psp (
	rok smallint,
	datum varchar,
	schuze smallint not null,
	fn varchar not null,
	autor varchar,
	funkce varchar,
	tema varchar,
	"text" text not null
);
