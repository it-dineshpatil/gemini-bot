import pandas as pd
import os

def log(date,form_number,message,Chat_repy):
    data = {
        "Date":[date],
        'Number':[form_number],
        'Send_message':[message],
        "Chatbot_repy":[Chat_repy]
    }
    pf = pd.DataFrame(data)

    file_name = "log.xlsx"

    if os.path.exists(file_name):
        #read File 
        file_df = pd.read_excel(file_name)
  
        final_df = pd.concat([file_df, pf], ignore_index=True)
    else:
        final_df = pf

    
    final_df.to_excel(file_name, index=False)

