-- kvuli duplikatu v ICO 64123561

delete from ares.vreo_firmy t1 using
ares.vreo_firmy t2 where t1.aktualizace_db < t2.aktualizace_db and t1.ico=t2.ico;

alter table ares.vreo_firmy add primary key (ico);
