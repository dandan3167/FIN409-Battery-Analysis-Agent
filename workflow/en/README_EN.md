# Portable English workflow entry point

Open the package root and follow ../../README.md, START_NEW_SESSION_EN.md, MASTER_PROMPT_EN.md, METHOD_EN.md, task_en.json, INPUT_FILES_EN.json and output_contract_en.json. The master prompt, method, configuration, contract, deterministic scripts and evidence are unchanged copies; only this launch documentation and the startup page were made portable for this package.

Use Python 3.10+ without optimisation (-O). No external Python packages are required. The original run was checked on Python 3.12. On Windows replace python3 with py -3 where available. From the package root:

```text
python3 workflow/en/run_en.py prepare --config workflow/en/task_en.json --run-id NEW_RUN_ID
python3 workflow/en/run_en.py show --run-id NEW_RUN_ID --ids IND-2023 IND-2024 IND-2025
```

Choose a unique ID. AWAITING_MODEL means deterministic preparation only. Read the snapshot, digest and calculations; inspect complete records in sensible batches, including counterevidence. The model must then form fresh judgments and write all five required outputs following the master prompt. Do not read examples as formal inputs.

Only after model-authored outputs exist:

```text
python3 workflow/en/run_en.py validate --run-id NEW_RUN_ID
python3 workflow/en/run_en.py finalize --run-id NEW_RUN_ID
```

Validation checks facts, source integrity, output schema, active claims, declared measurements, arithmetic, English-body structure and word counts. Finalisation requires all configured targets and seals outputs. Neither step executes a model. Model self-review is not independent validation. Preparation reuses 207 curated records and 134 source assets; it does not repeat retrieval or comprehensive PDF extraction.

Body target: 2,200–2,400 words; absolute maximum: 2,500; five forces together: at most 2,000; introduction and conclusion: 200–250 each. Use the exact markers and counter convention from the prompt. Keep methods, actual prompts, tools and source details in appendices.

Evidence and source hashes must remain unchanged. The package's top-level verification records are packaging checks, not a completed new research run. Preserve sealed outputs and choose new run IDs for subsequent revisions.
