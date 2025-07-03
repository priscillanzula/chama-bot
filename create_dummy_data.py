# create_dummy_data.py

from supabase import create_client
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_dummy_data():
    # Step 1: Create Members
    members = [
        {"name": "Nzula Priscila", "phone_number": "+254792214211"},
        {"name": "CipheredBits", "phone_number": "+254762490862"},
        {"name": "Motile Wamorris", "phone_number": "+2348184296075"},
    ]

    created_members = supabase.table("members").insert(members).execute()

    if created_members.error:
        print("❌ Error inserting members:", created_members.error)
        return

    member_data = created_members.data
    print("✅ Members created:", member_data)

    # Step 2: Create Payments
    today = datetime.utcnow().date()
    next_week = today + timedelta(days=7)

    payments = [
        {"member_id": member_data[0]["id"], "amount_due": 1000, "due_date": today.isoformat()},
        {"member_id": member_data[1]["id"], "amount_due": 1000, "due_date": today.isoformat()},
        {"member_id": member_data[2]["id"], "amount_due": 1000, "due_date": next_week.isoformat()},
        {"member_id": member_data[0]["id"], "amount_due": 500, "due_date": next_week.isoformat(), "is_paid": True, "paid_at": datetime.utcnow().isoformat()},
    ]

    created_payments = supabase.table("payments").insert(payments).execute()
    if created_payments.error:
        print("❌ Error inserting payments:", created_payments.error)
        return

    payment_data = created_payments.data
    print("✅ Payments created:", payment_data)

    # Step 3: Create Reminders
    reminders = [
        {"payment_id": payment_data[3]["id"], "message_text": "Payment reminder for Nzula Priscila", "status": "sent"},
    ]

    created_reminders = supabase.table("reminders").insert(reminders).execute()
    if created_reminders.error:
        print("❌ Error inserting reminders:", created_reminders.error)
        return

    print("✅ Reminders created:", created_reminders.data)

if __name__ == "__main__":
    create_dummy_data()
