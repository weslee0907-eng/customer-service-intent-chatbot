"""Additional engineering checks; separate from the original 106 QA cases."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
import chatbot
from intent_classifier import classify, evaluate


class ReviewTests(unittest.TestCase):
    def setUp(self):
        chatbot.conversation_state = None

    def tearDown(self):
        chatbot.conversation_state = None

    def test_billing_paraphrases_resolve_clarification(self):
        for message in ["My payment failed", "My direct debit failed", "There is an unexpected fee"]:
            with self.subTest(message=message):
                chatbot.chat("I have a charge issue")
                self.assertEqual(chatbot.chat(message), "I can help you with your billing enquiry.")
                self.assertIsNone(chatbot.conversation_state)

    def test_other_supported_topic_switches(self):
        for message, response in [
            ("My email is already linked", "Is your email linked to another account?"),
            ("Where is my online order?", "Do you need help with an online order?"),
        ]:
            with self.subTest(message=message):
                chatbot.chat("I have a charge issue")
                self.assertEqual(chatbot.chat(message), response)
                self.assertIsNone(chatbot.conversation_state)

    def test_numbered_billing_and_reset_commands(self):
        chatbot.chat("I have a charge issue")
        self.assertEqual(chatbot.chat("1"), "I can help you with your billing enquiry.")
        self.assertIsNone(chatbot.conversation_state)
        for command in ["cancel", "restart", "start over"]:
            chatbot.chat("I have a charge issue")
            self.assertEqual(chatbot.chat(command), "Conversation reset. How can I help you?")
            self.assertIsNone(chatbot.conversation_state)

    def test_non_string_inputs(self):
        for function in [classify, chatbot.chat]:
            for message in [None, 123, [], {}]:
                with self.subTest(function=function.__name__, message=message):
                    with self.assertRaisesRegex(TypeError, "message must be a string"):
                        function(message)

    def test_empty_input_preserves_waiting_state(self):
        self.assertEqual(classify("  "), "Fallback")
        self.assertEqual(chatbot.chat(""), "Could you please provide more details?")
        chatbot.chat("I have a charge issue")
        self.assertEqual(chatbot.chat(""), "Please choose Billing (1) or Phone Charging (2).")
        self.assertEqual(chatbot.conversation_state, "waiting_for_charge_choice")

    def test_malformed_csv(self):
        cases = ["", "id,message,expected_intent\n", "id,text,label\nx,hello,Fallback\n",
                 "id,message,expected_intent\nx,hello\n", "id,message,expected_intent\nx,,Fallback\n",
                 "id,message,expected_intent\nx,hello,Fallback,extra\n"]
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            output = Path(directory) / "output.csv"
            for text in cases:
                with self.subTest(text=text):
                    source.write_text(text, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        evaluate(source, output)

    def test_failures_are_reported(self):
        # A temporary deliberately wrong label verifies the evaluator, not the model.
        # Original dataset files and labels are never edited.
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            output = Path(directory) / "output.csv"
            source.write_text("id,message,expected_intent\nx,My internet is down,Billing\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()) as captured:
                rows = evaluate(source, output)
            self.assertEqual(rows[0]["correct"], 0)
            self.assertIn("expected=Billing, predicted=Network_Issue", captured.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
