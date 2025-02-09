# Description: Helper functions for loading, saving, and processing data.
import streamlit as st
import pandas as pd
import re
from app.crew.agents_tasks import LeadProcessingCrew

# File path for the Excel sheet
EXCEL_PATH = "lead_data.xlsx"

class Helper:
    # Load and save Excel data
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

    # Save the updated data to Excel
    def save_excel(df1, df2):
        """Saves updated data to lead_data.xlsx with two sheets."""
        with pd.ExcelWriter(EXCEL_PATH, engine="xlsxwriter") as writer:
            df1.to_excel(writer, sheet_name="sheet-1", index=False)
            df2.to_excel(writer, sheet_name="sheet-2", index=False)

    # Extract values from the AI result
    def extract_values_from_result(result):
        # Normalize spacing and remove unwanted characters for consistent matching
        result = result.replace("\n", " ").strip()

        # Regex pattern to match both bold (`**`) and non-bold formats
        priority_pattern = r"(?:-?\s*\*?\*?Assigned Priority Level:\*?\*?\s*)(\w+)"
        status_pattern = r"(?:-?\s*\*?\*?Qualified Status:\*?\*?\s*)(\w+)"

        # Extract priority and status using regex
        priority_match = re.search(priority_pattern, result, re.IGNORECASE)
        status_match = re.search(status_pattern, result, re.IGNORECASE)

        # Extract values or return 'Unknown' if not found
        priority = priority_match.group(1) if priority_match else "Unknown"
        status = status_match.group(1) if status_match else "Unknown"

        return {"Status": status, "Priority": priority}

    # Process the lead using the AI model
    def process_lead(inputs, lead_id, df_results):
        """Runs AI processing and updates sheet-2 with the results."""
        # Initialize the AI model
        crew_instance = LeadProcessingCrew()
        
        # Run the AI model
        result = crew_instance.crew().kickoff(inputs=inputs).raw
        
        # Display the AI result
        st.markdown(result)
        
        extracted_data = Helper.extract_values_from_result(result)
        new_result = {
            "id": lead_id, 
            "status(qualified_status)": extracted_data["Status"],
            "priority": extracted_data["Priority"]
        }
        # Append the new result to the existing sheet-2
        df_results = pd.concat([df_results, pd.DataFrame([new_result])], ignore_index=True)
        return df_results