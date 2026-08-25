import os
import streamlit as st
import json
# python -m streamlit run web.py
json_path = os.path.join(os.path.dirname(__file__), "number.json")
with open(json_path, "r") as f:
    data = json.load(f)
    
st.title("Number Map")

# Add New Number
with st.expander("Add New Number"):
    with st.form("add_number_form"):
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("Enter Phone Number", value=91, placeholder="918140021166")
        with col2:
            name = st.text_input("Enter Name", placeholder="dinesh")        
        submitted = st.form_submit_button("Submit")
        if submitted:
            if phone.strip() and name.strip():
                data[phone.strip()] = name.strip()
                with open(json_path, "w") as f:
                    json.dump(data, f, indent=4)
                st.success(f"Successfully added {name} ({phone})")
                st.rerun()
            else:
                st.warning("Please enter both a Phone Number and a Name.")

# Delete Number
with st.expander("Delete Number"):
    with st.form("delete_number_form", clear_on_submit=True):
        options = list(data.keys())
        selected_phones = st.multiselect(
            "Select Number(s) to Delete",
            options=options,
            format_func=lambda p: f"{data[p]} ({p})" if p in data else p
        )
        delete_submitted = st.form_submit_button("Remove")
        if delete_submitted:
            if selected_phones:
                for p in selected_phones:
                    if p in data:
                        del data[p]
                with open(json_path, "w") as f:
                    json.dump(data, f, indent=4)
                st.success("Successfully deleted selected record(s).")
                st.rerun()
            else:
                st.warning("Please select at least one number to delete.")

# Search / Filter
search_query = st.text_input("Search by Name or Phone Number", placeholder="Type to filter...")

# Convert JSON key-value pairs into table rows with column headers
table_data = [
    {"sr": sr + 1, "Phone Number": phone, "Name": name}
    for sr, (phone, name) in enumerate(data.items())
    if search_query.lower() in str(phone).lower() or search_query.lower() in str(name).lower()
]
st.table(table_data)

