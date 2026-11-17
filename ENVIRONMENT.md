# Environment used to produce ./outputs

| Component | Version |
|---|---|
| Operating system | Ubuntu 24.04.5 LTS |
| Python | 3.13.18 |
| openpyxl | 3.1.5, with lxml 6.1.3 (openpyxl writes slightly different XML when lxml is absent, which changes the XLSX bytes but not the cell values) |
| matplotlib | 3.11.2 (FreeType 2.14.3) |
| numpy | 2.5.3 |
| Pillow | 12.3.0 |
| Fonts for Fig. 1 | Liberation Sans 2.1.5 (Debian/Ubuntu package fonts-liberation 1:2.1.5-3), read from /usr/share/fonts/truetype/liberation/ |

## What was reproduced where

* **Reference environment (the versions above; fresh virtual environment built from `requirements.txt`).** `python3 reproduce.py --strict` passes: CSV, XLSX and Fig1.pdf are byte-identical; Fig1.png has identical pixels and can differ only in its compression stream.
* **Independent run by the auditor on v0.9.11 (Python 3.12.14, openpyxl 3.1.5, lxml 6.1.1, matplotlib 3.10.8; the pinned versions could not be installed there).** All count checks passed; the eight CSV files were byte-identical; all cells of all workbook sheets and all decompressed workbook members were identical; the XLSX file hash differed (ZIP compression); Fig1.pdf bytes differed and Fig1.png differed at 213,516 of 5,936,000 pixels. The cause of the figure difference across environments is not established; pinning the hinting and dpi settings in the script removes one known cause only.

* **Independent run by the auditor on v0.9.17.** Default mode exit code 0; eight CSV files and all workbook cell values matched; figure rendering differed across environments as before.
* **Independent run by the auditor on v0.9.16.** Default mode exit code 0: all eight CSV files and all workbook cell values matched; decompressed workbook members identical; XLSX file bytes differed; Fig1.pdf bytes differed and Fig1.png differed at 217,127 of 5,544,000 pixels. Strict success in the reference environment is reported by the package author and was not independently established.
* **Independent run by the auditor on v0.9.12.** Default mode exit code 0 (counts, eight CSV files and all workbook cells identical); `--strict` exit code 1 because file bytes differed.

For this reason `reproduce.py` decides on content (counts, CSV text, workbook cells) and reports file hashes separately; `--strict` is meant for the reference environment.

The figure script reads the counts it draws from the manuscript tables and asserts them; box labels and explanatory wording are literal text in the script.
