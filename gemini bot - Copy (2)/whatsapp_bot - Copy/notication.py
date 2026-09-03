from whatsapp_send_text import whatsapp_send_text

def regarding_pers(meationwhatsapp, sender_name, docname, data):
    message = (
        f"🎯 *You are assigned a Ticket*\n\n"
        f"👤 *Created By:* {sender_name}\n"
        f"🆔 *Ticket ID:* #{docname}\n"
        f"📌 *Subject:* {data.get('subject', 'N/A')}\n"
        f"📝 *Regarding:* {data.get('custom_issue_regarding ', 'N/A')}\n"
        f"📅 *Reminder Date:* {data.get('custom_remainder_date', 'N/A')}\n"
        f"⭐ *Priority:* {data.get('priority', 'N/A')}\n\n"
        f"🔗 _Keep this ID for tracking._"
    )
    return whatsapp_send_text(meationwhatsapp, message)

def ticket_details_noti(from_number, docname, data):
    message = (
    f"✅ *Ticket #{docname}*\n\n"
    f"📌 *Subject:* {data.get('subject', 'N/A')}\n"
    f"📝 *Regarding:* {data.get('custom_issue_regarding', 'N/A')}\n"
    f"📅 *Reminder Date:* {data.get('custom_remainder_date')}\n"
    f"⭐ *Priority:* {data.get('priority', 'N/A')}\n\n"
    f"🔗 _Keep this ID for tracking._"
    )
    return whatsapp_send_text(from_number,message)