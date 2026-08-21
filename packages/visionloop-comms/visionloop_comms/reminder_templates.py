from typing import Optional

class CollectionReminderEngine:
    """Generates polite to legally escalated billing reminders for WhatsApp/Email."""
    
    @staticmethod
    def generate_message(
        lessee_name: str,
        invoice_number: str,
        amount: float,
        due_date: str,
        stage: str = "DUE_DATE", # UPCOMING, DUE_DATE, OVERDUE, ESCALATION
        upi_link: Optional[str] = None
    ) -> str:
        pay_instruction = f"\n👉 Click to Pay via UPI: {upi_link}" if upi_link else ""
        
        if stage == "UPCOMING":
            return (
                f"Namaste {lessee_name}! 🙏\n"
                f"This is a friendly reminder from Vision Loop. Your commercial lease invoice {invoice_number} "
                f"for ₹{amount:,.2f} is scheduled for due settlement on {due_date}.{pay_instruction}\n"
                f"Thank you for choosing Vision Loop!"
            )
        elif stage == "DUE_DATE":
            return (
                f"Namaste {lessee_name}! ⚡\n"
                f"Your commercial lease invoice {invoice_number} for ₹{amount:,.2f} is due today ({due_date}).\n"
                f"Please remit via your e-NACH mandate or scan to pay:{pay_instruction}\n"
                f"Prompt payment ensures continuous, uninterrupted vehicle telematics service."
            )
        elif stage == "OVERDUE":
            return (
                f"Important Notice for {lessee_name} ⚠️\n"
                f"Invoice {invoice_number} for ₹{amount:,.2f} is now overdue past {due_date}.\n"
                f"As per the MSMED Act, 2006 statutory terms, please clear this balance immediately to avoid contractual late interest.{pay_instruction}"
            )
        else: # ESCALATION
            return (
                f"LEGAL DEMAND NOTICE — {lessee_name} 🚨\n"
                f"Payment for Invoice {invoice_number} (₹{amount:,.2f}) has exceeded the contractual grace period. "
                f"Failure to settle within 48 hours will trigger Section 16 MSMED compounding interest and remote vehicle standstill immobilization.{pay_instruction}"
            )
