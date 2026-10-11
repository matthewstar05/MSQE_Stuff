# Validation record

Validated locally on 2026-10-10 from an isolated clone of the team repository. Source revision: `0ef7bc14e6a964ce66fe4c105a672b0b758d7277`. Only the new `Draft Submission/` tree is changed; the upstream analysis and published site files are preserved.

## Google Doc and exports

Edited the exact requested Google Doc in place, tab `t.0`; it was blank before editing. Final saved native readback confirms 8 embedded image objects, 27 bracketed writing/review prompts, required section headings, and 72-point margins on US Letter pages.

The PDF and DOCX were downloaded through authenticated Google Drive exports after the final changes. These are actual exports of the edited Google Doc. The PDF has 14 pages: 5 reserved narrative pages, references, attribution/submission notes, and 7 exhibit pages. Figures and references are outside the narrative allocation. All pages were rendered and visually reviewed in a contact sheet, with larger inspections of the dense regression/sensitivity pages. No clipping, overlap or stranded captions was observed. The DOCX contains 8 embedded images.

The source Markdown and figure snapshots permit offline review; the Google Doc remains the working master. Refresh both exports after team edits.

## Reproduction execution

Ran the self-contained copy in `Draft Submission/Replication/Data-Parsing` using its sibling `Resources` folder:

```
python3 -u run_all.py
Rscript crosscheck_clogit.R
```

**Both commands exited 0.** All eight Python stages completed: parse (2 s), descriptives (under 1 s), CL (45 s), ML (219 s), dashboard (under 1 s), slides (under 1 s), paper figures (60 s), and discrepancy diagnostics (79 s). Complete outputs are in `pipeline_validation.log` and `r_validation.log`.

The local environment was Python 3.9.6 with versions recorded in `environment.txt`. Upstream recommends Python 3.10+ for normal reproduction; this successful local run does not establish general support for Python 3.9. R and its `survival` package were available.

## Checked evidence

- The raw data SHA-256 matches the source-repository file byte for byte: 2,160 rows, 147 columns.
- Parsed data retain 180 people; the estimation sample uses 164 people, 656 occasions, 1,968 alternative rows, and 123 councillors. Every complete occasion has three alternatives and one selection.
- All five monetary-information interactions match their attribute-by-treatment definitions on every parsed row.
- All 36 Figure 1 counts match the published-count comparison.
- All 48 R/Python CL coefficient/p-value pairs (12 regressors, two samples, two groupings) agree within 0.0011 using rounded saved outputs. R verifies model-based p-values, not respondent-clustered inference.
- Both primary ML fits report convergence and use 2,000 draws. Primary coefficients and uncertainty estimates are finite; each sample has 20 finite 500-draw sensitivity runs.
- Numeric columns in the rerun `table3_cl.csv`, `table3_ml.csv`, and separate paper-figure regression comparison match the committed source exactly at saved precision (maximum absolute difference 0).
- The memo's exact source-commit images and numerical CSVs are preserved. Exhibit ML uses 500 draws; primary ML uses 2,000. The memo labels these separately.
- `verify_package.py` checks file hashes and key saved-result invariants. The manifest excludes itself.

## Warnings and remaining limitations

The Python run emitted **48 NumPy RuntimeWarnings** involving divide-by-zero, overflow or invalid matrix multiplication during estimation. The pipeline completed; primary saved coefficients/standard errors and sensitivity coefficients/log likelihoods are finite, primary fits report convergence, and rounded outputs agree with the source snapshot. These checks do not establish a global optimum or eliminate simulation sensitivity. The warnings are retained in the log.

The notebook was not executed separately; it is the existing narrated companion to the canonical scripts. No Stata run or author confirmation was obtained. The custom respondent-clustered covariance calculation was not independently reimplemented. Preserved upstream diagnostics sometimes assert author errors more strongly than warranted; the memo and source notes distinguish observed mismatches from possible explanations.

This is the requested iterative template. Narrative, final recommendations, actual contribution claims and team review remain to be written. It is not a completed five-page prose memo. No Canvas submission was made.
