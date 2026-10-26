# FIN409 agent submission package inventory

Prepared: 26 October 2026. No upload, publication, remote repository creation or report modification occurred.

## Measured upload folder

- Folder: FIN409_Agent_Submission
- File count: **161** regular files (includes this inventory and the package manifest; excludes empty directories).
- Total uncompressed file size: **92,364,279 bytes (88.09 MiB)**.
- Curated evidence: **207 records; 134 source assets**, all manifest-listed assets included unchanged.
- Missing required source assets: **none**.
- One isolated example report, reader references and its 31-claim source mapping are under examples/completed_english_report; they are not formal analysis inputs.
- Manifest: package_manifest.json covers every delivery file except itself and this self-describing inventory.

## Largest files

| Package-relative path | Bytes | MiB |
|---|---:|---:|
| evidence/english/v001/sources/e9c2d7fdd088e151__比亚迪_2024年年度报告.pdf | 10092140 | 9.62 |
| evidence/english/v001/sources/710d8b2e08e37ba5__比亚迪_2025年年度报告.pdf | 7533972 | 7.18 |
| evidence/english/v001/sources/959d6d51d529fd51__亿纬锂能_2023年年度报告.pdf | 6280048 | 5.99 |
| evidence/english/v001/sources/06be1a045d1ec713__亿纬锂能_2024年年度报告.pdf | 5988065 | 5.71 |
| evidence/english/v001/sources/6081f0377617dddb__宁德时代2023年度报告.pdf | 5986207 | 5.71 |
| evidence/english/v001/sources/3bee0ca9a6232c60__亿纬锂能_2025年年度报告.pdf | 5815598 | 5.55 |
| evidence/english/v001/sources/21ef29ff66c6e13d__iea2024.pdf | 5227203 | 4.99 |
| evidence/english/v001/sources/7522f23a3844c6a5__GlobalEVOutlook2025.pdf | 4996288 | 4.76 |
| evidence/english/v001/sources/cacf470f2dea6d0c__国轩高科_2024年年度报告.pdf | 4257494 | 4.06 |
| evidence/english/v001/sources/865d69b0da6dfa05__国轩高科_2023年年度报告.pdf | 4063097 | 3.87 |
| evidence/english/v001/sources/b4f1713d7b821eb0__宁德时代2024年度报告.pdf | 2070073 | 1.97 |
| evidence/english/v001/sources/6850b3d22ec2427c__宁德时代2025年度报告.pdf | 2051998 | 1.96 |

## File types

(no extension): 1, .html: 7, .jpg: 1, .json: 10, .jsonl: 1, .md: 13, .pdf: 14, .png: 56, .py: 3, .txt: 55.

## Included and excluded material

Included: portable README/startup instructions and agent boundary; unchanged English master prompt, method, task configuration, formal input list and contract; two actual workflow scripts; full curated facts/manifest/notes and all required source assets; standard-library package verifier; one isolated report example with source mapping and references; rights/security notes and portable validation summaries.

Excluded: historical reports and draft collections, sealed-run copies, historical ratings/judgment records, preparation quarantine, fixed-prose write/revise exporters, caches, account settings, credentials, unrelated documents, temporary files, and generated test outputs. The original final Word/PDF report and original sealed runs remain untouched outside this package. The single example is intentional and labelled.

workflow/en/README_EN.md and START_NEW_SESSION_EN.md were made portable in the package copy. Core research scripts/instructions/configuration and all evidence bytes remain unchanged. Original acquisition paths retained in source metadata are provenance, not extra runtime dependencies. Every active source_file/text_file/screenshot locator resolves within this package. Archived HTML dependencies are not rendered or needed by the local evidence-record workflow.

## Checks actually performed

| Check | Result |
|---|---|
| Required instruction, config and formal input paths | Passed from new package root |
| Script AST compilation and actual import of deterministic companion | Passed without cache writes; standard-library imports only |
| Fact IDs/count, facts hash and package-notes hash | Passed: 207 unique records |
| Source-asset SHA-256 | Passed: all 134 assets |
| Active source file, text and screenshot references | Passed: 355 references |
| Deterministic arithmetic recomputation | Passed: 19 calculation records |
| Example claim/source membership and citations | Passed: 31 claims |
| Fresh preparation smoke ID | package_smoke_20261026_01; passed |
| Snapshot hashes, no historical inputs and recalculations | Passed |
| show command | Passed for IND-2025 |
| validate before model outputs | Expected refusal, exit 2: five required outputs missing |
| finalize before model outputs | Expected refusal, exit 2; no seal created |
| Final test state | AWAITING_MODEL; no model report generated |
| Final read-only package verification | Passed |
| Original sealed run and final-report hashes | Verified unchanged |
| Credential/private-path scan | No matched credentials or private paths in scanned text/PDF metadata |

Validation records are in verification/. Preparation-only test snapshots and local command/runtime records were retained outside the proposed upload folder, in the sibling FIN409_Agent_Submission_validation directory. They are not part of the ZIP. No fresh live-model analysis was performed during packaging. Passing these checks is not a semantic review or successful full analytical run.

## Security, rights and remaining issues

No account settings, personal student details or requester credentials were intentionally copied. Text and PDF metadata were scanned for key/token patterns, quoted credential assignments and private machine paths. Public publisher email contacts and third-party author/signatory information remain source material. Image text and complete PDF bodies were not exhaustively OCR/privacy-audited, so absence of all possible personal data is not guaranteed. See verification/security_review.json for scope.

No open-source licence was assigned to third-party material. Confirm redistribution rights and appropriate repository access before any future upload. No required asset was dropped to avoid rights or size concerns. If an exact source must be transferred separately, use its manifest path from the original curated library and verify its SHA-256; a fresh download may differ. Source URLs are finding aids, not a guarantee of byte-identical recovery.

The research requires a live Codex/model session; the package does not provide a hosted agent or repository URL. Model service availability is separate from Python. A subsequent model session must form fresh analysis without reading examples or reusing example conclusions. Original source limitations and unknown metadata remain. No licence, source permission or independent analytical validation has been inferred from passing the packaging tests.

## Browser-upload practicality

GitHub currently allows browser uploads of at most 25 MiB per file and up to 100 files at a time: [GitHub Docs — Adding a file](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository), checked 26 October 2026.

The largest file is 9.62 MiB, below the per-file browser limit. With 161 files, browser upload of the extracted package is technically practical in at least 2 batches, preserving relative paths. A folder upload must be split deliberately; do not assume one selection exceeding 100 files will succeed. The complete ZIP is for transfer/extraction and exceeds the browser single-file limit; uploading a ZIP would also not unpack it into a runnable repository. GitHub Desktop or Git is less error-prone for this many paths, but no repository was initialised and nothing was uploaded. No individual file requires Git LFS on size grounds. Rights/privacy review remains separate from technical upload practicality.
