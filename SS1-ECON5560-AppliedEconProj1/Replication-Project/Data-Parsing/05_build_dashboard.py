"""
Step 5 - Build the interactive dashboard (dashboard/index.html).

Collects every result written by steps 1-4 into one JSON object and injects it into
dashboard/template.html (plain HTML/CSS/JS, no external libraries, works offline).
Open dashboard/index.html in any browser. If a ../docs folder exists (the team repo),
the same page is copied there for GitHub Pages.
"""
import json
import platform
from datetime import date
import pandas as pd
import numpy as np
import scipy, statsmodels
from common import HERE, DATA_OUT, RES_OUT, VARS, MAIN, LABELS, PAPER_T3

desc = json.loads((RES_OUT / "descriptives.json").read_text())
cl = json.loads((RES_OUT / "cl.json").read_text())
ml = json.loads((RES_OUT / "ml.json").read_text())

long = pd.read_csv(DATA_OUT / "choice_long.csv", keep_default_na=False, na_values=[""])
example_id = 2   # a treatment-3 respondent, so the "$ shown" columns are switched on
ex = long[long.id == example_id][["choice_set", "card", "alt_label", "development", "water", "cultural", "chosen",
                                  "res_money", "low_money", "med_money"]]

data = {
    "meta": {"built": date.today().isoformat(), "python": platform.python_version(),
             "pandas": pd.__version__, "numpy": np.__version__, "scipy": scipy.__version__,
             "statsmodels": statsmodels.__version__},
    "vars": [{"key": v, "label": LABELS[v], "group": "main" if v in MAIN else "treat"} for v in VARS],
    "paper": PAPER_T3,
    "cl": {k: v for k, v in cl.items() if k in ("m1", "m2")},
    "cl_relative": cl["relative"],
    "ml": {k: {"primary": ml[k]["primary"], "relative": ml[k]["relative"],
               "runs": [{"ll": r["ll"], "coef": r["coef"]} for r in ml[k]["sensitivity"]]} for k in ("m3", "m4")},
    "fig2": {t: {kk: ml["fig2"][t][kk] for kk in ("grid", "density", "p2_5", "p97_5", "mean")} for t in ml["fig2"]},
    "example": {"id": example_id, "rows": ex.to_dict(orient="records")},
    **desc,
}
page = (HERE / "dashboard" / "template.html").read_text()
page = page.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":"), default=float))
# template = <head> material (title, fonts, styles) followed by the page body; wrap it as a full document
cut = page.index("</style>") + len("</style>")
html = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
        "[hidden]{display:none!important}img{max-width:100%}</style>\n"
        + page[:cut] + "\n</head>\n<body>\n" + page[cut:] + "\n</body>\n</html>\n")
(HERE / "dashboard" / "index.html").write_text(html)
print(f"Wrote dashboard/index.html ({len(html) / 1024:.0f} KB)")
docs = HERE.parent / "docs"            # in the team repo, GitHub Pages serves docs/index.html
if docs.is_dir():
    (docs / "index.html").write_text(html)
    print("Also wrote ../docs/index.html (GitHub Pages)")
