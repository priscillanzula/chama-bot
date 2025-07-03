import schedule, time
from twilio.rest import Client
from supabase_client import supabase
import os

client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH"))

def send_reminders():
    members = supabase.table("members").select("*").execute().data
    for m in members:
        payments = supabase.table("payments").select("*").eq("member_id", m["id"]).eq("is_paid", False).execute().data
        if payments:
            total = sum(p["amount_due"] for p in payments)
            message = f"Hi {m['name']}, you owe ${total}. Reply 'paid <amount>' once paid."
            client.messages.create(
                from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
                to=f"whatsapp:{m['phone_number']}",
                body=message
            )
            for p in payments:
                supabase.table("reminders").insert({
                    "payment_id": p["id"],
                    "message_text": message
                }).execute()

schedule.every().day.at("09:00").do(send_reminders)

while True:
    schedule.run_pending()
    time.sleep(60)