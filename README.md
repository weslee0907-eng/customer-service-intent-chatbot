# Customer Service Intent Classifier & Chatbot

## About this project
This is a personal learning portfolio independently assembled by the author, with ChatGPT assistance for learning Python, developing code, debugging and improving documentation. It demonstrates a simple rule-based chatbot using simulated customer messages. It is not an employer product, an official service, or a production system. No real customer data or internal company material is intended or required.

## What it demonstrates
- Intent classification: App_Login, Duplicate_Email, Online_Order, Billing, Network_Issue, Fallback and Clarification.
- Multi-turn clarification for ambiguous charge enquiries, with billing or device-charging choices.
- Topic switching, cancel and restart commands.
- Automated classification QA and conversation response/state checks.
- Reproducible CSV results and an SVG dashboard.

## Run locally
Python 3.10 or newer is recommended; this revision was checked with Python 3.13.17. The scripts use only the Python standard library. Extract the complete project and open a terminal in this folder:

```bash
python intent_classifier.py
python test_chatbot.py
python run_qa.py
```

`run_qa.py` evaluates all four classification datasets, runs conversation QA, and regenerates the result CSVs and dashboard. The final review independently reproduced 106/106 passing predefined tests. These are regression examples already seen during development, not a held-out evaluation. The script returns exit code 0 when all tests pass and a nonzero exit code if any test fails.

For separate engineering regression checks:

```bash
python test_review.py
```

These seven unittest methods cover billing clarification, remaining topic switches, reset commands, input validation, malformed CSVs and failure reporting. They are separate from the original 106 cases and are not included in the dashboard denominator. All seven passed in the final review. See `execution_results.json` for captured command results.

For a quick interaction:

```python
import chatbot
print(chatbot.chat("I have a charge issue"))
print(chatbot.chat("2"))
print(chatbot.chat("cancel"))
```

To use the notebook, install Jupyter separately (`python -m pip install notebook`) and open `Customer_Service_Chatbot_Development.ipynb` from the project directory. In Colab, upload the Python and CSV files to the notebook's current directory first. The notebook needs no pandas or plotting packages. During final review, all six code cells ran sequentially in a fresh Python process. Jupyter/Colab UI and kernel integration were not tested because Jupyter was not installed. Its code cells import the same modules as the scripts; they do not rewrite source files or mount cloud drives.

## QA Results and Improvements

Final review: 2026-11-22 (Australia/Brisbane), Python 3.13.17 on Windows. The current 106/106 result was independently rerun. The historical Before Improvements figures below are author-reported; the earlier implementation was not supplied and those figures were not independently reproduced.

| Test Suite | Before Improvements | After Improvements |
|---|---:|---:|
| Known classification cases | 60/60 | 60/60 |
| Development examples | 2/7 | 7/7 |
| Validation examples | 9/12 | 12/12 |
| Additional examples | 11/18 | 18/18 |
| Conversation QA | 9/9 | 9/9 |
| **Total** | **91/106** | **106/106** |

### Improvement Process

I reviewed the failed classification cases and expanded the keyword rules to recognise more natural customer expressions relating to app login, duplicate email, online orders, billing and network issues.

The expected test labels were not changed.

### Exploratory Testing

The author previously reported manually testing five additional messages. The final review reproduced the documented example `I cannot make calls at home`: it still returns Fallback, although it may indicate a network issue. The other four original verbatim messages were not supplied, so that historical manual test was not independently reproduced.

### Important Limitations

The 100% pass rate applies only to predefined tests, including cases used to improve the classifier. It does not represent accuracy on unseen customer messages or real-world performance.

The chatbot remains rule-based and may struggle with unfamiliar wording, negation, multiple intents and context-dependent enquiries.

![QA dashboard](qa_dashboard.svg)

## Files
| File | Purpose |
| --- | --- |
| `intent_classifier.py` | Ordered keyword rules and CSV evaluation |
| `chatbot.py` | Predefined responses and one conversation state |
| `test_chatbot.py` | Nine original conversation scenarios; CSV export |
| `test_review.py` | Seven additional engineering regression checks |
| `execution_results.json` | Captured final command and notebook execution results |
| `run_qa.py` | All classification datasets, conversation QA and dashboard |
| `test_cases.csv` | Original 60 classification examples |
| `development_cases.csv`, `validation_cases.csv`, `additional_cases.csv` | Original notebook examples recovered with their labels |
| `*_results.csv` | Regenerated predictions and pass/fail results |
| `Customer_Service_Chatbot_Development.ipynb` | Clean sequential walkthrough; saved without outputs |
| `edge_case_summary.md` | Observations on negation, charging and multiple intents |
| `REVIEW_REPORT.md` | Review scope, changes, privacy findings and validation limits |

## Design and limitations
The classifier lowercases input and checks keyword groups in order. The first match determines one intent. The chatbot stores whether it is waiting for a billing/charging choice and clears that state when a supported topic switch or reset occurs.

This is not machine learning or an LLM. It does not parse negation, understand every paraphrase, return multiple intents or solve customer account issues. Substring rules can produce false matches. Direct phone-charging questions return Fallback because device support is outside the classifier categories; charging guidance is a placeholder available through clarification. The global conversation state supports one demo conversation per Python process, not simultaneous users. English string input is expected; non-string input raises a clear TypeError. Empty input returns Fallback or repeats the pending clarification prompt. The classifier priority is: device charging, ambiguous charging, duplicate email, login, online order, billing, network, then Fallback. Do not enter real customer details.

Future work could use new independently authored evaluation cases, per-session state and a comparison with a simple machine-learning baseline. Measure improvements on separate data rather than repeatedly tuning to the same examples.
