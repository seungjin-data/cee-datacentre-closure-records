# Not included, and why

| Material | Reason | What is provided instead |
|---|---|---|
| Agency documents (EPA licences, inspector reports, closure plans, annual reports, the EPA list, CRU, EirGrid and ESB Networks publications), including page extracts | Published by third parties; reuse terms were not checked document by document. Only the short assessment wording of each inspector report is quoted | `registers/source_register.csv`: publisher, date, URL where recorded, held file name, SHA-256, pages used |
| Financial statements of the eight companies | Purchased from the Companies Registration Office; not for redistribution | CRO number, file name and SHA-256 in Supplementary Table 6 and the source register |
| Press and trade articles for the 27 tracking records | Copyright of the publishers | Title and date in Supplementary Tables 1 and 2 |
| Records released under access-to-information requests, and the correspondence around them | Contain personal names, email addresses and signatures | Document identifiers and hashes where the record is used |
| The author's working ledgers, audit notes and internal instructions | Working papers with internal notes; superseded by the derived tables | The derived tables and the checks in `code/` |
| The manuscript, cover letter and review correspondence | Under preparation or confidential | An extract of the manuscript tables in `inputs/` used only to assert the counts |
| Protocol version 2 and the amendment log | Awaiting the author's approval | To be added by the author if approved |
| Local file paths and personal contact details | Private | None |
