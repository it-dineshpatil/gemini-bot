from whatsapp_send_text import whatsapp_send_text
from Template_send import assigned_a_ticket
# from regarding_per import create_by
def regarding_pers_audio_with(meationwhatsapp,  sender_name: str, docname: str, data: dict, url: str = None):
    message = (
        f"🎯 *You are assigned a Ticket*\n\n"
        f"👤 *Created By:* {sender_name}\n"
        f"🆔 *Ticket ID:* #{docname}\n"
        f"📌 *Subject:* {data.get('subject', 'N/A')}\n"
        # f"📝 *Regarding:* {data.get('custom_issue_regarding ', 'N/A')}\n"
        f"📅 *Reminder Date:* {data.get('custom_remainder_date', 'N/A')}\n"
        f"⭐ *Priority:* {data.get('priority', 'N/A')}\n\n"
        f"💬 *Audio Message:* {url}\n"
        f"🔗 _Keep this ID for tracking._"
    )
    # message_status= whatsapp_send_text(meationwhatsapp, message)
    # if message_status == 200:
    temp_status = assigned_a_ticket(meationwhatsapp, sender_name, docname, data, url)
    return temp_status
def regarding_pers(meationwhatsapp,  sender_name: str, docname: str, data: dict):
    message = (
        f"🎯 *You are assigned a Ticket*\n\n"
        f"👤 *Created By:* {sender_name}\n"
        f"🆔 *Ticket ID:* #{docname}\n"
        f"📌 *Subject:* {data.get('subject', 'N/A')}\n"
        # f"📝 *Regarding:* {data.get('custom_issue_regarding ', 'N/A')}\n"
        f"📅 *Reminder Date:* {data.get('custom_remainder_date', 'N/A')}\n"
        f"⭐ *Priority:* {data.get('priority', 'N/A')}\n\n"
        f"🔗 _Keep this ID for tracking._"
    )
    return whatsapp_send_text(meationwhatsapp, message)

# regarding_pers("918140021166", "dinesh", "DdfdOdfds", {"subject": "Test Ticket"})

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