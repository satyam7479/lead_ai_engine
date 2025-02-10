# Description: Define the agents and tasks for the Lead Processing Crew
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
import os
from app.helper.llm_helper import LlmHelper

# Load LLM configuration (Gemini or Ollama)
llm = LlmHelper.GeminiConnection()
# llm = LlmHelper.llamaConnection()

# Define the Lead Processing Crew
@CrewBase
class LeadProcessingCrew:
    """Lead Qualification, Categorization, and Prioritization Crew"""

    # Load agent and task configurations from YAML files
    agents_config = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/agents.yaml"))
    tasks_config = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/tasks.yaml"))

    # Define agents and tasks
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

    # Define the crew using the agents and tasks
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

