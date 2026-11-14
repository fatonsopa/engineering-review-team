# Repository instructions

This is a native instruction and engineering-knowledge package. Scripts serve setup and installation only. Keep shared authority in `references/review_policy.md`, evidence and findings in `references/review_standard.md`, and technical methods in the domain guides, policies and standards.

Do not add review state engines, registries, host matrices or mandatory per-criterion records without an explicit new user requirement. Use ordinary host tools and task messages. Keep role identifiers and `{{SKILL_ROOT}}` resource links consistent with the installer.

Preserve substantive technical controls, user overrides, conditional applicability and evidence limits when editing prose. Select applicable controls instead of requiring every standard or research file for each task. Keep CLAUDE.md importing AGENTS.md.

Validate changes proportionately: use the installer safety tests for setup changes, check affected links and native asset syntax, and inspect meaning for instruction changes. The small package check is `python3 -B -m unittest discover -s tests -p test_package.py -v`. Reuse passed unaffected checks. Do not invalidate evidence solely for bookkeeping hashes or automatically expand live model testing into a grid. A targeted host smoke is useful only for a changed host interaction; static parsing does not prove actual host behavior.

Preserve unrelated user changes. Publish or merge only within the user's existing authority; normal editing and testing do not grant publication permission.
