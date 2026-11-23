# Project Review

**Last reviewed:** 22 November 2026  
**Environment:** Python 3.13.17, Windows

## Overview

Before publishing this project on GitHub, I completed a final review to make sure the code, test results and documentation were consistent.

I checked the Python scripts, Jupyter notebook, CSV datasets, README, dashboard and other project files. I also reviewed the content for unnecessary company references and sensitive information.

The project uses fictional customer enquiries and is intended for learning and demonstration.

## Changes Made

During the final review, I made a few improvements:

- **Conversation handling:** Fixed an issue where the chatbot could miss a topic change while waiting for a billing or charging clarification.
- **Error handling:** Improved how the classifier handles invalid inputs and incorrectly formatted CSV files.
- **Testing:** Updated the scripts so they report failures properly instead of always returning a successful exit code.
- **Code cleanup:** Improved indentation and readability while keeping the existing keyword rules and classification order.
- **Documentation:** Updated the README, test results and QA dashboard to reflect the current project.

I also added seven engineering checks in `test_review.py` to cover conversation behaviour, input validation and error handling.

The original test cases and expected answers were not changed.

## Test Results

I ran the project using Python 3.13.17 on Windows.

| Test | Result |
|---|---|
| Intent classifier | 60/60 passed |
| Conversation tests | 9/9 passed |
| Full QA suite | 106/106 passed |
| Additional engineering checks | 7/7 passed |
| Notebook code cells | 6/6 executed successfully |

All four Python test commands completed with exit code `0`.

I also checked that the test scripts correctly report failures when incorrect predictions are introduced in a temporary copy of the project.

The QA dashboard and result CSV files were regenerated after the final review.

The full command results are saved in `execution_results.json`.

## Notebook Review

I checked the notebook to make sure it uses the current Python scripts and project files.

All six code cells ran in order without errors in a fresh Python process.

The notebook no longer contains old Google Colab paths, duplicate classifier implementations or unnecessary saved outputs.

I did not test it through the full Jupyter or Google Colab interface, so that part remains unverified.

## Privacy Check

I reviewed the project for company-specific information, real customer details, passwords, API keys and other sensitive content.

I did not find any sensitive information in the reviewed files.

The project uses simulated customer messages and does not connect to company systems or external services.

I also removed unnecessary Python cache files from the final release.

This check covers the project files provided for review; it does not independently verify how every example was originally created.

## Known Limitations

Although all 106 predefined tests pass, these examples were already used during development. The result does not mean the chatbot will achieve 100% accuracy with new customer messages.

For example, the message:

`I cannot make calls at home`

still returns `Fallback`, even though it could be related to a network issue.

Other limitations include:

- The chatbot relies on keyword matching rather than understanding the full meaning of a message.
- It may struggle with unfamiliar wording, negative statements or multiple questions.
- It supports one demonstration conversation at a time.
- Its responses are predefined and cannot access real customer accounts or resolve service issues.

This is a rule-based Python project, not a machine learning model or an LLM.

## Final Status

The final project was checked, repackaged and tested again after extraction.

The ZIP file passed its integrity check, and the required project files were present. Temporary Python cache files were excluded.

**The project is ready to publish on GitHub as a personal learning portfolio.**

There is still room to improve how the chatbot handles unfamiliar customer messages, which would be a useful next step if I continue developing it.
