# Independent checks on the rebuilt CSV files (does not reuse the build script).
# Usage: python3 code/verify_counts.py OUTPUT_FOLDER
import csv, os, sys, collections
D = os.path.join(sys.argv[1], 'csv'); rd = lambda n: list(csv.DictReader(open(os.path.join(D, n + '.csv'), encoding='utf-8')))
ok = []
s4 = rd('S4_EPA_list_197'); assert len(s4) == 197
g = lambda r, k: r[k] == '1'
both = [r for r in s4 if g(r, 'Closure cost (T3)') and g(r, 'Instrument (T4)')]
conly = [r for r in s4 if g(r, 'Closure cost (T3)') and not g(r, 'Instrument (T4)')]
ionly = [r for r in s4 if g(r, 'Instrument (T4)') and not g(r, 'Closure cost (T3)')]
neither = [r for r in s4 if not g(r, 'Closure cost (T3)') and not g(r, 'Instrument (T4)')]
assert (len(both), len(conly), len(ionly), len(neither)) == (162, 13, 1, 21); ok.append('EPA list: 197 = 162 + 13 + 1 + 21')
s1 = rd('S1_Tracking_27'); assert len(s1) == 27
cnt = lambda k, v: sum(r[k] == v for r in s1)
assert (cnt('Operation ended', 'yes'), cnt('Equipment removal', 'yes'), cnt('Demolition', 'stated complete'), sum(r['Demolition'].startswith('qualified') for r in s1), cnt('Amount recorded', 'yes')) == (21, 7, 4, 2, 5)
ok.append('Tracking records: 27; ended 21; equipment 7; demolition 4 stated complete + 2 qualified; amount 5')
fa = collections.Counter(r['Final account of the works: verdict'] for r in s1); cb = collections.Counter(r['Final net cost bearer: verdict'] for r in s1)
assert fa == cb == {'not identified in the documents reviewed': 7, 'not judged (event-level sources only)': 20}
assert all(r['Final account: basis'] != r['Final net cost bearer: basis'] for r in s1)
ok.append('S1: two verdict columns, each 7 not identified + 20 not judged, 0 identified; bases differ in all 27 rows')
s2 = rd('S2_US_cells_56'); assert len(s2) == 56 and sum(r['Status'] == 'documented' for r in s2) == 27 and sum(r['Status'].startswith('not established') for r in s2) == 29
ok.append('S2: 56 cells = 27 documented + 29 negative observations')
s3 = rd('S3_Licences_18'); assert len(s3) == 18 and len({r['SHA-256 of the report'] for r in s3}) == 18
assert collections.Counter(r['Closure-cost statement: counted as'] for r in s3) == {'initial application': 5, 'licence review': 1, 'earlier reading not matched': 1, 'no costing document obtained': 11}
assert [r['Licence'] for r in s3 if r['EPA list at 31 Dec 2025'] != 'Not listed'] == ['P1191-01']
shared = {r['Licence'].split('-')[0] for r in s3} & {r['Registration'] for r in s4}; assert shared == {'P1191'}
ok.append('S3: 18 licences, 18 distinct report hashes; closure-cost statements 5 / 1 / 1 / 11; only P1191 on the list; the 18 and the 197 share one registration (P1191)')
s6 = rd('S6_Company_statements'); assert len(s6) == 8
assert sum(not r['Provisions for liabilities'].startswith('no ') for r in s6) == 3 and all(r[list(r)[-1]] == 'no' for r in s6)
ok.append('S6: 8 companies; 3 disclosed provisions; 0 attributed an amount to an identified licensed data centre')
s7 = rd('S7_AER_2025_18'); f7 = [r for r in s7 if r['2025 report found'] == 'yes']; assert len(s7) == 18 and len(f7) == 16
t = [int(r['Incidents (table)']) for r in f7]; a = [int(r['Incidents (alternative count)'] or r['Incidents (table)']) for r in f7]
assert (sum(t), sum(x > 0 for x in t), sum(a), sum(x > 0 for x in a)) == (56, 12, 53, 11)
assert [r['Licence'] for r in s3] == [r['Licence'] for r in s7]
ok.append('S7: 16 reports; 56 notifications across 12 licences; alternative 53 across 11')
for x in ok: print('VERIFY OK:', x)
