"""Single-conversation demo with one clarification state and canned responses."""
from intent_classifier import classify

conversation_state = None

RESPONSES = {
    "Billing": "I can help you with your billing enquiry.",
    "App_Login": "Are you having trouble logging into the service app?",
    "Duplicate_Email": "Is your email linked to another account?",
    "Online_Order": "Do you need help with an online order?",
    "Network_Issue": "Are you experiencing mobile network issues?",
}


def chat(message):
    global conversation_state
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    answer = message.lower().strip()

    restart_commands = ["cancel", "restart", "start over"]
    restart_phrases = [
        "can we start over", "can i start over", "i want to start over",
        "let's start over", "please restart", "restart the conversation",
    ]
    if answer in restart_commands or any(phrase in answer for phrase in restart_phrases):
        conversation_state = None
        return "Conversation reset. How can I help you?"

    intent = classify(message)
    if conversation_state == "waiting_for_charge_choice":
        # Use the same classifier for every supported topic, including billing.
        if intent in RESPONSES:
            conversation_state = None
            return RESPONSES[intent]
        if answer == "1":
            conversation_state = None
            return RESPONSES["Billing"]
        phone_terms = ["phone", "charging", "charger", "won't charge", "not charging"]
        if answer == "2" or any(term in answer for term in phone_terms):
            conversation_state = None
            return "Let's troubleshoot your phone charging issue."
        return "Please choose Billing (1) or Phone Charging (2)."

    if intent == "Clarification":
        conversation_state = "waiting_for_charge_choice"
        return "Is this about Billing (1) or Phone Charging (2)?"
    return RESPONSES.get(intent, "Could you please provide more details?")
