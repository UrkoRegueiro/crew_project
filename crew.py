from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from core.tools.agent_tools import InformationTool, SenderTool
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from datetime import datetime
import os


@CrewBase
class NewspaperCrew:
    """Newspaper crew"""

    agents_config = "core/agents/agents.yaml"
    tasks_config = "core/tasks/tasks.yaml"

    #def llm(self):
        #llm = ChatGroq(model="llama3-70b-8192",
               #groq_api_key= os.getenv('GROQ_API_KEY'))

        #return llm

    def llm(self):
        llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", openai_api_key=os.getenv('OPENAI_API_KEY'))

        return llm

    @agent
    def journalist(self) -> Agent:
        return Agent(
            config=self.agents_config["journalist"],
            tools=[InformationTool()],
            verbose=True,
            allow_delegation=False,
            llm=self.llm(),
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config["editor"],
            verbose=True,
            allow_delegation=False,
            llm=self.llm(),
        )

    @agent
    def sender(self) -> Agent:
        return Agent(
            config=self.agents_config["sender"],
            tools=[SenderTool()],
            verbose=True,
            allow_delegation=False,
            llm=self.llm(),
        )
        
    @task
    def journalist_task(self) -> Task:
        return Task(
            config=self.tasks_config["journalist_task"],
            agent=self.journalist(),
            output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_journalist_task.md",
        )

    @task
    def editor_task(self) -> Task:
        return Task(
            config=self.tasks_config["editor_task"],
            agent=self.editor(),
            output_file="index.html",
        )

    @task
    def sender_task(self) -> Task:
        return Task(
            config=self.tasks_config["sender_task"],
            agent=self.sender(),
            output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_sender_task.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Newspaper crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=1,
        )
