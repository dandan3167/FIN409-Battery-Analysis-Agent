# Packaging provenance

Prepared 26 October 2026 as a separate portable folder. The original project, sealed acceptance run, approved revision and final report were not modified. The original acceptance output hashes and final-report delivery hashes were checked after packaging preparation.

Unchanged formal files: English master prompt, method, task configuration, input list, output contract, run_en.py and deterministic.py. The full evidence facts/manifest/notes and all 134 manifest-listed source assets are byte-identical copies. No evidence was omitted, re-collected, re-extracted, rewritten or re-licensed.

Package-only documentation changes: workflow/en/README_EN.md and START_NEW_SESSION_EN.md replace local workspace/interpreter paths with portable launch instructions. The new root README and AGENTS.md define this English-only package and keep examples outside formal inputs. These documentation changes legitimately produce a different new-run input digest; they do not change the evidence or prescribe ratings. No obsolete exporter or Chinese historical workflow was copied.

The single isolated example is the final report's analytical Markdown plus the approved source mapping and reader references. The formatted final DOCX/PDF, supporting development material and sealed runs remain in the original project, outside this minimum research package. Example IDs and mappings are checked for consistency; the example must not be read as evidence during a fresh run.

The test used a new package-local run ID, package_smoke_20261026_01. It prepared a snapshot, exercised show, checked deterministic calculations and exercised missing-output guards in validate/finalize. It stopped at AWAITING_MODEL. Test snapshots and local runtime-executable metadata were moved outside the upload folder and retained separately for local audit. Only a portable summary is included in verification/package_validation.json. The absence of test logs in this upload folder is intentional; generated run records are not formal source inputs.

verify_package.py is a package-specific standard-library verifier, not an analytical model. It checks source locators, hashes, imports, arithmetic and the example mapping. Its optional --prepare-smoke mode creates a fresh run and exercises guards; it does not generate a model report. Use a new ID on every repeat.

package_manifest.json covers the delivery files other than itself and package_inventory.md, avoiding self-referential hashes. The inventory records whole-folder totals including both. Generated runs/caches are excluded from the upload payload and ZIP. No remote repository, Git metadata, account configuration, credentials or uploads were created.
