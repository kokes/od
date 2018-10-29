create index zakazky_etrziste_dodavatele_dodavatelico_idx on zakazky.etrziste_dodavatele(dodavatelico);
create index zakazky_etrziste_vz_zadavatelico_idx on zakazky.etrziste_vz(zadavatelico);
create index zakazky_etrziste_vz_dodavatelico_idx on zakazky.etrziste_vz(dodavatelico);
create index zakazky_vvz_casti_vz_dodavatelicozezadani_idx on zakazky.vvz_casti_vz(dodavatelicozezadani);
create index zakazky_vvz_vz_zadavatelico_idx on zakazky.vvz_vz(zadavatelico);
create index zakazky_vvz_vz_dodavatelico_idx on zakazky.vvz_vz(dodavatelico);
create index zakazky_zzvz_dodavatele_dodavatelico_idx on zakazky.zzvz_dodavatele(dodavatelico);
create index zakazky_zzvz_vz_zadavatelico_idx on zakazky.zzvz_vz(zadavatelico);
