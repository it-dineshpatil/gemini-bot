from main import fetch_customers
from whatsapp_send_text import whatsapp_send_text
from Whatsapp_file_send import whatsapp_send_file
from Jobwork_order_idashboard import execute_and_export_report

# from Template_send import Template_send
def about_person(from_number,message_text):
    message = (
        "Hello 👋\n\n"
        "Welcome to Gokul Text Print Support.\n"
        "For any Query, Please call our support team directly at 📞 9904455516.\n\n"
        "We’ll be glad to assist you."
    )
    whatsapp_send_text(from_number,message)

    


def samesales(from_number):
    match from_number:
        case "919375373663":
            return "Chandan Singh"
        case "919310002625":
            return "Jai Shankar Ji"
        case "919586092901":
            return "Dilip Singh"
        case "919328413002":
            return "Dilip Singh"
        case "919737250002":
            return "Bikash Behera"
        case "919792510910":
            return "Manoj Pandey"
        case "919974972625":
            return "Kamlesh Yadav"
        case "919304450508":
            return "Ranjit Gupta"
        case "919974912625":
            return "Javed Mohd."
        case "918140021166":
            return "Bikash Behera"
        case _:
            return "None"
# print(samesales("918140021166"))       
# USER RESPONSE ANALYSIS AND REPLY GENERATION
def requment_analysis(from_number, message_text):
    if "job" in message_text.lower():
        return jobwork_report(from_number, message_text)
    
    elif "sales" in message_text.lower():
        return sales_report(from_number, message_text)
    else:
        return "unknown"
    whatsapp_send_text(from_number,)
    
def jobwork_report(from_number, message_text=None):
        print(from_number)
        sales = samesales(from_number)
        if sales == "None":
            whatsapp_send_text(from_number,"🤔 Sorry, I couldn't identify you.  Only Salesman Allow..")
            return "🤔 Sorry, I couldn't identify you.  Only Salesman Allow.."
        else:
            message = "📊 Jobwork Order Dashboard Report\n ⏳ Sending in progress...\n ✅ The report will be delivered within 1 minute."
            whatsapp_send_text(from_number,message)
            file_path = execute_and_export_report(sales)
            whatsapp_send_file(from_number, file_path, f"Hello {sales}, here is your jobwork report.")

def sales_report(from_number, message_text):
    whatsapp_send_text(from_number, "Sales report functionality is under development. Please check back later.")


#     pass

def reply_analysis(from_number, message_text):

    salesman = samesales(from_number)


    if salesman == "None":
       about_person(from_number,message_text)
    else:
        result = requment_analysis(from_number, message_text)

        if result == "unknown":
            whatsapp_send_text(from_number, "Sorry, I didn't understand that request. Please ask for 'jobwork report' or 'sales report'.")

  
        
    # whatsapp_send_text(from_number, salesman)