from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
import os
from dotenv import load_dotenv
from app.config.helper.llm_helper import LlmHelper

load_dotenv()

# Load LLM configuration (Gemini or Ollama)
llm = LlmHelper.GeminiConnection()
# llm = LlmHelper.llamaConnection()

@CrewBase
class LeadProcessingCrew:
    """Lead Qualification, Categorization, and Prioritization Crew"""

    # Load agent and task configurations from YAML files
    agents_config = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/agents.yaml"))
    tasks_config = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/tasks.yaml"))

    @agent
    def lead_qualification_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["lead_qualification_agent"],
            allow_delegation=False,
            verbose=True,
            llm=llm,
        )

    @agent
    def service_categorization_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["service_categorization_agent"],
            allow_delegation=False,
            verbose=True,
            llm=llm,
        )

    @agent
    def lead_prioritization_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["lead_prioritization_agent"],
            allow_delegation=False,
            verbose=True,
            llm=llm,
            
        )

    @task
    def lead_qualification_task(self) -> Task:
        return Task(
            config=self.tasks_config["lead_qualification_task"], 
            agent=self.lead_qualification_agent()
        )

    @task
    def service_categorization_task(self) -> Task:
        return Task(
            config=self.tasks_config["service_categorization_task"], 
            agent=self.service_categorization_agent()
        )

    @task
    def lead_prioritization_task(self) -> Task:
        return Task(
            config=self.tasks_config["lead_prioritization_task"], 
            agent=self.lead_prioritization_agent()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.lead_qualification_agent(),
                self.service_categorization_agent(),
                self.lead_prioritization_agent(),
            ],
            tasks=[
                self.lead_qualification_task(),
                self.service_categorization_task(),
                self.lead_prioritization_task(),
            ],
            process=Process.sequential,  
            verbose=True,
        )

