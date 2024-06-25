from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from core.tools.agent_tools import ScraperTool
from langchain_groq import ChatGroq
from datetime import datetime
import os


@CrewBase
class NewspaperCrew:
    """Newspaper crew"""

    agents_config = "core/agents/agents.yaml"
    tasks_config = "core/tasks/tasks.yaml"

    def llm(self):
        llm = ChatGroq(model="llama3-70b-8192",
               groq_api_key= os.getenv('GROQ_API_KEY'))

        return llm

    @agent
    def scraper(self) -> Agent:
        return Agent(
            config=self.agents_config["scraper"],
            tools=[ScraperTool()],
            verbose=True,
            allow_delegation=False,
            llm=self.llm(),
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            verbose=True,
            allow_delegation=False,
            llm=self.llm(),
        )

    @agent
    def designer(self) -> Agent:
        return Agent(
            config=self.agents_config["designer"],
            verbose=True,
            allow_delegation=False,
            llm=self.llm(),
        )

    @task
    def scrape_task(self) -> Task:
        return Task(
            config=self.tasks_config["scrape_task"],
            agent=self.scraper(),
            output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_scrape_task.md",
        )
        
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.researcher(),
            output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_research_task.md",
        )

    @task
    def newspaper_task(self) -> Task:
        return Task(
            config=self.tasks_config["newspaper_task"],
            agent=self.designer(),
            output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_newspaper_task_task.html",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Newspaper crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
        )