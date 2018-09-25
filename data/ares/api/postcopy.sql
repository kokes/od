ALTER TABLE od.ares_or_angos_fo ADD COLUMN jmeno_prijmeni varchar;
UPDATE od.ares_or_angos_fo SET jmeno_prijmeni = TRIM(CONCAT(jmeno, ' ', prijmeni));
CREATE INDEX ares_or_angos_fo_jmeno_prijmeni_idx ON od.ares_or_angos_fo(LOWER(jmeno_prijmeni));
