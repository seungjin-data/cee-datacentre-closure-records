# Fig. 1. Usage: python3 code/make_fig1.py inputs/manuscript_extract_v0.9.24.json OUTPUT_PREFIX
# Public copy of the author's figure script: reads the manuscript extract instead of the full manuscript. Every count drawn is read from the tables and asserted.
# Reads every count from the manuscript tables and captions in <content.json> and asserts it; nothing is typed in by hand.
import json, re, sys, textwrap, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib import font_manager
for f in ("LiberationSans-Regular.ttf", "LiberationSans-Bold.ttf"):
    try: font_manager.fontManager.addfont("/usr/share/fonts/truetype/liberation/" + f)
    except Exception: pass
plt.rcParams.update({"font.family": ["Liberation Sans", "DejaVu Sans"], "font.size": 7, "pdf.fonttype": 42, "svg.hashsalt": "fig1", "path.simplify": False, "text.hinting": "no_hinting", "figure.dpi": 200.0})  # hinting and dpi pinned: they differ between matplotlib installations and change the PNG bytes
src, out = sys.argv[1], sys.argv[2]
c = json.load(open(src, encoding="utf-8"))
T = lambda o: "".join(r["t"] for r in o["runs"])
tabs = [o["rows"] for o in c if o["k"] == "t"]
t1 = {r[0]: int(r[1]) for r in tabs[0][1:]}
tot3 = dict(zip(tabs[2][0], tabs[2][-1]))
g3 = lambda k: int(tot3[k])
n_obl = t1["Closure obligation in licence (Condition 10.1)"]; n_adv = t1["Closure plan or cost required in advance by the licence"]
n_ne = t1["Closure plan filed with the initial application states that closure costs were not estimated"]
n_rev = t1["Same statement in a closure plan filed in a licence review (P1113)"]
n_unm = t1["Same statement in an earlier reading, not matched to the application (P1170)"]
n_nod = t1["No costing document obtained"]; n_lst = t1["Listed as requiring financial provision"]
assert (n_obl, n_adv, n_ne, n_rev, n_unm, n_nod, n_lst) == (18, 0, 5, 1, 1, 11, 1) and n_ne + n_rev + n_unm + n_nod == 18
assert t1["Agreed closure cost in list"] == 0 and t1["Provision instrument in list"] == 0
tr, end, eq, dem, qual, amt, fin = (g3(k) for k in ["Tracked", "Operation ended", "Equipment removal", "Demolition: stated complete", "Demolition: qualified", "Amount recorded", "Final cost bearer identified"])
assert (tr, end, eq, dem, qual, amt, fin) == (27, 21, 7, 4, 2, 5, 0)
cap3 = [T(o) for o in c if o["k"] == "p" and T(o).startswith("Table 3 |")][0]
assert "For seven records with project-level documents, the documents reviewed do not identify it; for the other 20 the available sources describe the event" in cap3
assert any("All 18 original inspector reports for the initial licences assessed" in T(o) and "financial provision as unnecessary" in T(o) for o in c if o["k"] == "p")
t6 = {r[0]: r for r in tabs[5]}; assert "soil or groundwater before and after closure" in t6["27 international tracking records"][2]

LINKS = [("O", "Obligation"), ("C", "Costing"), ("A", "Assurance"), ("P", "Payment"), ("E", "Exposure")]
A = [[f"Closure obligation in {n_obl} of 18 licences"],
     [f"Licence condition: plan or cost required in advance in {n_adv} of 18", f"Closure plans read that state costs were not estimated: {n_ne + n_rev}", f"Earlier reading not matched to a document (P1170): {n_unm}", f"No costing document obtained: {n_nod}"],
     ["Inspector at application: provision unnecessary in 18 of 18", f"On the EPA provision list: {n_lst} of 18, with no agreed cost or instrument"],
     None, None]
B = [None, None, None,
     [f"Amounts recorded for exit, relocation or closure: {amt} (not all payments)", "Final cost bearer: not identified in 7 records reviewed; not judged in 20"],
     ["Paired soil or groundwater measurements before and after closure: not found"]]
BLUE, FILL, GREY, GFILL = "#2E74B5", "#D9EAF7", "#9A9A9A", "#F2F2F2"
W, H = 7.0, 4.95
fig = plt.figure(figsize=(W, H)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
x0, bw, gap = 0.08, 1.12, 0.30
def row(y, h, title, letter, content, grey_text, arrows):
    ax.text(0.04, y + h + 0.15, letter, fontsize=9, fontweight="bold", va="bottom")
    ax.text(0.26, y + h + 0.15, title, fontsize=8, fontweight="bold", va="bottom")
    for k, ((L, name), items) in enumerate(zip(LINKS, content)):
        x = x0 + k * (bw + gap); on = items is not None
        ax.add_patch(FancyBboxPatch((x, y), bw, h, boxstyle="round,pad=0,rounding_size=0.06", lw=0.9 if on else 0.7,
                     ec=BLUE if on else GREY, fc=FILL if on else GFILL, ls="-" if on else (0, (3, 2))))
        ax.text(x + 0.08, y + h - 0.08, L, fontsize=10, fontweight="bold", color=BLUE if on else GREY, va="top")
        ax.text(x + 0.30, y + h - 0.105, name, fontsize=7.5, fontweight="bold", color="black" if on else GREY, va="top")
        yy = y + h - 0.36
        for s in (items if on else [grey_text]):
            if s == "---":
                ax.plot([x + 0.08, x + bw - 0.08], [yy + 0.01, yy + 0.01], color=BLUE, lw=0.6); yy -= 0.06; continue
            bold = s.startswith("*"); s = s.lstrip("*")
            s = re.sub(r":\s(\d)", ":\u00a0\\1", s); s = re.sub(r"(\s)(\d+)$", "\u00a0\\2", s); s = re.sub(r"in (\d+) of (\d+)", "in\u00a0\\1\u00a0of\u00a0\\2", s)
            w = textwrap.wrap(s, 21)
            ax.text(x + 0.08, yy, "\n".join(w), fontsize=6.5, color="black" if on else GREY, va="top", linespacing=1.12, fontweight="bold" if bold else "normal")
            yy -= 0.112 * len(w) + (0.02 if bold else 0.05)
        assert yy > y - 0.02, ("text overflow", letter, L, round(y - yy, 3))
        if arrows and k < 2:
            ax.add_patch(FancyArrowPatch((x + bw + 0.03, y + h / 2), (x + bw + gap - 0.03, y + h / 2), arrowstyle="-|>", mutation_scale=8, lw=0.8, color="#555555"))
row(2.73, 1.85, "Facilities in operation: 18 identified Irish EPA data-centre licences", "a", A, "Outside scope by design: licences are not followed to closure", True)
row(0.92, 1.36, "International tracking records (n = 27)", "b", B, "Outside the scope of the tracking records", False)
# physical events strip (not a link of the chain)
xs, xe = x0, x0 + 5 * bw + 4 * gap
ax.add_patch(Rectangle((xs, 0.18), xe - xs, 0.52, lw=0.8, ec="#555555", fc="white"))
ax.text(xs + 0.08, 0.62, "Physical closure events recorded in the same 27 records (not payments)", fontsize=7, fontweight="bold", va="top")
ax.text(xs + 0.08, 0.40, f"Operation ended: {end}     Equipment removal: {eq}     Demolition stated complete: {dem}; qualified: {qual}", fontsize=6.8, va="top")
fig.savefig(out + ".png", dpi=400, metadata={"Software": None}); fig.savefig(out + ".pdf", metadata={"CreationDate": None, "Producer": None, "Creator": None})
print("ok", (n_obl, n_adv, n_ne, n_rev, n_unm, n_nod, n_lst), (tr, end, eq, dem, qual, amt, fin))
