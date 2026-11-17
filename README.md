# Data and code for: Tracing closure obligations and payments in public data-centre records

**Release 1.0.0 (18 November 2026).** Archived at Zenodo through the GitHub release `v1.0.0`; the DOI of this version is shown on the Zenodo record and in the citation box of the repository.

Author: SeungJin Kim (ORCID 0009-0007-6876-0777), Institute for Industrial Policy Studies (IPS), Seoul, Republic of Korea.

This repository holds the derived data, registers and code behind a study of how far closure obligations, costs, financial assurance, payments and environmental evidence for data centres can be traced in public records. It matches manuscript version 0.9.24 and supplementary tables version 0.9.24 (18 November 2026).

## Roles

The author obtained the original source documents, reviewed them directly and decided the coding, the analysis, the interpretation and what was finally adopted. ChatGPT (OpenAI; labelled GPT) and Claude (Anthropic) assisted with source searches, cross-checking document readings and citations, verifying calculations, preparing the scripts in `code/`, and drafting, translation and language editing. The tables record the method and scope of each AI-assisted verification (document, page, access method, limits). In the table cells, "auditor" means a check made with GPT, and "second reader" or "second verifier" a check made with Claude; they are not independent double reading by two human readers.

## Two record sets, reported separately

* **18 identified Irish EPA industrial emissions licences** for data centres (versions valid at 31 December 2025), read with the EPA list of **197 registrations** with financial provision requirements at that date and the filed financial statements of the **eight** licence-holding companies. The 18 and the 197 were selected by different criteria and share one registration (P1191); they are not compared.
* **27 international tracking records** of data-centre closures and related events in six countries.

The two sets concern different facilities and are never pooled.

## Contents

| Path | What it is |
|---|---|
| `inputs/` | Coding files read by the build script, and an extract of the manuscript tables against which every count is asserted |
| `code/build_supplement.py` | Builds Supplementary Tables 1 to 7 (XLSX and one CSV per sheet) |
| `code/make_fig1.py` | Draws Fig. 1; every number drawn is read from the tables and asserted |
| `code/verify_counts.py` | Independent recount from the rebuilt CSV files |
| `reproduce.py` | Runs the three scripts and compares the result with `outputs/` |
| `outputs/` | The deposited tables (XLSX, CSV), Fig. 1 (PNG, PDF) and `SHA256SUMS` |
| `registers/source_register.csv` | Sources by publisher, date, URL where recorded, held file name, SHA-256, pages used |
| `registers/cru_guided_register_v1.1.csv` | The 33 system-level connection documents (31 read, 2 could not be opened) |
| `registers/irish_18_verification_register.csv` | For each of the 18 licences: the initial inspector report, its SHA-256, URL and page, cross-checked on 18 November 2026. A verification register, not a search log: the historical search terms and exclusion record were not recovered |
| `registers/source_reuse_disposition_103.csv` | Reuse disposition for 103 source-register rows as audited on 18 November 2026 (rows added later are not covered): no original redistributed; publisher permission not determined |
| `registers/author_held_archive_inventory_81.csv` | File-level inventory of one archive of agency documents held by the author (81 distinct files) |
| `CODEBOOK.md` | The five questions (O, C, A, P, E), status codes and column definitions |
| `EXCLUDED.md` | What is not in this repository and why |
| `ENVIRONMENT.md`, `requirements.txt` | Software versions |
| `LICENSE`, `LICENSE-DATA.md` | MIT licence for the code; Creative Commons Attribution 4.0 International for the data, registers and documentation |

## Reproduce

```
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python3 reproduce.py
```

The script rebuilds everything into `rebuild/` and prints each check. The result is decided on content: the counts, the text of every CSV file and every cell of the workbook must equal `outputs/`. File hashes are then reported separately, because XLSX compression and figure rendering depend on library versions. `python3 reproduce.py --strict` also fails on any byte difference and is meant for the reference environment. `ENVIRONMENT.md` records what was reproduced in which environment.

Counts checked: EPA list 197 = 162 (closure cost and instrument) + 13 + 1 + 21; tracking records 27, operation ended 21, equipment removal 7, demolition 4 stated complete and 2 qualified, amount recorded 5; two separate verdict columns for the final account and the final net cost bearer (7 not identified, 20 not judged, 0 identified in each); 56 cells for the eight US records (27 documented, 29 negative observations); 18 licences joined to 18 inspector reports; closure-cost statements 5 / 1 / 1 / 11; company statements 3 of 8 with a disclosed provision and 0 of 8 attributed to an identified licensed data centre; 2025 annual reports 56 incident notifications across 12 licences (alternative count 53 across 11).

## Where each reported number comes from

| In the manuscript | Rebuilt file and column | Input | Checked by |
|---|---|---|---|
| Table 1: 18 licences; costing statements 5 / 1 / 1 / 11; 1 licence on the EPA list | `outputs/csv/S3_Licences_18.csv` (closure-cost statement: counted as; EPA list at 31 Dec 2025) | `inputs/S3_base_18.csv`, `S3_closure_cost_statements_v097.csv`, `S3_initial_inspector_reports_18.csv` | build script (against Table 1) and `verify_counts.py` |
| Table 2: 197 registrations = 162 + 13 + 1 + 21; 163; 131 | `outputs/csv/S4_EPA_list_197.csv` | `inputs/S4_epa_list_197.csv` | build script (against Table 2) and `verify_counts.py` |
| Table 3 and Fig. 1b: 27 / 21 / 7 / 4 / 2 / 5; final account and final net cost bearer 0 identified, 7 not identified, 20 not judged | `outputs/csv/S1_Tracking_27.csv` | `inputs/S1_base_27.csv`, `S1_two_verdicts_GPT_audit_2026-11-17b.csv` | build script (against Table 3, by country) and `verify_counts.py` |
| Table 4: 56 cells (27 documented, 29 not established) | `outputs/csv/S2_US_cells_56.csv` | `inputs/S2_*.csv` | build script (cell text taken from Table 4) and `verify_counts.py` |
| Results: 2025 annual reports for 16 of 18 licences; 56 notifications across 12 licences; 53 across 11 | `outputs/csv/S7_AER_2025_18.csv` | `inputs/S7_AER_2025_18.csv` | build script (against the Results text) and `verify_counts.py` |
| Results: 3 of 8 companies with a disclosed provision; 0 attributed to a licensed site | `outputs/csv/S6_Company_statements.csv` | values in `code/build_supplement.py` | build script and `verify_counts.py` |
| Table 5 and the amounts in the Results | `outputs/csv/S5_Amounts.csv` (listed, not recomputed) | values in `code/build_supplement.py` | read against the sources named in each row |
| Fig. 1 | `outputs/Fig1.png`, `outputs/Fig1.pdf` | `inputs/manuscript_extract_v0.9.24.json` | figure script asserts the counts it draws |

Table 6 of the manuscript is a summary in words and is not rebuilt.

## What the data do and do not show

* "Not observed", "not identified" and "not judged" describe the records examined. They are not findings that a cost, an instrument, a payment or a measurement does not exist.
* A shared registration number links entries to an installation. It does not state which liability an instrument covers.
* Amounts at different stages (budget, contract, statement of payment, recorded spending) are not added or netted.
* No future cost is estimated.

## Verification status

* The two verdict columns in Supplementary Table 1 come from the auditor's source check of 17 November 2026: held originals were reopened for four cases (several documents for one of them), public source text was read for 22 cases, and for one (C15) only a search extract was available. It is not a re-reading of every original for all 27 records.
* The search terms and exclusion record that produced the set of 18 licences could not be reproduced from the project files; the set is not claimed to be complete. Its membership is documented in `registers/irish_18_verification_register.csv`.
* For tracking record C15 the link between the source article and the site was resolved with secondary sources (a broker page and the indexed text of the article); the full article page was not downloaded, and its two final verdicts stay not judged.
* Three background references whose full text could not be obtained were removed from the manuscript, which now cites 21 references; reference 1 was checked from page images, without text extraction.
* Most 2025 annual environmental reports were read from the EPA-published PDF via the web; the reading basis is given per row in Supplementary Table 7.
* `registers/source_register.csv` gives one source locator per tracking record (the source of the two verdicts) from the auditor's crosswalk; 23 of the 27 URLs returned a public response when opened on 17 November 2026 and 4 did not. The other case documents are cited by title and date in Supplementary Tables 1 and 2. Not every register row has a URL, a date and a hash; empty fields mean that the item was not recorded.
* The inspector-report input carries only the assessment wording, page, URL and SHA-256 of each report, not page extracts.

## Citation

See `CITATION.cff` and the Zenodo record of this release. The manuscript title is the title at the time of release and may change during peer review.
