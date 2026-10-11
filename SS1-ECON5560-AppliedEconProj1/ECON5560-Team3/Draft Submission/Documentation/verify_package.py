#!/usr/bin/env python3
"""Verify submission integrity and key saved-result invariants without rerunning estimation.

Run: python3 Documentation/verify_package.py
After intentional edits: python3 Documentation/verify_package.py --refresh-manifest
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'MANIFEST_SHA256.csv'


def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and p != MANIFEST
                  and not any(x in p.parts for x in ('__pycache__', '.venv', '.ipynb_checkpoints'))
                  and p.name != '.DS_Store')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(newline='') as stream:
        return list(csv.DictReader(stream))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh-manifest', action='store_true')
    args = parser.parse_args()
    if args.refresh_manifest:
        with MANIFEST.open('w', newline='') as stream:
            w = csv.writer(stream)
            w.writerow(['path', 'bytes', 'sha256'])
            for path in files():
                w.writerow([path.relative_to(ROOT).as_posix(), path.stat().st_size, digest(path)])
        print('Refreshed manifest.')
    entries = rows(MANIFEST)
    actual = {p.relative_to(ROOT).as_posix() for p in files()}
    assert actual == {r['path'] for r in entries}, 'Manifest file list differs'
    for row in entries:
        p = ROOT / row['path']
        assert p.stat().st_size == int(row['bytes']), 'Size mismatch: ' + row['path']
        assert digest(p) == row['sha256'], 'SHA256 mismatch: ' + row['path']
    out = ROOT / 'Replication/Data-Parsing/output'
    data = rows(out / 'data/choice_long.csv')
    assert len(data) == 2160
    complete = [r for r in data if r['complete'] == '1']
    assert len(complete) == 1968
    assert len({r['id'] for r in complete}) == 164
    assert len({r['id'] for r in complete if r['councillor'] == '1'}) == 123
    occasions = {}
    for r in complete:
        occasions.setdefault(r['occasion'], []).append(r)
    assert len(occasions) == 656
    assert all(len(v) == 3 and sum(int(r['chosen']) for r in v) == 1 for v in occasions.values())
    for r in data:
        priced_dev = int(r['treatment'] in ('2', '3'))
        priced_water = int(r['treatment'] == '3')
        for term, base in [('lim_money', 'dev_limited'), ('res_money', 'dev_high'), ('com_money', 'dev_com')]:
            assert int(r[term]) == int(r[base]) * priced_dev
        for term, base in [('med_money', 'wat_med'), ('low_money', 'wat_low')]:
            assert int(r[term]) == int(r[base]) * priced_water
    bars = rows(out / 'paper_figures/03_fig1_responses_per_choice_scenario_comparison.csv')
    assert len(bars) == 36 and all(int(r['ours']) == int(r['paper']) for r in bars)
    ml = json.loads((out / 'results/ml.json').read_text())
    for key in ('m3', 'm4'):
        assert ml[key]['primary']['converged'] is True
        assert ml[key]['primary']['draws'] == 2000
        assert len(ml[key]['sensitivity']) == 20
    cl = rows(out / 'tables/table3_cl.csv')
    rr = rows(out / 'tables/r_crosscheck_clogit.csv')
    labels = {'dev_limited': 'Development: Limited', 'dev_high': 'Development: Residential',
              'dev_com': 'Development: Commercial', 'wat_med': 'Water quality: Medium',
              'wat_low': 'Water quality: Low', 'cult_s': 'Cultural: Stables',
              'cult_sl': 'Cultural: Stables & landscape', 'lim_money': 'Limited × $ shown',
              'res_money': 'Residential × $ shown', 'com_money': 'Commercial × $ shown',
              'med_money': 'Medium water × $ shown', 'low_money': 'Low water × $ shown'}
    checked = 0
    for r in rr:
        councillor = 'Councillors' in r['model']
        py = next(p for p in cl if p['variable'] == labels[r['variable']]
                  and ('Councillors' in p['model']) == councillor)
        coef_col, p_col = ('rep_coef', 'rep_p') if r['grouping'] == 'card' else ('corr_coef', 'corr_p_model')
        assert abs(float(py[coef_col]) - float(r['coef'])) <= 0.0011
        assert abs(float(py[p_col]) - float(r['p'])) <= 0.0011
        checked += 1
    assert checked == 48
    with zipfile.ZipFile(ROOT / 'Memo/Team3_Draft_Replication_Memo.docx') as z:
        assert len([n for n in z.namelist() if n.startswith('word/media/')]) == 8
        xml = z.read('word/document.xml').decode()
        assert 'Recommendations' in xml and 'posterior mean coefficients' in xml
    assert (ROOT / 'Memo/Team3_Draft_Replication_Memo.pdf').read_bytes().startswith(b'%PDF')
    print('PASS:', len(entries), 'file hashes; 164 respondents / 656 choices; treatment coding; 36 bars;')
    print('2 converged primary ML fits / 20 sensitivity runs each; 48 R/Python CL comparisons; 8 DOCX images.')
    print('This checks saved outputs and integrity, not the validity of all statistical assumptions.')


if __name__ == '__main__':
    main()
