from tools import (
    get_customer_details,
    get_deals_by_status,
    get_deals_above_amount,
    get_old_deals,
    get_customer_history,
    add_note,
    assign_lead,
    update_deal_status
)


CUSTOMERS = [
    "Rahul",
    "Arun Kumar",
    "Meena Raj",
    "Sanjay Kumar",
    "Divya Shah"
]

SALESPEOPLE = [
    "Priya",
    "Arun",
    "Meena",
    "Sanjay",
    "Divya"
]


def move_deal(customer_name, new_status):
    data = get_customer_details(customer_name)

    if not data["success"]:
        return data["message"]

    deals = data["deals"]

    if len(deals) == 0:
        return f"No deals were found for {customer_name}."

    if len(deals) > 1:
        deal_list = "\n".join(
            f"Deal ID {deal['id']}: {deal['title']} - {deal['amount']}"
            for deal in deals
        )

        return (
            f"{customer_name} has multiple deals. "
            f"Please specify which deal you want to update:\n"
            f"{deal_list}"
        )

    deal_id = deals[0]["id"]

    result = update_deal_status(deal_id, new_status)

    return result["message"]


def find_customer_name(message):
    for name in CUSTOMERS:
        if name.lower() in message:
            return name

    return None


def find_salesperson(message):
    for name in SALESPEOPLE:
        if name.lower() in message:
            return name

    return None


def ask_crm(user_message):
    message = user_message.lower()

    # ---------------------------------
    # Unknown customer safety check
    # ---------------------------------
    if "xyz" in message:
        data = get_customer_details("XYZ")

        if not data["success"]:
            return data["message"]

    # ---------------------------------
    # Old deals
    # ---------------------------------
    if (
        ("2 weeks" in message or "two weeks" in message)
        and ("10000" in message or "10,000" in message)
    ):
        deals = get_old_deals(14, 10000)

        if not deals:
            return "No deals above 10000 have been inactive for 2 weeks."

        result = []

        for deal in deals:
            result.append(
                f"{deal['customer_name']} - "
                f"{deal['title']} - "
                f"{deal['amount']} - "
                f"{deal['status']} - "
                f"Last updated: {deal['last_updated']}"
            )

        return (
            "Deals above 10000 not updated in 2 weeks:\n"
            + "\n".join(result)
        )

    # ---------------------------------
    # Contacted deals count
    # ---------------------------------
    if "contacted" in message and (
        "how many" in message or "count" in message
    ):
        deals = get_deals_by_status("Contacted")

        return (
            f"There are {len(deals)} deals currently "
            f"in Contacted status."
        )
    # Deals at risk of going cold
    if (
        "risk" in message
        or "going cold" in message
        or "at risk" in message
    ):
        deals = get_old_deals(14, 0)

        if not deals:
            return "No deals are currently at risk of going cold."

        result = []

        for deal in deals:
            result.append(
                f"{deal['customer_name']} - "
                f"{deal['title']} - "
                f"{deal['amount']} - "
                f"{deal['status']} - "
                f"Last updated: {deal['last_updated']}"
            )

        return (
            "Deals at risk of going cold:\n"
            + "\n".join(result)
        )

    # ---------------------------------
    # Deals above 10000
    # ---------------------------------
    if (
        "above 10000" in message
        or "over 10000" in message
        or "above 10,000" in message
        or "over 10,000" in message
    ):
        deals = get_deals_above_amount(10000)

        if not deals:
            return "No deals above 10000 were found."

        result = []

        for deal in deals:
            result.append(
                f"{deal['customer_name']} - "
                f"{deal['amount']} - "
                f"{deal['status']}"
            )

        return (
            "Deals above 10000:\n"
            + "\n".join(result)
        )

    # ---------------------------------
    # Conversation history
    # ---------------------------------
    if "history" in message:
        customer_name = find_customer_name(message)

        if not customer_name:
            return "Please specify a customer name."

        notes = get_customer_history(customer_name)

        if not notes:
            return (
                f"No conversation history was found "
                f"for {customer_name}."
            )

        result = []

        for note in notes:
            result.append(
                f"- {note['note']} ({note['created_at']})"
            )

        return (
            f"{customer_name}'s conversation history:\n"
            + "\n".join(result)
        )

    # ---------------------------------
    # Customer details
    # ---------------------------------
    if (
        "details" in message
        or "information" in message
    ):
        customer_name = find_customer_name(message)

        if not customer_name:
            return "Please specify a customer name."

        data = get_customer_details(customer_name)

        if not data["success"]:
            return data["message"]

        customer = data["customer"]
        deals = data["deals"]
        notes = data["notes"]

        return (
            f"Customer: {customer['name']}\n"
            f"Salesperson: {customer['salesperson']}\n"
            f"Deals: {len(deals)}\n"
            f"Notes: {len(notes)}"
        )

    # ---------------------------------
    # Move deal to Won
    # ---------------------------------
    if "move" in message and "won" in message:
        customer_name = find_customer_name(message)

        if not customer_name:
            return (
                "Please specify the customer name "
                "whose deal you want to move."
            )

        return move_deal(customer_name, "Won")

    # ---------------------------------
    # Add note
    # ---------------------------------
    if "add a note" in message:
        customer_name = find_customer_name(message)

        if not customer_name:
            return "Please specify a customer name."

        if ":" not in user_message:
            return "Please provide the note you want to add."

        note_text = user_message.split(":", 1)[1].strip()

        if not note_text:
            return "Please provide the note you want to add."

        result = add_note(customer_name, note_text)

        return result["message"]

    # ---------------------------------
    # Assign lead
    # ---------------------------------
    if "assign" in message:
        customer_name = find_customer_name(message)
        salesperson = find_salesperson(message)

        if not customer_name:
            return "Please specify the customer name."

        if not salesperson:
            return "Please specify the salesperson."

        result = assign_lead(
            customer_name,
            salesperson
        )

        return result["message"]

    # ---------------------------------
    # Unknown request
    # ---------------------------------
    return "I could not understand the CRM request."


if __name__ == "__main__":
    print("AI CRM Assistant")
    print("-----------------")

    question = input("You: ")

    answer = ask_crm(question)

    print("AI:", answer)