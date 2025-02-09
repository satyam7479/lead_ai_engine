# lead_ai_engine

## Overview

The Lead AI Engine is designed to process leads through qualification, categorization, and prioritization to help the sales team focus on high-value opportunities. The project uses a combination of agents and tasks defined in YAML configuration files to automate the lead processing workflow.

### Prerequisites

- Python 3.12 or 3.10(make sure to change pipfile)
- Required packages listed in `Pipfile`

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/satyam7479/lead_ai_engine.git
    cd lead_ai_engine
    ```

2. Create a  file in the root directory and add the necessary environment variables:

    ```env
    # Example .env file
    LLM_API_KEY=your_api_key_here
    LLAMA_BASE_URL=your_base_url
    ```
## Running the Application

1. Activate the Pipenv shell:

    ```sh
    pipenv shell
    ```
2. Install dependencies using Pipenv:

    ```sh
    pipenv install
    ```

3. Run the main application:

    ```sh
    pipenv run main
    ```

## Directory Structure
app/
    crew/
        agents_tasks.py
        crew.py
    config/
        agents.yaml
        tasks.yaml
    helper/
        general_helper.py
        llm_helper.py
.env
.gitignore
crew_workflow.yaml
lead_data.xlsx
main.py
Pipfile
Pipfile.lock
README.md

## Usage
The main application uses Streamlit to provide a web interface for adding, reprocessing, and batch uploading leads. Open your web browser and navigate to the provided URL after running the application.
