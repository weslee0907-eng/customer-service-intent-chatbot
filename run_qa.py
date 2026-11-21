"""Run all preserved examples. Report failures honestly without changing labels."""
import csv
from pathlib import Path
from intent_classifier import evaluate
from test_chatbot import run_tests

DATASETS = {
    'Known cases': ('test_cases.csv', 'qa_results.csv'),
    'Development examples': ('development_cases.csv', 'development_results.csv'),
    'Validation examples': ('validation_cases.csv', 'validation_results.csv'),
    'Additional examples': ('additional_cases.csv', 'additional_results.csv'),
}


def write_dashboard(base):
    scores = []
    for label, (_, filename) in DATASETS.items():
        with (base / filename).open(encoding='utf-8', newline='') as handle:
            rows = list(csv.DictReader(handle))
        scores.append((label, sum(int(r['correct']) for r in rows), len(rows)))
    with (base / 'conversation_qa_results.csv').open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    scores.append(('Conversation QA', sum(r['Result'] == 'PASS' for r in rows), len(rows)))
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="850" height="390" viewBox="0 0 850 390">',
           '<rect width="850" height="390" fill="white"/>',
           '<g font-family="Arial, sans-serif" fill="#172b4d">',
           '<text x="25" y="35" font-size="23">Customer Service Chatbot - QA Results</text>',
           '<text x="25" y="65" font-size="14">Simulated, previously seen examples; not real-world accuracy</text>']
    for i, (label, passed, total) in enumerate(scores):
        y = 100 + i * 50
        percent = passed / total * 100
        svg.extend([
            f'<text x="25" y="{y+17}" font-size="15">{label}</text>',
            f'<rect x="220" y="{y}" width="400" height="25" fill="#edf0f5"/>',
            f'<rect x="220" y="{y}" width="{percent*4:.1f}" height="25" fill="#28789c"/>',
            f'<text x="635" y="{y+18}" font-size="15">{passed}/{total} ({percent:.1f}%)</text>',
        ])
    passed = sum(score[1] for score in scores)
    total = sum(score[2] for score in scores)
    svg.append(f'<text x="25" y="365" font-size="16">Total: {passed}/{total} predefined tests passed</text>')
    svg.append('</g></svg>')
    (base / 'qa_dashboard.svg').write_text('\n'.join(svg), encoding='utf-8')


def main():
    base = Path(__file__).resolve().parent
    all_correct = True
    for label, (input_name, output_name) in DATASETS.items():
        print('\n' + label)
        rows = evaluate(base / input_name, base / output_name)
        all_correct = all_correct and all(r['correct'] for r in rows)
    rows = run_tests(base / 'conversation_qa_results.csv')
    all_correct = all_correct and all(r['Result'] == 'PASS' for r in rows)
    write_dashboard(base)
    print('Overall QA:', 'PASS' if all_correct else 'FAIL')
    return 0 if all_correct else 1


if __name__ == '__main__':
    raise SystemExit(main())
