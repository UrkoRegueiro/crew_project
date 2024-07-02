from crew import NewspaperCrew
import os
from core.tools.functions import load_html_template
from dotenv import load_dotenv
load_dotenv()

def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {'html_template': load_html_template()}
    NewspaperCrew().crew().kickoff(inputs=inputs)

run()