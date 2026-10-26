# FIN409 English research agent

This package supports a fresh model-led analysis of China's broad automotive traction-battery industry in 2023–2025, with CATL as the focal company and Porter's Five Forces as the sole framework. It includes captive and external automotive supply across battery chemistries; stationary storage and starter-only batteries are outside the target industry.

The agent is a live Codex/model session following the supplied research instructions. Python is its deterministic companion. **No Python command alone generates the model analysis, ratings or report.**

## Prerequisites

- Python 3.10 or later; the package check used Python 3.12. The research CLI and package verifier use only the standard library. No pip installation, API key, paid API or model SDK is required by the scripts.
- An active Codex or equivalent model session with permission to read this folder, write new local run outputs and execute Python. Model access is separate from Python and subject to the user's service/account arrangements.
- Keep this package's directory structure and UTF-8 filenames intact. Run commands from the package root, where this README is located. Preserve the Chinese source filenames.

On macOS/Linux use `python3`; on Windows use `py -3`, or a configured `python` command pointing to the intended Python version. Do not use Python's `-O` option: the supplied workflow uses assertions for integrity checks. Word/PDF production dependencies are not needed to run the research workflow; this package exports Markdown/JSON/CSV rather than formatted Word/PDF files.

## Open a fresh model session

Extract this folder and open **FIN409_Agent_Submission itself** as the workspace. Do not open a parent folder containing other historical research. Give the model local file and command access. Its first inputs are `AGENTS.md`, `workflow/en/START_NEW_SESSION_EN.md`, the English master prompt, task configuration, method, README and formal input list.

Paste this exact startup instruction as the session's user message:

> Execute one fresh FIN409 English analysis using workflow/en/MASTER_PROMPT_EN.md, workflow/en/task_en.json and workflow/en/INPUT_FILES_EN.json. Choose an unused run ID. Use only the curated evidence package and the new run snapshot; Python performs deterministic preparation, calculations and checks, while you form fresh evidence-based mechanisms, counterweights, force ratings, confidence and separate industry-attractiveness and CATL-position judgments in this session. Do not read examples/, previous runs, historical reports, ratings, judgments, analysis records or preparation quarantine files as formal inputs or target answers. Write the five required outputs directly into the new run's outputs directory. Keep the English body at 2,200–2,400 words, never above 2,500; keep the five forces together at or below 2,000 and introduction/conclusion each at 200–250 words. Preserve traceable claims, original units, source locators and section word counts. Place methods, the actual prompt and tool details in appendices. This is reused curated evidence, not fresh retrieval or comprehensive PDF extraction. Validate, correct actual errors and finalise only after all requirements pass. Do not publish, upload or deploy anything.

The example is for a human reader reviewing output structure. Its conclusions are not prescribed outcomes. Close it before starting a fresh analysis; neither scripts nor formal input lists load it.

## Python operations and model handoff

First check the packaged inputs without making a research run:

```text
python3 verify_package.py
```

Use an unused run ID in place of `NEW_RUN_ID` in every command below. `prepare` refuses to overwrite an existing directory.

```text
python3 workflow/en/run_en.py prepare --config workflow/en/task_en.json --run-id NEW_RUN_ID
```

Expected state: **AWAITING_MODEL**. This establishes a snapshot and calculations only. The model must inspect `runs_en/NEW_RUN_ID/inputs/`, `calculations.json` and `evidence_digest.md`, then use actual IDs from the digest, for example:

```text
python3 workflow/en/run_en.py show --run-id NEW_RUN_ID --ids IND-2023 IND-2024 IND-2025
```

Continue inspecting relevant complete evidence records, including counterevidence, before forming fresh judgments. The master prompt specifies the required analytical work and schema. The model writes these files using ordinary file tools:

```text
runs_en/NEW_RUN_ID/outputs/analysis.json
runs_en/NEW_RUN_ID/outputs/claims.json
runs_en/NEW_RUN_ID/outputs/report_en.md
runs_en/NEW_RUN_ID/outputs/semantic_review.json
runs_en/NEW_RUN_ID/outputs/appendices_en.md
```

After that model-authored work exists:

```text
python3 workflow/en/run_en.py validate --run-id NEW_RUN_ID
python3 workflow/en/run_en.py finalize --run-id NEW_RUN_ID
```

Do not finalise before resolving failures. `finalize` also enforces all configured length targets and seals the outputs. Later changes require a new run ID. Missing model outputs are an expected validation failure immediately after preparation; do not fill them by replaying the example. The CLI has no model API or report-writing exporter.

## Expected records and responsibilities

Preparation produces input/runtime manifests, a fact snapshot, source manifest, arithmetic, evidence digest, event log and state file. Successful validation additionally produces `claim_source_map.json`, `claim_source_map.csv`, `word_counts.json`, `word_counts.md` and `validation.json`. Finalisation adds a sealed output manifest and FINALIZED state.

Mechanical checks cover hashes, schemas, references, declared original measurements, arithmetic, English-body structure and the configured counter. That counter includes section headings but excludes claim tags, Markdown syntax and link destinations; other software may count differently. Mechanical success does not establish causal correctness, independent review or that the model performed every reasoning step. The model's semantic self-review is separate and is not independent validation.

## Package boundaries and limitations

All 207 curated evidence records and all 134 manifest-listed source assets are included unchanged. No required source asset was omitted. Source locators use package-relative paths; original_paths/original_source_file fields are provenance labels pointing to historical acquisition locations, not additional runtime dependencies. Archived HTML subresources and original upstream working directories are not needed by this local fact/locator workflow. Source URLs are retained for attribution but are not automatically downloaded or freshly verified.

This package reuses curated local evidence. Its preparation does not repeat comprehensive retrieval or PDF extraction. Missing dates, scope differences, approximate values, original source assessments, country-versus-vendor concentration and unmeasured causal effects remain limitations. See the method, source records and source-specific qualifications. No force rating is preselected, and the example is not a correctness oracle.

No account settings, user credentials, caches, historical drafts, old fixed-prose exporters or unrelated documents are included. Verification records describe the actual preparation-only packaging test; it is **not a fresh model analysis**. Generated runs are ignored by Git and are not part of the upload payload. `verify_package.py` accepts future generated runs without treating them as formal packaged inputs.

Third-party reports and source material retain their original rights. No open-source licence is assigned by this package. Read `THIRD_PARTY_NOTICES.md` before any future redistribution. Package preparation does not create a remote repository, publish files or supply an agent-access URL. See `package_inventory.md` for measured sizes, checks, remaining issues and upload practicality.
