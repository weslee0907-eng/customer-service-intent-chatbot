# GitHub Pre-publication Final Review

Reviewed: 2026-11-22 (Australia/Brisbane). Runtime: Python 3.13.17, Windows.

## Input and scope

The supplied `Conversational_AI_Project.zip` was read and extracted successfully. ZIP CRC validation passed. The archive contained one project root, with all requested Python, notebook, CSV, Markdown, SVG and `.gitignore` files. No required project files were missing or duplicated in nested project folders. Compiled Python cache files were present and are excluded from the release archive because they are generated, unnecessary and can embed local paths.

Every delivered text file was read during review, including all four original Python files, the notebook's six code cells and six Markdown cells, all nine CSVs, all three Markdown documents, the SVG and `.gitignore`. Module imports and file references resolve with the documented project working directory. Scripts locate their datasets relative to their own file; the notebook explicitly requires the project working directory.

## Fixes

- Waiting for charge clarification previously recognised only a small billing vocabulary. Messages such as `My payment failed` could be left waiting even though the classifier recognised Billing. The chatbot now uses the same classifier and shared response mapping for all supported topic switches, avoiding duplicated responses.
- The standalone classifier command previously always exited successfully after evaluation, even if a prediction was wrong. It now returns exit code 1 on failed cases, matching the other QA commands.
- Non-string classifier/chat input now raises a clear TypeError. Empty chat input remains safe and preserves a pending clarification. Missing, blank or extra CSV cells now produce a descriptive ValueError.
- Tidied indentation without changing keyword rules or priority. Preserved the one-state conversation design and standard-library-only implementation.
- Regenerated all five result CSVs and the SVG. Added a dashboard total and refreshed the current review documentation. Kept historical improvement numbers explicitly identified as author-reported, since the earlier implementation is unavailable.
- Added seven separate engineering regression checks in `test_review.py`. They are not added to the 106-case dashboard denominator.

## Actual execution

| Command | Exit code | Result |
| --- | ---: | --- |
| `python intent_classifier.py` | 0 | 60/60 |
| `python test_chatbot.py` | 0 | 9/9 |
| `python run_qa.py` | 0 | 106/106 across all five groups |
| `python test_review.py` | 0 | 7/7 unittest methods, with parameterised subchecks |
| Notebook: six code cells sequentially in a fresh Python process | 0 | All executed without runtime errors |

| Predefined group | Before this review | After fixes |
| --- | ---: | ---: |
| Known classification | 60/60 | 60/60 |
| Development | 7/7 | 7/7 |
| Validation | 12/12 | 12/12 |
| Additional | 18/18 | 18/18 |
| Conversation QA | 9/9 | 9/9 |
| Total | 106/106 | 106/106 |

No exceptions or failures occurred in these normal runs. `execution_results.json` contains captured stdout, stderr and exit codes, with machine-specific project paths removed. Python was invoked using its installed executable because the default Windows `python` alias was broken in this environment.

Original classification dataset files and `test_chatbot.py` were compared byte-for-byte with the supplied ZIP and are unchanged. No expected label was changed and no failing original case was removed. Each input dataset has unique case IDs and no duplicate message rows within that dataset. Output CSV rows and dashboard counts were checked against the current inputs and predictions.

Failure detection was separately tested in a temporary project copy by forcing the classifier to predict Fallback. All three requested commands then returned exit code 1. Original labels were untouched, the temporary copy was discarded, and only normal regenerated results are delivered.

## Notebook validation boundary

All six code cells were executed from first to last in a fresh Python process and shared namespace, including module imports, examples, conversation checks and dashboard generation. The notebook imports the delivered code; it contains no classifier redefinitions, source-file overwrites, obsolete cloud paths, embedded customer data, old outputs or backup cells. Saved outputs and execution counts remain empty.

Jupyter, nbclient and ipykernel were not installed in this Python environment. A complete Jupyter kernel, browser session or Colab upload flow was therefore not tested. Sequential Python execution validates the cell code, not that integration.

## Privacy and publication findings

No unnecessary employer branding, internal project names, identifiable customer names, actual email addresses, phone/account numbers, customer records, internal business data, credentials, API keys, tokens, internal system addresses, private links or sensitive personal paths were found in the reviewed release text. `password` and `credentials` occur as generic intent keywords and simulated enquiry wording, not actual secrets. The public SVG XML namespace is a format identifier, not an external data dependency. No network or employer service is accessed by the code.

The compiled caches from the input archive were excluded rather than published. Privacy review is based on supplied content and cannot independently establish the original provenance of every simulated example. No unresolved item requiring a sensitivity decision was identified in the release text.

## Remaining limitations

**Known test pass rate is not real-world accuracy.** All named datasets, including the file called validation, were seen during development and keyword tuning; none is an independent held-out benchmark. The historical 91/106 before-improvement score was not reproduced because that earlier implementation was not supplied.

The exact documented exploratory message `I cannot make calls at home` was rerun and still predicts Fallback, a potential network false negative. The other four historical exploratory inputs were only summarised, so their exact manual runs could not be independently reproduced. All four exact notebook edge cases were rerun with the documented outcomes.

Substring rules can misread word fragments, negation, unfamiliar wording and messages with multiple intents. Device-charging patterns and ambiguous charging take priority; a mixed enquiry may therefore select Fallback or Clarification before other intents. The global conversation state supports one conversation per Python process. Responses are prompts or placeholders, not account actions or actual troubleshooting. This is a personal rule-based learning project, independently assembled with ChatGPT assistance, not an ML model, LLM or commercial product.

## Release packaging

The final archive contains one project folder, without Python caches, notebook checkpoints, virtual environments or Git metadata. A fresh extraction was used to rerun the QA suite and engineering checks. ZIP CRC and required file presence were verified before delivery.
