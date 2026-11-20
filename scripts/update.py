#!/usr/bin/env python3
"""Download Spain's official fuel prices and keep only Shell stations (not Shell Express) with diesel.

Source: Ministerio para la Transicion Ecologica, Geoportal de Gasolineras REST service (open data, updated about
every 30 minutes). Writes data/shell.json, read by index.html. Standard library only, so the GitHub Action needs
no installs.
"""
import json
import os
import sys
import time
import urllib.request

URL = ('https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/'
       'PreciosCarburantes/EstacionesTerrestres/')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'shell.json')
# Shell Express stations the ministry lists under the plain "SHELL" sign: DISA's own list, matched to station ids
EXPRESS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'express_ids.json')


def num(v):
    """'1,459' -> 1.459; '' -> None."""
    v = (v or '').strip().replace(',', '.')
    try:
        return float(v) if v else None
    except ValueError:
        return None


def is_shell(rotulo):
    r = (rotulo or '').upper()
    return 'SHELL' in r and 'EXPRESS' not in r


def fetch():
    req = urllib.request.Request(URL, headers={
        'Accept': 'application/json',
        'User-Agent': 'shell-diesel (github.com/46Wen/shell-diesel; personal fuel price page)',
    })
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode('utf-8-sig'))
        except Exception as e:  # the service is sometimes briefly unavailable (503)
            last = e
            time.sleep(15 * (attempt + 1))
    raise SystemExit('could not download the prices: %s' % last)


def main():
    try:
        with open(EXPRESS, encoding='utf-8') as f:
            express = set(json.load(f)['ids'])
    except (OSError, ValueError, KeyError):
        express = set()
    raw = fetch()
    rows = raw.get('ListaEESSPrecio') or []
    out = []
    for s in rows:
        if not is_shell(s.get('Rótulo')) or s.get('IDEESS') in express:
            continue
        lat, lon = num(s.get('Latitud')), num(s.get('Longitud (WGS84)'))
        ga, gp = num(s.get('Precio Gasoleo A')), num(s.get('Precio Gasoleo Premium'))
        if lat is None or lon is None or (ga is None and gp is None):
            continue
        out.append({
            'id': s.get('IDEESS'),
            'n': (s.get('Rótulo') or '').strip(),
            'a': (s.get('Dirección') or '').strip(),
            'cp': (s.get('C.P.') or '').strip(),
            'loc': (s.get('Localidad') or '').strip(),
            'mun': (s.get('Municipio') or '').strip(),
            'prov': (s.get('Provincia') or '').strip(),
            'h': (s.get('Horario') or '').strip(),
            'lat': round(lat, 6), 'lon': round(lon, 6),
            'ga': ga, 'gp': gp,
        })
    if len(out) < 50:
        # a broken download must never replace good data with an almost empty file
        raise SystemExit('only %d Shell stations found in %d rows; not writing' % (len(out), len(rows)))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump({'fecha': raw.get('Fecha'), 'updated': int(time.time()), 'stations': out}, f,
                  ensure_ascii=False, separators=(',', ':'))
    print('%d Shell stations (no Express) of %d, prices of %s' % (len(out), len(rows), raw.get('Fecha')))


if __name__ == '__main__':
    sys.exit(main())
