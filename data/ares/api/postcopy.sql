ALTER TABLE ares.or_angos_fo ADD COLUMN jmeno_prijmeni varchar;
UPDATE ares.or_angos_fo SET jmeno_prijmeni = TRIM(CONCAT(jmeno, ' ', prijmeni));
CREATE INDEX ares_or_angos_fo_jmeno_prijmeni_idx ON ares.or_angos_fo(LOWER(jmeno_prijmeni));
