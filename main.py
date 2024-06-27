from crew import NewspaperCrew
import os
from dotenv import load_dotenv
load_dotenv()


def load_html_template(): 
    with open('core/utils/templates/template.html', 'r') as file:
        html_template = file.read()
        
    return html_template


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {'html_template': load_html_template()}
    NewspaperCrew().crew().kickoff(inputs=inputs)

run()