from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from supabase_client import supabase
import re
from datetime import datetime

# First create the app
app = Flask(__name__)

# Optional root route for health check
@app.route("/")
def index():
    return "✅ Chama Bot is up and running!"

# WhatsApp webhook
@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip().lower()
    from_number = request.values.get("From", "").replace("whatsapp:", "")
    resp = MessagingResponse()
    msg = resp.message()

    member = supabase.table("members").select("*").eq("phone_number", from_number).single().execute()
    if not member.data:
        msg.body("You are not registered. Please contact the admin.")
        return str(resp)

    member_id = member.data["id"]

    if "balance" in incoming_msg:
        payments = supabase.table("payments").select("*").eq("member_id", member_id).eq("is_paid", False).execute().data
        total_due = sum(p["amount_due"] for p in payments)
        msg.body(f"Your total outstanding balance is ${total_due}.")

    elif match := re.match(r"paid\\s+(\\d+)", incoming_msg):
        amount = float(match.group(1))
        unpaid = supabase.table("payments").select("*").eq("member_id", member_id).eq("is_paid", False).limit(1).execute()
        if unpaid.data:
            payment_id = unpaid.data[0]["id"]
            supabase.table("payments").update({
                "is_paid": True,
                "paid_at": datetime.utcnow().isoformat()
            }).eq("id", payment_id).execute()
            msg.body(f"Thanks! Your payment of ${amount} was recorded.")
        else:
            msg.body("You have no outstanding payments.")
    else:
        msg.body("Send 'balance' or 'paid <amount>'")

    return str(resp)

# Optional: only needed for local testing
if __name__ == "__main__":
    app.run(debug=True)
