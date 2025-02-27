# Lead AI Engine

## Overview

The Lead AI Engine is designed to process leads through qualification, categorization, and prioritization to help the sales team focus on high-value opportunities. The project uses a combination of agents and tasks defined in YAML configuration files to automate the lead processing workflow.

### Prerequisites

- Python 3.10
- Required packages listed in `Pipfile`
- For versioning please refer requirements.txt file
- I have used ubuntu-22 or windows-11(This project compatible with both)

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/satyam7479/lead_ai_engine.git
    cd lead_ai_engine
    ```

2. Create a `secrets.toml` file in the root directory and add the necessary environment variables:

    ```
    # Example secrets.toml file
    LLAMA_MODEL="ollama/llama3.2:latest"
    LLAMA_BASE_URL="http://localhost:11434"
    GEMINI_MODEL="gemini/your_gemini_model_name"
    GEMINI_API_KEY="your_gemini_api_key"
    EXCEL_PATH="lead_data.xlsx"
    ```
# Run the Project with Docker
## Setting Up the Remote User

Ensure that the remote user is set correctly in the `devcontainer.json` and `Dockerfile`. The default user is `verve` with UID `1000` and GID `1000`. If you need to change these values, update the following files:

1. **devcontainer.json**:
    ```jsonc
    {
      "build": {
        "args": {
          "REMOTE_USER": "your_username",
          "NEW_UID": "your_uid",
          "NEW_GID": "your_gid"
        }
      },
      "remoteUser": "your_username",
      ...
    }
    ```

2. **Dockerfile**:
    ```dockerfile
    # Build arguments
    ARG REMOTE_USER=your_username
    ARG NEW_UID=your_uid
    ARG NEW_GID=your_gid
    ```

Replace `your_username`, `your_uid`, and `your_gid` with the appropriate values for your setup.

After making these changes, rebuild your development container to apply the new settings.

3. Build the Docker container:

    ```sh
    docker build -t lead_ai_engine -f .devcontainer/Dockerfile .
    ```

4. Run the Docker container:

    ```sh
    docker run -p 8501:8501 -v $(pwd):/workspace --env-file secrets.toml lead_ai_engine
    ```

# Run the Project with pipenv

1. Make virtual env from pipepnv
   
    ```sh
    pipenv shell
    ```
    
2. After successfully creating virtual env from pipenv, please Select the Interpreter for the created venv in your code editor which you are using e.g., vs-code
   
3. Install dependencies using Pipenv:

    ```sh
    pipenv install
    ```

## Run the main application:

    ```sh
    pipenv run main
    ```
    
## Change llm configuration (Gemini or Ollama) by uncommenting the llm you want to run
Navigate:  

     ```sh
     app/crew/agents_tasks.py
     ```
    
    # Load LLM configuration (Gemini or Ollama)
    llm = LlmHelper.GeminiConnection()
    # llm = LlmHelper.llamaConnection()
    
## For any issues/ Troubleshoot
1.   Ensure you are running the code inside the correct virtual environment (pipenv).
2.   Ensure you have selected the correct Interpreter as of your pipenv env name
3.   If still getting any error please update your "Pipfile" with the below code, by ensuring you are using python 3.10 version:

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
    
4.  Delete Pipfile.lock:
   
    ```sh
    rm Pipfile.lock
    ```
    
5. Install dependencies using Pipenv:

    ```sh
    pipenv install
    ```
    Then run your application by: **pipenv run main**
   
6.   If still getting any error, please update pipenv dependencies:

    ```sh
    pipenv update
    ```
   Then run your application by: **pipenv run main**
   
7. If still getting any error, please contact me at **sk6005848@gmail.com**

## Usage
The main application uses Streamlit to provide a web interface for adding, reprocessing, and batch uploading leads. Open your web browser and navigate to the provided URL after running the application.
