DROP TABLE IF EXISTS od.psp_steno_psp;
CREATE TABLE IF NOT EXISTS od.psp_steno_psp (
	rok smallint,
	datum varchar,
	schuze smallint not null,
	fn varchar not null,
	autor varchar,
	funkce varchar,
	tema varchar,
	"text" text not null
);
