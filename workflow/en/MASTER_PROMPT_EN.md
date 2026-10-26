# FIN409: English acceptance run master prompt

You are the research model in the current Codex session. Python performs deterministic preparation and checking; you must analyse the active evidence at run time. Do not replay a previous report or call an exporter containing finished prose. Do not treat file generation as evidence that analysis has been performed correctly.

## Task and permitted inputs

Study China's broad vehicle traction-battery industry in **2023–2025**, focusing on **CATL**, using **Porter's Five Forces only**. Include automotive internal and external supply, across battery chemistries. Follow `workflow/en/task_en.json` and `workflow/en/METHOD_EN.md`. Do not use SWOT, PESTLE or another analytical framework.

This run uses a **previously curated local evidence library**. It is not a fresh comprehensive download or PDF-extraction exercise. Preserve and consult the packaged original Chinese sources, quotations, units, physical PDF pages (cover = page 1), URLs, dates, calculations and limitations. No paid API, deployment, repository publishing or network retrieval is authorised for this run.

Do not read historical Chinese/English reports, force ratings, judgment files, analysis records, closeout conclusions, historical comparisons, development archives, or preparation-only quarantine files. Do not seek a previous answer, translate an old draft, or require ratings to change or to reproduce history. The formal English evidence package contains no prescribed force outcomes. Original company or research-source assessments are attributed evidence, not the agent's established conclusion.

## Prepare and read

1. Read `workflow/en/README_EN.md`, the task configuration, this prompt, the method, the output contract and the formal input list. Use a fresh `run_id`. Execute with the interpreter in the README:

   `python workflow/en/run_en.py prepare --config workflow/en/task_en.json --run-id <new_run_id>`

   `AWAITING_MODEL` means preparation only. No report has been generated and no force has been analysed by Python.
2. Read the new run's `inputs/config.json`, `inputs/facts.jsonl`, `inputs/method.md`, `inputs/master_prompt.md`, `inputs/output_contract.json`, `inputs/source_manifest.json`, its `calculations.json` and `evidence_digest.md`. Use `show --run-id <id> --ids <IDs...>` to inspect complete records and log which facts were displayed. Work through numerical and qualitative evidence, including counterevidence. Packaged source files may be consulted for a specific scope or quotation question. Do not follow provenance into excluded historical analysis files.
3. Check period, publication date, geography, product/business scope, denominator, unit, numerical precision, source hierarchy and shared-source overlap. Distinguish disclosed facts, deterministic calculations, approximations, source assessments, missing values and non-comparable business segments. Flag unresolved uncertainty. Do not silently turn unknowns into zeros or source claims into proven causes.

## Live model analysis

4. Form a fresh structured analysis for RIV, BUY, SUP, ENT and SUB. For each, list observed facts and traceable sources, supporting mechanisms, counterweights, alternative explanations, limits, a Low/Medium/High rating, confidence and an explicit weighing explanation. No rating is preselected. Confidence is separate from intensity. Do not default to Medium when evidence is missing. A single confirmed case need not increase confidence in an industry-wide conclusion.
5. Review cross-force double counting and industry/company-level confusion. Treat established firms' expansion as rivalry; explain shared self-production facts without duplicating independent impacts. Battery-chemistry competition is internal. Assess industry attractiveness and CATL's position separately from mechanisms, not by averaging five ratings or equating a strong company with weak rivalry. Do not claim measured profit losses or pricing/cost leadership without support.
6. Write the following directly using ordinary file tools to `runs_en/<id>/outputs/`. Do not embed these answers in Python:
   - `analysis.json`: run ID, input digest, `reasoning_origin: "live_codex_session"`, `five_forces`, separate `industry_attractiveness`, `catl_position`, and `overlap_review`. Each force has `id`, `rating`, `confidence`, `support`, `counterweights`, `alternative_explanations`, `weighing`, and `limits`. Supporting/counterweight objects contain `evidence_ids` and `reason`.
   - `claims.json`: array of claims with unique C001-style IDs, `kind` (fact/calculation/inference/judgment/missing), `text`, active `evidence_ids`, `scope`, and `limitations`. Include `reported_metrics` entries (`evidence_id`, measurement `name`, exact original `value`) for key disclosed numbers. Calculation claims state inputs and formulas. Preserve approximations and nulls. Every key fact must map to original pages/URLs, not just to a historical analyst's paragraph.
   - `report_en.md`: a new analytical English report, not a translation of an earlier draft. Cite `[C001]` etc next to the supported claims.
   - `semantic_review.json`: `reviewer: "current_codex_session"`, `checks` (issue/result/explanation and relevant IDs), `remaining_limits`, and an explicit statement that same-model review is not independent validation. Review quotations, periods, scopes, numbers/accounting layers, alternative causes, duplicate effects, industry/company separation and English-only analytical prose. Resolve any `fail` before finalising.
   - `appendices_en.md`: methods, source/reference index and original-language evidence excerpts where necessary, actual prompt/configuration, tool responsibilities, input list, commands/events, calculations/comparability notes, missing evidence and remaining implementation limits. English explanations; original Chinese excerpts are permitted here if labelled. Do not move substantive force arguments into an appendix to evade the word limits.

## Report structure and word limits

All analytical report prose must be **English**. The report body target is **2,200–2,400 words**, with an absolute maximum of **2,500**. The five force sections combined must be **no more than 2,000 words**. The introduction and conclusion should each be **200–250 words**. Aim to satisfy all targets together; do not pad text or silently relax configuration.

Use exactly seven sections, in this order, with these HTML markers enclosing all counted text:

```text
<!-- REPORT_BODY_START -->
<!-- SECTION:INTRO:START -->
[Introduction]
<!-- SECTION:INTRO:END -->
<!-- SECTION:RIV:START -->
[Rivalry among existing competitors]
<!-- SECTION:RIV:END -->
<!-- SECTION:BUY:START -->
[Bargaining power of buyers]
<!-- SECTION:BUY:END -->
<!-- SECTION:SUP:START -->
[Bargaining power of suppliers]
<!-- SECTION:SUP:END -->
<!-- SECTION:ENT:START -->
[Threat of new entrants]
<!-- SECTION:ENT:END -->
<!-- SECTION:SUB:START -->
[Threat of substitutes]
<!-- SECTION:SUB:END -->
<!-- SECTION:CONCLUSION:START -->
[Conclusion]
<!-- SECTION:CONCLUSION:END -->
<!-- REPORT_BODY_END -->
```

The bracketed labels above are structure placeholders, not report prose. Put headings, tables and substantive footnotes inside their respective section markers. The introduction sets scope and the analytical question; the conclusion explains decisive industry-attractiveness trade-offs and CATL's distinct position. Include each force's CATL implications within its discussion rather than adding an uncounted extra body section.

Count all text within the seven sections, including headings and tables; exclude Markdown syntax, link destinations, claim tags and HTML markers. Hyphenated compounds and apostrophe contractions count as one word, and numerical expressions count as words. Bibliographic entries, methods, prompts and tool details belong outside the body, in appendices. The counter is an explicit project convention, not a promise of identical Microsoft Word counting. Retain each section's count, the force subtotal and body total in `word_counts.json` and `word_counts.md`.

## Check and seal

7. Execute `python workflow/en/run_en.py validate --run-id <id>`. The tool checks input/source integrity, output schema, active references, declared numerical values, deterministic calculations, English body screening, section structure and word counts. Target misses must be explained in the model's review; do not exceed the hard body/force limits or misstate an out-of-target report as meeting the target. Prefer revising to meet the target. Mechanical validation does not prove causal correctness or independent model execution.
8. Fix actual errors without modifying original sources. Execute `python workflow/en/run_en.py finalize --run-id <id>` only when checks pass. It requires the report to meet the body, introduction and conclusion targets as well as hard limits, then seals the outputs. Use a new run ID for later revisions. Do not run historical comparison commands or open historical ratings for this English acceptance.
9. Present the English acceptance outputs, section/total word counts, source mapping, actual model/Python execution steps and honest limitations. Report which inputs were actually inspected. Do not claim every PDF was re-extracted or that logs prove every internal reasoning step. A new session reduces earlier chat-context exposure but is not an independently validated blind experiment.

This preparation package does not contain an English report or any expected force grades. The new session must perform the analysis.
