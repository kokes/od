# TODO: bacha, u angazovanych osob jsou ministerstva bez uvedenych ICO (spousta radek to tak ma - filtruj ale jen ty, co maj jako stat cesko)
# 
# TODO: dodelat angazovane osoby! (dodelano?) mame 29 mapovani - mame 29 distinct typu? select nazev_ang, count(*) from ares.or_angos_fo group by 1;
# TODO: CIN, OSK (cinnosti, ostatni skutecnosti), KAP (kapital), REG/SZ (kym zapsano)

import json
import os
import csv

import lxml.etree
import psycopg2
import psycopg2.extras
from tqdm import tqdm

def get_el(root, address, namespace):
    el = root.find(address, namespaces=namespace)
    if el is None:
        return el
    return el.text

def get_el_all(root, address, namespace):
    el = root.findall(address, namespaces=namespace)
    if el is None:
        return el
    return [j.text for j in el]

def get_els(root, mapping, namespace):
    ret = {}
    for k, v in mapping.items():
        if isinstance(v, str):
            el = get_el(root, v, namespace)
            if el is not None:
                ret[k] = el
        else:
            ret[k] = json.dumps(get_els(root, v, namespace), ensure_ascii=False)

    return ret

hds = {
    'udaje': ['ico', 'aktualizace_db', 'datum_vypisu', 'platnost_od', 'datum_zapisu', 'stav_subjektu'],
    'nazvy': ['ico', 'dod', 'ddo', 'nazev'],
    'pravni_formy': ['ico', 'dod', 'ddo', 'kpf', 'npf', 'pfo', 'tzu'],
    'sidla': ['ico', 'dod', 'ddo', 'ulice', 'obec', 'stat', 'psc'],
    'angos_fo': ['ico', 'dod', 'ddo', 'nazev_ang', 'kategorie_ang', 'funkce', 'clenstvi_zacatek', 'clenstvi_konec', 'funkce_zacatek', 'funkce_konec', 'titul_pred', 'titul_za', 'jmeno', 'prijmeni', 'datum_narozeni', 'bydliste'],
    'angos_po': ['ico', 'dod', 'ddo', 'nazev_ang', 'kategorie_ang', 'funkce', 'clenstvi_zacatek', 'clenstvi_konec', 'funkce_zacatek', 'funkce_konec', 'ico_ang', 'izo_ang', 'nazev', 'pravni_forma', 'stat', 'sidlo'],
}

tdir = 'data/csv'
os.makedirs(tdir, exist_ok=True)

fhs = {} # file handlers
cws = {} # csv writers
for k,v in hds.items():
    tfn = os.path.join(tdir, f'{k}.csv')
    fhs[k] = open(tfn, 'w')
    cws[k] = csv.DictWriter(fhs[k], fieldnames=v)
    cws[k].writeheader()

conn = psycopg2.connect(host='localhost') # TODO: close
conn.cursor_factory = psycopg2.extras.DictCursor

with conn, conn.cursor('raw_read') as rcursor:
    rcursor.execute('''select ico, xml from ares.raw where rejstrik = \'or\' and "xml" is not null
        and found is true''')

    for row in tqdm(rcursor):
        et = lxml.etree.fromstring(row['xml'].tobytes())

        vyp = et.find('./are:Odpoved/D:Vypis_OR', namespaces=et.nsmap)
        if vyp is None:
            print(f'{row["ico"]} nacteno, ale neobsahuje vypis dat')
            continue

        udmap = {
            'aktualizace_db': './D:UVOD/D:ADB',
            'datum_vypisu': './D:UVOD/D:DVY',
            'platnost_od': './D:ZAU/D:POD',
            # 'ico': './D:ZAU/D:ICO', # nakonec pouzivame ICO z dotazu
            'datum_zapisu': './D:ZAU/D:DZOR',
            'stav_subjektu': './D:ZAU/D:S/D:SSU', # TODO: ZAU/S veci: konkurzy atd.    
        }

        udaje = get_els(vyp, udmap, et.nsmap)
        ico = int(row['ico']) # lepsi nez - int(udaje['ico']) - da se pak dohledat

        cws['udaje'].writerow({'ico': ico, **udaje})

        # nazev subjektu (v case)
        for el in vyp.findall('./D:ZAU/D:OF', namespaces=et.nsmap):
            of = {
                'ico': ico,
                'dod': el.attrib.get('dod'),
                'ddo': el.attrib.get('ddo'),
                'nazev': el.text,
            }
            cws['nazvy'].writerow(of)

        # pravni formy
        pmp = {
            'kpf': 'D:KPF',
            'npf': 'D:NPF',
            'pfo': 'D:PFO',
            'tzu': 'D:TZU',
        }

        for pfobj in vyp.findall('./D:ZAU/D:PFO', namespaces=et.nsmap):
            pfo = get_els(pfobj, pmp, et.nsmap)
            pfo['dod'] = pfobj.attrib.get('dod')
            pfo['ddo'] = pfobj.attrib.get('ddo')

            cws['pravni_formy'].writerow({'ico': ico, **pfo})
            
        # sidla
        # TODO: zbytek mappingu
        smp = {
            'stat': 'D:NS',
            'obec': 'D:N',
            'ulice': 'D:NU',
            'psc': 'D:PSC',
        }
        
        for siobj in vyp.findall('./D:ZAU/D:SI', namespaces=et.nsmap):
            si = get_els(siobj, smp, et.nsmap)
            si['dod'] = siobj.attrib.get('dod')
            si['ddo'] = siobj.attrib.get('ddo')
            
            cws['sidla'].writerow({'ico': ico, **si})

        # angazovane osoby
        # http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.3/ares_datatypes_v_1.0.3.xsd
        ang = {
            'statutarni_organ': 'D:SO/D:CSO/D:C',
            'sos': 'D:SOS/D:CSS/D:C',
            'sok': 'D:SOK/D:CSK/D:C',
            'sop': 'D:SOP/D:CSP/D:C',
            'predstavenstvo': 'D:PRE/D:CPR/D:C',
            'szo': 'D:SOZ/D:CZO/D:C',
            'spravni_rada': 'D:SR/D:CSR/D:C',
            'nadace': 'D:NAD/D:OON',
            'nadacni_fond': 'D:NF/D:OOF',
            'likvidace': 'D:LI/D:LIR',
            'prokura': 'D:PRO/D:PRA',
            'reditele_ops': 'D:Reditele_ops/D:Reditel_ops',
            'dozorci_rada': 'D:DR/D:CDR/D:C',
            'kontrolni_komise': 'D:Kontrolni_komise/D:Clen_kontrolni_komise/D:C',
            'revizori': 'D:REI/D:RE',
            'spolecnici_bez_vkladu': 'D:SBV/D:SB',
            'spolecnici_s_vkladem': 'D:SSV/D:SS',
            'akcionari': 'D:AKI/D:AKR',
            'zakladatele_SP': 'D:Z_SP/D:ZSP',
            'zakladatele_OPS': 'D:Z_OPS/D:ZOPS',
            'zrizovatele_OZ': 'D:Z_OZ/D:ZOZ',
            'zrizovatele_PR': 'D:Z_PR/D:ZPR',
            'nastupci_zrizovatele': 'D:NAU/D:NAE',
            'zrizovatele_nadace': 'D:Z_N/D:ZN',
            'ved_oz': 'D:VOU/D:VOZ',
            'komanditiste': 'D:KME/D:KMA',
            'druzstevnici': 'D:DCI/D:DIK',
            'komplementari': 'D:KPI/D:CSK/D:C',
            'clenove_sdruzeni': 'D:CLS/D:CS',
        }
        # high level info
        hli = {
            'kategorie_ang': 'D:KAN', # kod angazovanosti
            'funkce': 'D:F',
            'clenstvi_zacatek': 'D:CLE/D:DZA',
            'clenstvi_konec': 'D:CLE/D:DK',
            'funkce_zacatek': 'D:VF/D:DZA',
            'funkce_konec': 'D:VF/D:DK',
        }
        # FO
        fomap = {
            'titul_pred': 'D:TP',
            'titul_za': 'D:TZ',
            'jmeno': 'D:J',
            'prijmeni': 'D:P',
            'datum_narozeni': 'D:DN',
            'bydliste': {
                'ida': 'D:B/D:IDA',
                'kod_statu': 'D:B/D:KS',
                'nazev_statu': 'D:B/D:NS',
                'nazev_oblasti': 'D:B/D:Nazev_oblasti',
                'nazev_kraje': 'D:B/D:Nazev_kraje',
                'nazev_okresu': 'D:B/D:NOK',
                'nazev_obce': 'D:B/D:N',
                'nazev_obvodu': 'D:B/D:Nazev_pobvodu',
                'nazev_casti_obce': 'D:B/D:NCO',
                'nazev_mestske_casti': 'D:B/D:NMC',
                'nazev_ulice': 'D:B/D:NU',
                'cis_dom': 'D:B/D:CD',
                'typ_cis_dom': 'D:B/D:TCD',
                'cis_or_sp': 'D:B/D:CO',
                'cislo_do_adresy': 'D:B/D:CA',
                'psc': 'D:B/D:PSC',
                'string': 'D:B/D:Zahr_PSC',
                'adresa_textem': 'D:B/D:AT',
                'adresa_UIR': 'D:B/D:AU',
            },
        }
        # PO
        pomap = {
            'ico_ang': 'D:ICO',
            'izo_ang': 'D:IZO',
            'nazev': 'D:OF',
            'pravni_forma': 'D:NPF',
            'stat': 'D:SI/D:NS', # TODO: redundantni
            'sidlo': {
                'ida': 'D:SI/D:IDA',
                'kod_statu': 'D:SI/D:KS',
                'nazev_statu': 'D:SI/D:NS',
                'nazev_oblasti': 'D:SI/D:Nazev_oblasti',
                'nazev_kraje': 'D:SI/D:Nazev_kraje',
                'nazev_okresu': 'D:SI/D:NOK',
                'nazev_obce': 'D:SI/D:N',
                'nazev_obce': 'D:SI/D:Nazev_pobvodu',
                'nazev_casti_obce': 'D:SI/D:NCO',
                'nazev_mestske_casti': 'D:SI/D:NMC',
                'nazev_ulice': 'D:SI/D:NU',
                'cis_dom': 'D:SI/D:CD',
                'typ_cis_dom': 'D:SI/D:TCD',
                'cis_or_sp': 'D:SI/D:CO',
                'cislo_do_adresy': 'D:SI/D:CA',
                'psc': 'D:SI/D:PSC',
                'string': 'D:SI/D:Zahr_PSC',
                'adresa_textem': 'D:SI/D:AT',
                'adresa_UIR': 'D:SI/D:AU',
            },
        }

        for nm, ad in ang.items():
            for el in vyp.findall(ad, namespaces=et.nsmap):
                info = get_els(el, hli, et.nsmap)

                if ad.endswith('/D:C'):
                    # dozorci rada a stat. organy maj cleny
                    # takze platnost je o koren vyse
                    pr = el.getparent()
                    info['dod'] = pr.attrib['dod']
                    info['ddo'] = pr.attrib.get('ddo')
                else:
                    info['dod'] = el.attrib['dod']
                    info['ddo'] = el.attrib.get('ddo')

                fo = el.find('D:FO', namespaces=et.nsmap)
                po = el.find('D:PO', namespaces=et.nsmap)
                if fo is not None:
                    fo_info = get_els(fo, fomap, et.nsmap)
                    cws['angos_fo'].writerow({
                          'ico': ico,
                          'nazev_ang': nm,
                          **info,
                          **fo_info
                      })

                if po is not None:
                    po_info = get_els(po, pomap, et.nsmap)
                    cws['angos_po'].writerow({
                          'ico': ico,
                          'nazev_ang': nm,
                          **info,
                          **po_info
                      })

for fh in fhs.values():
    fh.close()
