# Edge Case QA Summary

## Objective
Evaluate how the rule-based chatbot handles complex customer messages.

## Test Results
1. Phone charging with billing negation
   Predicted: Fallback
   Finding: Device charging is outside the classifier categories; Fallback is consistent with the current design but does not resolve the customer's problem. Charging guidance is available only after clarification.

2. Network negation with forgotten password
   Predicted: App_Login
   Finding: Correctly identified the login issue.

3. Multiple intents: login and network
   Predicted: App_Login
   Finding: Detected only one of two customer issues.

4. Billing negation with online order
   Predicted: Online_Order
   Finding: Correctly identified the order issue.

## Key Findings
- All four edge cases executed without runtime errors.
- Two cases produced the desired primary intent.
- Negation and multiple intents remain limitations.

## Future Improvements
- Improve negation handling.
- Support multiple intents in one message.
- Expand testing with unseen customer messages.

## Additional Exploratory Testing

Historical author-reported testing: after keyword improvements, five new
customer messages were tested manually. The descriptions below are summaries,
not a reproducible dataset of five verbatim inputs.

Results:
- Phone charging problem: Fallback
- Change email address: Fallback
- Broken handset screen: Fallback
- Cannot make calls at home: Fallback
- Buy a new phone: Fallback

Four results were considered reasonable for the current
supported intent categories.

One potential false negative was identified:
"I cannot make calls at home" was classified as Fallback,
although it may indicate a network issue.

This demonstrates a limitation of keyword-based
classification when customers use unfamiliar wording.

## Final review verification (2026-11-22, Australia/Brisbane)

All four exact edge-case messages in the notebook were rerun, with the outcomes above. The exact documented exploratory message `I cannot make calls at home` was also rerun and still returns Fallback. It remains an acknowledged potential false negative, outside the original 106-case score. No keyword was added specifically to eliminate this demonstration of the current limitation. The other four historical exploratory messages cannot be reproduced exactly from their summaries.
