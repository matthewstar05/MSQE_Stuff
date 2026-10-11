# Team 3: Draft Submission

Replication of Eppink, Winden, Wright and Greenhalgh (2016), *Non-Market Values in a Cost-Benefit World: Evidence from a Choice Experiment*.

**Status: draft writing template.** The figures and supporting files are populated; bracketed narrative sections, actual contribution statements and team review remain to be completed. This is not a finished five-page memo.

## Submit now versus package for later

The user-provided saved Canvas assignment, **Draft Replication Memo**, is due **October 11, 2026 at 11:59 pm**. Its text asks for the draft memo now and says the data and replication files do **not** have to be submitted yet. They are organized here for the final submission. No Canvas upload or submission has been performed.

- **Draft memo:** `Memo/Team3_Draft_Replication_Memo.pdf`, downloaded from the edited Google Doc. The `.docx` is an editable export of the same document.
- **Working master:** [5560 G3 Replication Draft](https://docs.google.com/document/d/1FzXGMijtagZ8z7D-jOVymoIqLtOcgDA6rQEgrsZA4uw/edit?tab=t.0). After team edits, download PDF and Word again and replace the exports here.
- **Replication files:** `Replication/` is self-contained. Preserve `Data-Parsing/` and `Resources/` as siblings so relative paths work.
- **Provenance and checks:** `Documentation/` explains sources, data coding, literature verification, execution results and file integrity.

## Folder guide

```
Draft Submission/
  Memo/
    Team3_Draft_Replication_Memo.pdf
    Team3_Draft_Replication_Memo.docx
    Memo_Template_Source.md
    Figures/                         exact images embedded in the memo
    Supporting_Tables/               committed numerical evidence behind memo images
  Replication/
    Resources/
      S1Table.DTA                     immutable public raw data
      Eppink_2016_PLoSONE_paper.pdf
    Data-Parsing/
      01_parse_data.py ... 08_debug_discrepancies.py
      common.py, run_all.py, requirements.txt, crosscheck_clogit.R
      replication_walkthrough.ipynb
      REPLICATION_LOG.md, CHECKIN_WEEK5.md, README.md
      dashboard/                     source template and offline output
      replication-targets/           original article exhibits
      output/                        derived CSVs, model JSON, tables, plots and logs
  Documentation/
    COURSE_REQUIREMENTS.md
    DATA_GUIDE.md
    SOURCES_AND_LITERATURE.md
    VALIDATION.md
    pipeline_validation.log
    r_validation.log
    environment.txt
  MANIFEST_SHA256.csv
```

`Memo/Figures` and `Memo/Supporting_Tables` preserve the exact committed evidence used in the memo (source revision `0ef7bc14e6a964ce66fe4c105a672b0b758d7277`). `Replication/Data-Parsing/output` contains the verification rerun and may have small platform-dependent numerical differences. The main ML pipeline uses 2,000 draws; the paper-exhibit redraw uses 500 draws. Their coefficient tables must not be mixed without a label.

## Reproduce from this folder

The upstream scripts document Python 3.10+ as the supported version. Use a virtual environment; R is optional. Full execution can take several minutes, especially the mixed-logit sensitivity runs.

```sh
cd Replication/Data-Parsing
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -u run_all.py
Rscript crosscheck_clogit.R
```

The R command requires `survival` and must run from `Data-Parsing`. It independently checks CL coefficients and model-based p-values; it does not validate Python's respondent-clustered standard errors. Read `Documentation/VALIDATION.md` for what was actually checked and any numerical warnings. The notebook is a narrated companion; the numbered scripts are the canonical pipeline. The offline dashboard is `Replication/Data-Parsing/dashboard/index.html`.

## Finish the memo

Replace every bracketed writing prompt; keep about five pages of narrative, single-spaced, 11-12 pt and 1-inch margins. References, tables and figures are additional pages. Integrate at least five scholarly sources beyond the original paper into the prose. Confirm actual contributions and AI-use disclosure. Retain uncertainty about author-code and data-history explanations. Export the updated master again, then run `python3 Documentation/verify_package.py --refresh-manifest` to regenerate and check the integrity manifest.

The original article and public S1 Table are CC BY 4.0; credit Eppink et al. (2016), DOI: https://doi.org/10.1371/journal.pone.0165365. Existing analysis code and documentation are preserved from the team repository; this package does not add a new license. Saved Canvas HTML, account identifiers, private meeting links, caches, virtual environments and the separately supplied I4R example PDF are excluded.
