import streamlit as st
import pandas as pd
from app.helper.general_helper import Helper

# File path for the Excel sheet
EXCEL_PATH = "lead_data.xlsx"

st.title("Lead Engine AI")

# Load existing Excel data
data = Helper.load_excel()

# Extract the two DataFrames
df_leads = data["sheet-1"]
df_results = data["sheet-2"]

# Get the next lead ID
next_id = 1 if df_leads.empty else df_leads["id"].max() + 1

tab1, tab2, tab3 = st.tabs(["🔹 Add New Lead", "🔄 Reprocess Existing Lead", "📤 Batch Upload Leads"])

# TAB 1: Manually Enter New Lead
with tab1:
    with st.form("lead_form"):
        st.subheader("Enter Lead Details")
        lead_source = st.text_input("Lead Source", placeholder="e.g., Website, Referral, Linkedin, etc.")
        lead_status = st.selectbox("Lead Status", ["New", "Suspect", "Deal", "Closed"])
        lead_country = st.text_input("Lead Country", placeholder="e.g., India, USA, UK, etc.")
        lead_email = st.text_input("Lead Email", placeholder="e.g., example@gmail.com")
        lead_type = st.text_input("Lead Type", placeholder="e.g., B2B, B2C, Web Dev, etc.")
        lead_date = st.date_input("Lead Date")
        lead_category = st.text_input("Lead Category", placeholder="e.g., Sales, Marketing, Support, Cold Lead, etc.")
        lead_description = st.text_area("Lead Description", placeholder="Enter a brief description of the lead...")
        
        # Submit button
        submitted = st.form_submit_button("Process Lead")

    # Process the lead if submitted
    if submitted:
        # Check if all fields are filled
        if not all([lead_source, lead_status, lead_country, lead_email, lead_description, lead_type, lead_date, lead_category]):
            st.warning("Please fill in all fields before submitting.")
        else:
            inputs = {
                "lead_source": lead_source,
                "lead_status": lead_status,
                "lead_country": lead_country,
                "lead_email": lead_email,
                "lead_description": lead_description,
                "lead_type": lead_type,
                "lead_date": str(lead_date),
                "lead_category": lead_category
            }
            # Process the lead
            df_results = Helper.process_lead(inputs, next_id, df_results)
            
            # Update sheet-1
            new_lead = {
                "id": next_id, 
                "lead_source": lead_source, 
                "lead_status": lead_status, 
                "lead_country": lead_country, 
                "lead_email": lead_email, 
                "lead_description": lead_description, 
                "lead_date": str(lead_date),
                "lead_type": lead_type,
                "lead_category": lead_category,
                "created_at": pd.Timestamp.now(),
                "updated_at": pd.Timestamp.now()
            }
            # Increment the next ID
            df_leads = pd.concat([df_leads, pd.DataFrame([new_lead])], ignore_index=True)

            # Save to Excel
            Helper.save_excel(df_leads, df_results)
            st.success("Lead processed successfully!")
            st.download_button("📥 Download Updated Leads Data", data=open(EXCEL_PATH, "rb"), file_name="lead_data.xlsx")
            

# TAB 2: Reprocess Existing Lead
with tab2:
    st.subheader("Select an Existing Lead to Reprocess")
    if df_leads.empty:
        st.info("No leads available.")
    else:
        selected_id = st.selectbox("Select Lead ID", df_leads["id"])
        
        # Get index of selected lead
        selected_lead_idx = df_leads[df_leads["id"] == selected_id].index[0] 
        
        #Fetch lead details
        selected_lead = df_leads.loc[selected_lead_idx] 
        
        # Display selected lead details
        st.write("### Selected Lead Details")
        st.json(selected_lead.to_dict())

        if st.button("Reprocess Lead"):
            # Get the inputs for the selected lead
            inputs = selected_lead.drop(["id", "created_at", "updated_at"]).to_dict()
            
            # Process the lead
            df_results = Helper.process_lead(inputs, selected_id, df_results)
            
            # Update the 'updated_at' column
            df_leads.at[selected_lead_idx, "updated_at"] = pd.Timestamp.now()
            
            # Save to Excel
            Helper.save_excel(df_leads, df_results)
            st.success("Lead reprocessed successfully!")
            st.download_button("📥 Download Updated Leads Data", data=open(EXCEL_PATH, "rb"), file_name="lead_data.xlsx")


# TAB 3: Batch Upload Leads
with tab3:
    st.subheader("Upload an Excel File with Leads")
    uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

    # Flag to check if processing was successful
    success_flag = False  

    if uploaded_file:
        # Read the uploaded file
        uploaded_data = pd.read_excel(uploaded_file)

        required_columns = [
            "lead_source", "lead_status", "lead_country", "lead_email", 
            "lead_description", "lead_date", "lead_type", "lead_category"
        ]

        # Check if uploaded file has required columns
        if not all(col in uploaded_data.columns for col in required_columns):
            st.error(f"Uploaded file must have columns: {', '.join(required_columns)}")
        else:
            # Drop rows with missing values in required columns
            uploaded_data = uploaded_data.dropna(subset=required_columns, how="any").reset_index(drop=True)

            # Wrap in a form
            with st.form("batch_upload_form"):
                submitted = st.form_submit_button("Process Leads")

                if submitted:
                    # Initialize new leads list to store processed leads
                    new_leads = []
                    
                    # Process each lead
                    for _, row in uploaded_data.iterrows():
                        # Assign unique ID to each lead
                        lead_id = next_id  
                        next_id += 1
                        
                        # Convert row to dictionary
                        inputs = row.to_dict()

                        # Skip empty rows or rows with missing values
                        if not any(inputs.values()):
                            continue  
                        
                        # Process the lead
                        df_results = Helper.process_lead(inputs, lead_id, df_results) 
                        
                        # Append the new lead to the list
                        row["id"] = lead_id
                        row["created_at"] = pd.Timestamp.now()
                        row["updated_at"] = pd.Timestamp.now()
                        
                        # Append the new lead to the list
                        new_leads.append(row)

                    # Only append if there are new leads to add
                    if new_leads:
                        # Append new leads to the existing sheet-1
                        df_leads = pd.concat([df_leads, pd.DataFrame(new_leads)], ignore_index=True)

                    # Save updated data
                    Helper.save_excel(df_leads, df_results)
                    st.success("Batch leads processed successfully!")
                    
                    # Set flag to True if processing was successful
                    success_flag = True 

            # Provide download button if successful and there are new leads                
            if success_flag and not df_leads.empty:
                with open(EXCEL_PATH, "rb") as file:
                    st.download_button(
                        "📥 Download Updated Leads Data",
                        data=file,
                        file_name="lead_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

