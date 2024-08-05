# src/ranking_crew/crew.py

import os
from crewai import Agent, Task, Crew, Process

# Defina seus agentes e tarefas
researcher = Agent(
    role="Job Candidate Researcher",
    goal="Find potential candidates for the job",
    backstory="You are adept at finding the right candidates by exploring various online resources. Your skill in identifying suitable candidates ensures the best match for job positions.",
)

research_task = Task(
    description="Conduct thorough research to find potential candidates for the specified job.",
    expected_output="A list of 10 potential candidates with their contact information and brief profiles highlighting their suitability.",
    agent=researcher,
)

crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential,
)

def run_crew():
    result = crew.kickoff(inputs={'job_description': 'Software Engineer'})
    print(result)

if __name__ == "__main__":
    run_crew()
