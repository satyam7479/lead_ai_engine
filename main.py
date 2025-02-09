import streamlit as st
import pandas as pd
import re
from io import BytesIO
from app.agents_tasks.agents import LeadProcessingCrew

# File path for the Excel sheet
EXCEL_PATH = "lead_data.xlsx"

def load_excel():
    """Loads the Excel file and returns the two sheets as DataFrames."""
    try:
        return pd.read_excel(EXCEL_PATH, sheet_name=["sheet-1", "sheet-2"])
    except FileNotFoundError:
        return {
            "sheet-1": pd.DataFrame(columns=[
                "id", "lead_source", "lead_status", "lead_country", "lead_email", 
                "lead_description", "lead_date", "lead_type", "lead_category", 
                "technology", "complexity", "created_at", "updated_at"
            ]), 
            "sheet-2": pd.DataFrame(columns=["id", "status(qualified_status)", "priority"])
        }

def save_excel(df1, df2):
    """Saves updated data to lead_data.xlsx with two sheets."""
    with pd.ExcelWriter(EXCEL_PATH, engine="xlsxwriter") as writer:
        df1.to_excel(writer, sheet_name="sheet-1", index=False)
        df2.to_excel(writer, sheet_name="sheet-2", index=False)


def extract_values_from_result(result):
    # Use regex to extract priority and status
    priority_match = re.search(r'- \*\*Assigned Priority Level:\*\*\s*(\w+)', result)
    status_match = re.search(r'- \*\*Qualified Status:\*\*\s*(\w+)', result)
    
    # Extract values or return 'Unknown' if not found
    priority = priority_match.group(1) if priority_match else 'Unknown'
    status = status_match.group(1) if status_match else 'Unknown'
    print("Priority:", priority)
    print("Status:", status)
    
    return {"Status": status, "Priority": priority}


def process_lead(inputs, lead_id, df_results):
    """Runs AI processing and updates sheet-2 with the results."""
    crew_instance = LeadProcessingCrew()
    
    result = crew_instance.crew().kickoff(inputs=inputs).raw
    st.markdown(result)
    
    extracted_data = extract_values_from_result(result)
    
    new_result = {
        "id": lead_id, 
        "status(qualified_status)": extracted_data["Status"],
        "priority": extracted_data["Priority"]
    }
    
    df_results = pd.concat([df_results, pd.DataFrame([new_result])], ignore_index=True)
    return df_results

def main():
    st.title("Lead Engine AI")

    # Load existing Excel data
    data = load_excel()
    df_leads = data["sheet-1"]
    df_results = data["sheet-2"]

    # Get the next lead ID
    next_id = 1 if df_leads.empty else df_leads["id"].max() + 1

    tab1, tab2, tab3 = st.tabs(["🔹 Add New Lead", "🔄 Reprocess Existing Lead", "📤 Batch Upload Leads"])

    # TAB 1: Manually Enter New Lead
    with tab1:
        with st.form("lead_form"):
            st.subheader("Enter Lead Details")
            lead_source = st.text_input("Lead Source")
            lead_status = st.selectbox("Lead Status", ["New", "Suspect", "Deal", "Closed"])
            lead_country = st.text_input("Lead Country")
            lead_email = st.text_input("Lead Email")
            lead_description = st.text_area("Lead Description")
            lead_type = st.text_input("Lead Type")
            lead_date = st.date_input("Lead Date")
            lead_category = st.text_input("Lead Category")

            submitted = st.form_submit_button("Process Lead")

        if submitted:
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

                df_results = process_lead(inputs, next_id, df_results)

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
                    "technology": "",
                    "complexity": "",
                    "created_at": pd.Timestamp.now(),
                    "updated_at": pd.Timestamp.now()
                }
                df_leads = pd.concat([df_leads, pd.DataFrame([new_lead])], ignore_index=True)

                # Save to Excel
                save_excel(df_leads, df_results)
                st.success("Lead processed successfully!")
                st.download_button("📥 Download Updated Leads Data", data=open(EXCEL_PATH, "rb"), file_name="lead_data.xlsx")
                

    # TAB 2: Reprocess Existing Lead
    with tab2:
        st.subheader("Select an Existing Lead to Reprocess")
        if df_leads.empty:
            st.info("No leads available.")
        else:
            selected_id = st.selectbox("Select Lead ID", df_leads["id"])
            selected_lead = df_leads[df_leads["id"] == selected_id].iloc[0]

            st.write("### Selected Lead Details")
            st.json(selected_lead.to_dict())

            if st.button("Reprocess Lead"):
                inputs = selected_lead.drop(["id", "created_at", "updated_at"]).to_dict()
                df_results = process_lead(inputs, selected_id, df_results)
                save_excel(df_leads, df_results)
                st.success("Lead reprocessed successfully!")
                st.download_button("📥 Download Updated Leads Data", data=open(EXCEL_PATH, "rb"), file_name="lead_data.xlsx")


   # TAB 3: Batch Upload Leads
    with tab3:
        st.subheader("Upload an Excel File with Leads")
        uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

        # Flag to check if processing was successful
        success_flag = False  

        if uploaded_file:
            uploaded_data = pd.read_excel(uploaded_file)

            required_columns = [
                "lead_source", "lead_status", "lead_country", "lead_email", 
                "lead_description", "lead_date", "lead_type", "lead_category"
            ]

            if not all(col in uploaded_data.columns for col in required_columns):
                st.error(f"Uploaded file must have columns: {', '.join(required_columns)}")
            else:
                uploaded_data = uploaded_data.dropna(subset=required_columns, how="any").reset_index(drop=True)

                # Wrap in a form
                with st.form("batch_upload_form"):
                    submitted = st.form_submit_button("Process Leads")

                    if submitted:
                        new_leads = []
                        new_results = []

                        for _, row in uploaded_data.iterrows():
                            # Assign unique ID to each lead
                            lead_id = next_id  
                            next_id += 1

                            inputs = row.to_dict()

                            # Skip empty rows
                            if not any(inputs.values()):
                                continue  
                            
                            df_results = process_lead(inputs, lead_id, df_results) 

                            row["id"] = lead_id
                            row["technology"] = ""
                            row["complexity"] = ""
                            row["created_at"] = pd.Timestamp.now()
                            row["updated_at"] = pd.Timestamp.now()
                            new_leads.append(row)

                        # Only append if there are new leads
                        if new_leads:
                            df_leads = pd.concat([df_leads, pd.DataFrame(new_leads)], ignore_index=True)

                        # Save updated data
                        save_excel(df_leads, df_results)
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

if __name__ == "__main__":
    main()
