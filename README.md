# Lead AI Engine

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

2. Create a secrets.toml file in the root directory and add the necessary environment variables:

    ```
    # Example secrets.toml file
    LLM_API_KEY=your_api_key_here
    LLAMA_BASE_URL=your_base_url
    GEMINI_MODEL=gemini/<your gemini model name>
    GEMINI_API_KEY=your gemini api key
    EXCEL_PATH=lead_data.xlsx
    ```
4. For any issues

4.1> Ensure you are running the code inside the correct virtual environment (pipenv).
4.2> Ensure you have selected the correct Interpreter as of your pipenv env name
4.3> Is still getting any error please update your "Pipfile" with the below with ensuring you are using python 3.10 version:

    ```sh
    [[source]]
    url = "https://pypi.org/simple"
    verify_ssl = true
    name = "pypi"

    [packages]
    streamlit = "==1.41.1"
    httpx = "==0.27.2"
    python-dotenv = "==1.0.1"
    numpy = "==1.26.4"
    crewai = "==0.100.1"
    crewai-tools = "==0.33.0"
    xlsxwriter = "3.2.2"
    pyyaml = "==6.0.2"

    [dev-packages]

    [requires]
    python_version = "3.10"

    [scripts]
    main = "streamlit run main.py"
    ```
4.5> Delete Pipfile.lock and run the below cmd:
    ```sh
    pipenv install
    ```

4.6> If still getting any error, please update pipenv dependencies:

    ```sh
    pipenv update
    ```
2. Install dependencies using Pipenv:

    ```sh
    pipenv install
    ```

3. Run the main application:

    ```sh
    pipenv run main
    ```

## Usage
The main application uses Streamlit to provide a web interface for adding, reprocessing, and batch uploading leads. Open your web browser and navigate to the provided URL after running the application.
