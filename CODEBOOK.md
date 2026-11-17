# Codebook

## The five questions (O, C, A, P, E)

The questions describe the existing coding. They are not a score, a pass rate or a causal sequence.

| Item | What is read in the source | What that record can support |
|---|---|---|
| O, Obligation | The valid licence version and condition, the obligated party, the work required, the trigger | The duty to close and restore is read separately from any duty to submit a plan or a cost in advance |
| C, Costing | Scope of the work, whether a cost was estimated, the amount, whether it was agreed with the regulator | A statement that costs were not estimated is recorded as such; an operator estimate and an agreed amount are kept apart |
| A, Assurance | Type of instrument, the facility named, the liability secured, the stated scope | A shared registration number supports a link to the installation. Coverage of a specific liability needs the wording of the instrument or another explicit link |
| P, Payment | Payer, recipient, amount, the work paid for, the transaction status the document supports | Budget, contract, statement of payment and recorded spending are kept apart. The final account of the works and the party bearing the final net cost of restoration are two separate verdicts |
| E, Exposure | Whether comparable site measurements from before and after closure exist | A change in soil or groundwater condition needs matching location, medium, parameter and date. Judging residual exposure of people or ecosystems also needs evidence on pathways and receptors |

The 18 Irish licences bear on O, C and A. The 27 tracking records bear on P and E. No site is followed through all five.

## Status codes (kept apart; none is a negative finding about the world)

| Code as written in the tables | Meaning |
|---|---|
| `not identified in the documents reviewed` | Project or financial documents were reviewed for this record and do not identify the item |
| `not judged (event-level sources only)` | Only sources describing the event were available, so no verdict was made. Not counted as a negative observation |
| outside the scope by design (grey boxes in Fig. 1) | The record set was not examined for this question: the licences are not followed to closure, and the tracking records were not read for licence-stage obligations |
| `not established in the sources reviewed` (S2) | The case sources listed, read to 17 November 2026, contain no such statement |
| `Not listed` / not observed (S3) | No entry was found in the defined source. It does not mean that no cost or instrument exists |
| `no costing document obtained` (S3) | No document with a costing statement was obtained; whether a cost exists cannot be said |
| `no report found` (S7) | No 2025 annual report was found on the register; not a finding that none was filed |

## Files in `outputs/csv/` (one per supplementary table; the first row is the header)

| File | Unit | Key columns |
|---|---|---|
| `S1_Tracking_27.csv` | tracking record (C01 to C27) | operation ended and its basis; equipment removal; demolition (stated complete, qualified); amount recorded; two verdicts with basis, source, page or item, AI-assisted verification |
| `S2_US_cells_56.csv` | cell (8 US records by 7 stages) | cell text, status, verification class, evidence or search scope (AI-assisted verification), cross-check with Claude |
| `S3_Licences_18.csv` | licence | closure condition, provision clause, inspector report (date, page, wording, URL, SHA-256), closure-cost statement and how it is counted, EPA list status, operator answer, 2026 amendment note (not used) |
| `S4_EPA_list_197.csv` | registration | presence (1) in the incident-cost, closure-cost and instrument tables of the EPA list; energy-sector flag |
| `S5_Amounts.csv` | amount record | amount, what it is, stage, source with verification method and scope, treatment |
| `S6_Company_statements.csv` | company | CRO number, file name and SHA-256, period, provisions, location in the statements, attribution to a licensed site |
| `S7_AER_2025_18.csv` | licence | 2025 report found, register document ID, provision answer and basis, incident count (table), alternative count, pages, verification method and scope |
| `README.csv` | check | the checks printed by the build script |

Identifiers: licences `P####-01`; EPA list registrations `P####` or `W####`; tracking records `C01` to `C27`. Dates are ISO or written out. Amounts are quoted in the currency of the source.
