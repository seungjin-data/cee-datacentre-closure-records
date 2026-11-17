# One command: python3 reproduce.py            (content checks decide the result; file hashes are reported separately)
#              python3 reproduce.py --strict   (reference environment only: also fails on any byte difference)
import hashlib, os, shutil, subprocess, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'rebuild'); REF = os.path.join(HERE, 'outputs')
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
run = lambda *a: subprocess.run([sys.executable, '-I', *a], cwd=HERE, check=True)
run('code/build_supplement.py', '--out', OUT)                                   # asserts every table count against the manuscript tables
run('code/make_fig1.py', 'inputs/manuscript_extract_v0.9.24.json', os.path.join(OUT, 'Fig1'))  # asserts the counts it draws
run('code/verify_counts.py', OUT)                                                # independent recount from the rebuilt CSV files
fail = []
# 1. content: CSV text and workbook cells
import openpyxl
for f in sorted(os.listdir(os.path.join(REF, 'csv'))):
    same = open(os.path.join(REF, 'csv', f), encoding='utf-8').read() == open(os.path.join(OUT, 'csv', f), encoding='utf-8').read()
    print('CONTENT', 'same     ' if same else 'DIFFERENT', 'csv/' + f); fail += [] if same else ['csv/' + f]
X = 'CEE_Supplementary_Tables_v0.9.24.xlsx'; a, b = (openpyxl.load_workbook(os.path.join(d, X)) for d in (REF, OUT))
cells = lambda wb: {(ws.title, c.coordinate): c.value for ws in wb.worksheets for row in ws.iter_rows() for c in row if c.value is not None}
same = a.sheetnames == b.sheetnames and cells(a) == cells(b); print('CONTENT', 'same     ' if same else 'DIFFERENT', X, '(all cells of all sheets)'); fail += [] if same else [X]
# 2. file hashes, reported separately
exp = dict(reversed(l.split('  ', 1)) for l in open(os.path.join(REF, 'SHA256SUMS'), encoding='utf-8').read().splitlines()); bytes_diff = []
for rel, h in sorted(exp.items()):
    got = hashlib.sha256(open(os.path.join(OUT, rel), 'rb').read()).hexdigest(); print('BYTES  ', 'same     ' if got == h else 'different', rel); bytes_diff += [] if got == h else [rel]
if X in bytes_diff:
    za, zb = (zipfile.ZipFile(os.path.join(d, X)) for d in (REF, OUT)); m = za.namelist() == zb.namelist() and all(za.read(n) == zb.read(n) for n in za.namelist())
    print('NOTE: workbook members after decompression:', 'identical (only the ZIP compression differs)' if m else 'differ (XML serialisation differs; cells compared above)')
if 'Fig1.png' in bytes_diff:
    import numpy as np; from PIL import Image
    p = [np.asarray(Image.open(os.path.join(d, 'Fig1.png')).convert('RGBA')) for d in (REF, OUT)]
    n = int((p[0] != p[1]).any(axis=-1).sum()) if p[0].shape == p[1].shape else -1
    if n == 0: bytes_diff.remove('Fig1.png'); print('NOTE: Fig1.png has identical pixels; only its compression stream differs (not counted as a byte difference)')
    else: print('NOTE: Fig1.png pixels differing:', n if n >= 0 else 'image size differs', 'of', p[0].shape[0] * p[0].shape[1], '(text rendering depends on matplotlib, FreeType and font versions; the counts drawn are asserted by the script)')
if fail: sys.exit('FAILED (content): ' + ', '.join(fail))
if '--strict' in sys.argv and bytes_diff: sys.exit('FAILED (strict byte check): ' + ', '.join(bytes_diff))
print('REPRODUCED: counts verified; CSV text and all workbook cells identical to ./outputs.' + ('' if not bytes_diff else ' File bytes differ for: ' + ', '.join(bytes_diff) + ' (see ENVIRONMENT.md).'))
