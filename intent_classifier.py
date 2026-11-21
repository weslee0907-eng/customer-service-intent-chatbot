"""Personal learning portfolio: rule-based intent classifier and known-case QA evaluation.
Run: python intent_classifier.py
Uses only the Python standard library. All examples are fictional.
"""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent


def classify(message):
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    text = message.lower().strip()

    # Step 1: Handle phone charging and ambiguous enquiries
    device_charging_terms = [
        "phone won't charge",
        "phone is not charging",
        "can't charge my phone",
        "charge my phone",
        "phone charger"
    ]

    if any(term in text for term in device_charging_terms):
        return "Fallback"

    if any(term in text for term in ["charge issue", "charging issue"]):
        return "Clarification"

    # Step 2: Duplicate email
    if any(term in text for term in [
        "already linked", "already registered",
        "email in use", "email is used",
        "same email", "duplicate email",
        "using my email address",
        "accounts under one email",
        "email attached to an old service",
        "email is in use",
        "email already associated",
        "email conflict",
        "separate accounts using one email",
        "email is associated with",
        "linked to my other email",
        "email is already attached"
    ]):
        return "Duplicate_Email"

    # Step 3: App login
    if any(term in text for term in [
        "log in", "login", "sign in",
        "password", "credentials",
        "access my account", "access the app",
        "get into my account",
        "signs me out", "locked out of the app",
        "account is locked",
        "profile keeps getting locked",
        "sign-in screen",
        "logging me out",
        "access to my profile"
    ]):
        return "App_Login"
    # Step 4: Online order
    if any(term in text for term in [
        "order", "checkout", "delivery",
        "purchase online",
        "complete my purchase",
        "haven't received my new handset"
    ]):
        return "Online_Order"

    # Step 5: Billing
    if any(term in text for term in [
        "bill", "charged", "invoice",
        "payment", "direct debit",
        "payment question",
        "balance is unchanged",
        "understanding charges",
        "amount owing",
        "monthly charge",
        "owe more",
        "extra fees",
        "unexpected fee"
    ]):
        return "Billing"

    # Step 6: Network issue
    if any(term in text for term in [
        "internet", "network", "signal",
        "coverage", "mobile data",
        "wi-fi", "wifi", "connection",
        "reception", "cellular data",
        "calls keep dropping"
    ]):
        return "Network_Issue"

    return "Fallback"


def evaluate(input_path, output_path):
    with open(input_path, newline='', encoding='utf-8-sig') as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("The input CSV must contain at least one test case.")
    required = {"id", "message", "expected_intent"}
    if not required.issubset(rows[0]):
        raise ValueError("The input CSV requires id, message and expected_intent columns.")
    results = []
    for index, row in enumerate(rows, start=2):
        if None in row or any(row.get(name) is None or not row[name].strip() for name in required):
            raise ValueError(f"CSV row {index} must have nonempty id, message and expected_intent fields and no extra cells.")
        predicted = classify(row['message'])
        results.append({**row, 'predicted_intent': predicted,
                        'correct': int(predicted == row['expected_intent'])})
    with open(output_path, 'w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    total = len(results)
    correct = sum(row['correct'] for row in results)
    print(f'Test accuracy: {correct}/{total} = {correct/total:.1%}')
    print('Errors:')
    for row in results:
        if not row['correct']:
            print(f"  {row['id']}: expected={row['expected_intent']}, predicted={row['predicted_intent']} | {row['message']}")
    print(f'QA results saved to {output_path}')
    return results


if __name__ == '__main__':
    results = evaluate(BASE / 'test_cases.csv', BASE / 'qa_results.csv')
    raise SystemExit(0 if all(row['correct'] for row in results) else 1)
