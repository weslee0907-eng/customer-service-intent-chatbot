"""Nine original conversation regression scenarios; CSV output and failure exit code."""
import csv
from pathlib import Path
import chatbot

conversation_tests = [{'name': 'Network topic switch',
  'messages': ['I have a charge issue', 'My internet is not working'],
  'expected': 'Are you experiencing mobile network issues?',
  'expected_state': None},
 {'name': 'App login topic switch',
  'messages': ['I have a charge issue', 'I forgot my password'],
  'expected': 'Are you having trouble logging into the service app?',
  'expected_state': None},
 {'name': 'Normal billing clarification',
  'messages': ['I have a charge issue', 'Billing'],
  'expected': 'I can help you with your billing enquiry.',
  'expected_state': None},
 {'name': 'Invalid clarification answer',
  'messages': ['I have a charge issue', "I don't know"],
  'expected': 'Please choose Billing (1) or Phone Charging (2).',
  'expected_state': 'waiting_for_charge_choice'},
 {'name': 'Cancel conversation',
  'messages': ['I have a charge issue', 'cancel'],
  'expected': 'Conversation reset. How can I help you?',
  'expected_state': None},
 {'name': 'Phone charging clarification',
  'messages': ['I have a charge issue', '2'],
  'expected': "Let's troubleshoot your phone charging issue.",
  'expected_state': None},
 {'name': 'Natural language billing clarification',
  'messages': ['I have a charge issue', "I think it's about my bill"],
  'expected': 'I can help you with your billing enquiry.',
  'expected_state': None},
 {'name': 'Natural language phone charging',
  'messages': ['I have a charge issue', "Actually, my phone won't charge"],
  'expected': "Let's troubleshoot your phone charging issue.",
  'expected_state': None},
 {'name': 'Natural language restart',
  'messages': ['I have a charge issue', 'Can we start over please?'],
  'expected': 'Conversation reset. How can I help you?',
  'expected_state': None}]


def run_tests(output_path=None):
    rows = []
    for test in conversation_tests:
        chatbot.conversation_state = None
        for message in test["messages"]:
            actual = chatbot.chat(message)
        passed = (actual == test["expected"] and
                  chatbot.conversation_state == test["expected_state"])
        rows.append({
            "Test_Name": test["name"],
            "Expected_Response": test["expected"],
            "Actual_Response": actual,
            "Expected_State": str(test["expected_state"]),
            "Actual_State": str(chatbot.conversation_state),
            "Result": "PASS" if passed else "FAIL",
        })
        print(rows[-1]["Result"], test["name"])
    chatbot.conversation_state = None
    if output_path is None:
        output_path = Path(__file__).resolve().parent / "conversation_qa_results.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Conversation QA: {sum(r['Result'] == 'PASS' for r in rows)}/{len(rows)} passed")
    return rows


if __name__ == "__main__":
    results = run_tests()
    raise SystemExit(0 if all(r["Result"] == "PASS" for r in results) else 1)
